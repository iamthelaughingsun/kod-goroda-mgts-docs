#!/usr/bin/env python3
"""Извлечение проблемы из свободного отзыва через LLM по строгой схеме.

Провайдер — любой OpenAI-совместимый endpoint. По умолчанию используется
гейтвей, который уже настроен на машине: opencode.ai/zen/go/v1 с qwen.
Для продакшена у МГТС достаточно поменять три переменные окружения —
код не меняется (GigaChat/YandexGPT через тот же OpenAI-совместимый фасад).

Запуск:
    python3 ai/extract.py "Всё нормально, но задач стало больше..."
"""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = os.environ.get("LLM_BASE_URL", "https://opencode.ai/zen/go/v1")
MODEL = os.environ.get("LLM_MODEL", "qwen3.8-flash")
KEY_ENV = os.environ.get("LLM_KEY_ENV", "OPENCODE_GO_API_KEY")

# impulse: qwen на гейтвее требует UA и session-заголовок; при переезде на
# GigaChat/YandexGPT эти заголовки станут пустыми через LLM_EXTRA_HEADERS.
EXTRA_HEADERS = {
    "User-Agent": os.environ.get("LLM_USER_AGENT", "Mozilla/5.0 (X11; Linux x86_64) Chrome/131"),
    "x-opencode-session": os.environ.get("LLM_SESSION", "mgts-hackathon"),
}

SCHEMA = {
    "type": "object",
    "properties": {
        "has_problem": {"type": "boolean",
                        "description": "есть ли в отзыве конкретная проблема; false для «ок», «всё хорошо»"},
        "topic": {"type": "string", "description": "тема проблемы, 1-3 слова; пусто если проблемы нет"},
        "problem": {"type": "string", "description": "суть проблемы одной фразой; пусто если проблемы нет"},
        "severity": {"type": "integer", "description": "от 1 (мелочь) до 5 (блокер)"},
        "quote": {"type": "string", "description": "дословная цитата из отзыва; пусто если проблемы нет"},
        "confidence": {"type": "number", "description": "уверенность 0..1"},
    },
    "required": ["has_problem", "topic", "problem", "severity", "quote", "confidence"],
    "additionalProperties": False,
}

SYSTEM = (
    "Ты аналитик программы стажировок. Из отзыва стажёра извлекаешь одну "
    "конкретную проблему. Отвечай по-русски, все поля текста по-русски.\n"
    "Если в отзыве нет конкретной проблемы (например «ок», «всё хорошо», "
    "«нормально»), верни has_problem=false, пустые topic/problem/quote, "
    "severity 1 и confidence ниже 0.3. Не выдумывай проблему, которой нет: "
    "ложная тревога хуже пропуска.\n"
    "Поле quote — дословный фрагмент отзыва, по которому видно проблему. "
    "Отвечай только JSON по схеме, без пояснений."
)


def _api_key():
    key = os.environ.get(KEY_ENV)
    if key:
        return key
    env_file = Path(os.environ.get("HERMES_ENV", Path.home() / ".hermes/.env"))
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.startswith(KEY_ENV + "="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit(f"нет ключа: задай {KEY_ENV}")


def _call(messages, key, timeout=90):
    body = json.dumps({
        "model": MODEL,
        "messages": messages,
        "temperature": 0,
        "max_tokens": 500,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "problem", "strict": True, "schema": SCHEMA},
        },
    }).encode()
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json", **EXTRA_HEADERS}
    req = urllib.request.Request(f"{BASE_URL}/chat/completions", data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.load(r)
    # reasoning_content отдаётся отдельным полем и в ответ не попадает
    return data["choices"][0]["message"]["content"]


def _valid(obj):
    """Ручная проверка: pydantic в хакатоне — лишняя зависимость.

    Контракт различает два валидных исхода: проблема найдена (текст заполнен)
    и сигнала нет (has_problem=false, пустые поля). Второй — не ошибка.
    """
    if not isinstance(obj, dict):
        return False
    for field in SCHEMA["required"]:
        if field not in obj:
            return False
    if not isinstance(obj["has_problem"], bool):
        return False
    if not (isinstance(obj["severity"], int) and 1 <= obj["severity"] <= 5):
        return False
    if not (isinstance(obj["confidence"], (int, float)) and 0 <= obj["confidence"] <= 1):
        return False
    for field in ("topic", "problem", "quote"):
        if not isinstance(obj[field], str):
            return False
    if obj["has_problem"]:
        return bool(obj["problem"].strip()) and bool(obj["quote"].strip())
    return True


def extract(comment, retries=1):
    key = _api_key()
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": f"Отзыв: {comment}"}]
    last_error = None
    for attempt in range(retries + 1):
        try:
            raw = _call(messages, key)
            obj = json.loads(raw)
        except (urllib.error.URLError, json.JSONDecodeError, KeyError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            continue
        if _valid(obj):
            return obj
        last_error = f"схема не сошлась: {raw[:200]}"
        messages = messages[:2] + [
            {"role": "assistant", "content": raw},
            {"role": "user", "content": "Ответ не соответствует схеме. Верни только JSON с полями has_problem, "
                                        "topic, problem, severity, quote, confidence."},
        ]
    raise SystemExit(f"не удалось получить валидный ответ: {last_error}")


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(json.dumps(extract(text), ensure_ascii=False, indent=2))
