# Рынок: что уже есть и где наш зазор

Проверено 13.11.2026. Источники — в конце файла. Пометка «проверено лично»
означает, что страницу открывала я, а не агент.

## Короткий вывод

Ниша «ИИ-аналитика стажёрской программы» на рынке РФ пустая, а на западном —
занята только частично и не там. Рынок разбит на три слоя, которые не
пересекаются:

1. **Онбординг-модули** в HR-платформах (Skillaz, Mirapolis, Websoft, Поток
   Адаптация) — поток задач и опрос новичка, риск считается по просрочкам.
2. **ИИ-аналитика опросов** (Поток Вовлечённость, Happy Job) — категории и
   тональность комментариев, но объект — сотрудник вообще, не стажёр.
3. **Платформы стажёрских программ** (Talent Rocks в РФ, Symba на Западе) —
   расписание, геймификация, менторство, но без ИИ-разбора текста.

Наш продукт живёт в разрыве между слоями: программа стажировки как объект,
парные опросы стажёр ↔ наставник, расхождение как сигнал, объяснимый риск.

## РФ

- **Skillaz Старт** (`skillaz.ru/start`, страница жива — проверено) — ближайший
  конкурент: пребординг, контрольные точки, pulse-опросы, «риски считаются
  автоматически», AI-помощник. Заявленный запуск 19.11.2026, кейсов нет,
  стажёрская программа как отдельный объект не выделена.
- **Поток** (`potok.io/pulse_survey/` — проверено) — сильнейший в РФ разбор
  комментариев: GPT распределяет по категориям и тональности, учитывает сленг
  и опечатки; «виртуальный аналитик» на YandexGPT. Но модули разрознены.
- **Mirapolis Onboarding** — «увидеть риски ухода» на данных прохождения плана:
  без текстов и без модели.
- **Happy Job** — контент-анализ предложений сотрудников, ИИ-ассистент, но на
  уровне компании.
- **Talent Rocks** — мобильная платформа стажёрских программ: расписания,
  микрообучение, QR-посещаемость, рейтинги. Аналитики нет вообще.
- **Опросники** (Testograf, Анкетолог, Яндекс Формы, forms.app) — ветвление как
  заранее заданные правила, ИИ-переспроса нет ни у кого.
- **1С:Оценка персонала** — снята с продаж (новость 1c.ru), строить на ней нельзя.

## Запад

- **Qualtrics Conversational Feedback** — единственный enterprise-игрок с
  адаптивными уточнениями: ИИ генерирует 1–2 follow-up под открытый ответ плюс
  валидация расплывчатости (проверено по документации). Ограничение, важное для
  позиционирования: в Engagement и Lifecycle проектах поддерживается **только
  один** follow-up; фича на новых тарифах.
- **Microsoft Viva Glint + Viva Insights** — ближайший аналог сверки
  самоотчёта с поведением: опрос склеен с метриками работы (время в 1:1,
  работа после часов, focus time). Ограничение — уровень команды, не человека.
- **Symba** — специализированная платформа стажёрских программ, ИИ не заявлен
  вовсе; в ноябре 2025 куплена Yello.
- **Workday Peakon** — attrition prediction как методология, но обучено на
  миллионах ответов и считается по сегментам: для 40 стажёров неприменимо.
- **Culture Amp, Lattice, Leapsome, 15Five, Workleap, Glint, Gallup** — анализ
  комментариев есть, адаптивности нет. Пороги, полезные для слайда: Culture Amp
  делает саммари от 5 осмысленных комментариев на вопрос; Gallup — 50 на
  саммари и 250 на темы.
- **Mentorloop / Mentorly** — Mentoring Quality Score и ИИ-синтез открытых
  ответов плюс объективные метрики сессий (отмены, no-show). Единственные, кто
  соединяет поведение и самоотчёт в менторском контексте, но без программы
  стажировки.

## Что из этого следует для решения

1. **Адаптивный опрос возвращается — но на своей форме.** Спор команды снял его
   как фичу потому, что писать в чужую форму мы не можем. Верное решение: своя
   форма опроса для демо и пилота, а внешний сервис подключается импортом.
   На рынке РФ этого нет ни у кого, у Qualtrics — один follow-up и только на
   новых тарифах. Дифференциатор подтверждён.
2. **Парный опрос стажёр ↔ наставник — второй, более сильный дифференциатор.**
   Наставник у всех исполнитель задач, а не объект оценки. Расхождение двух
   оптик на одного человека не считает никто.
3. **Сверку самоотчёта с поведением не обещаем полностью**: в проде это Viva
   Insights-подобная интеграция, у нас — только при наличии данных заказчика.
   На демо это синтетика с честной пометкой.
4. **Никакого прогноза оттока.** Peakon требует миллионов ответов; на 40
   стажёрах единственный защищаемый вариант — детерминированные флаги с
   порогами и цитаты.
5. **Стек под 152-ФЗ.** Отзывы сотрудников — персональные данные, зарубежные API
   на защите будут минусом: GigaChat или YandexGPT со structured output
   (JSON Schema) + pydantic-валидация. Это же снимает вопрос жюри «а где
   хранятся данные».
6. **Идеи Concord** (MIT, 215★ — проверено): очередь мусорных ответов, уровни
   доказательности, drill-down «цифра → цитата». Форкать не надо, идеи забрать.

## Опенсорс: что берём

- **Берём:** Next.js + shadcn/ui charts (обёртки над Recharts), Recharts для
  графиков, FastAPI + Postgres, structured output провайдера, Instructor
  (опционально), Langfuse Cloud (free) для трассировки промптов и версий,
  spaCy точечно для языка и маскировки ПДн.
- **Не берём:** Metabase, Superset, Grafana, Redash, Cube (BI не кастомизируется
  под кейс, AGPL у Metabase), Formbricks (6 контейнеров, ИИ в Enterprise, разбора
  открытых ответов в OSS нет), OpnForm, Typebot (FSL), LimeSurvey, Dify, RAGFlow,
  Langflow, Open WebUI.
- **Готового проекта для форка нет.** Concord ближе всех по смыслу, но молодой,
  англоцентричный, без движка опросов и без русского.

## Оценка работ на трёх человек

- формы + адаптивные уточнения — 4–6 ч
- пайплайн анализа: промпт, схема, батчи, кэш по хэшу — 6–8 ч
- проверка качества данных — 3–4 ч
- дашборд: 5 виджетов + drill-down до цитат — 10–12 ч
- риск-флаги с объяснением — 4 ч
- docker compose + один VPS — 3 ч

Демо-данные: 300–500 реалистичных русских комментариев генерировать заранее,
иначе показывать нечего.

## Источники

РФ: huntflow.ru, skillaz.ru, skillaz.ru/onboarding, skillaz.ru/start,
potok.io/onboarding, potok.io/pulse_survey/, potok.io/tariffs_potok/,
friend.work, hr-link.ru, e-staff.ru/tariffs, boss.ru/products/boss-hcm/,
ispring.ru/ispring-learn, teachbase.ru/tarify/, mirapolis.ru/onboarding/,
websoft.ru/onboarding, testograf.ru/ru/functions, anketolog.ru/pages/plans.html,
yandex.ru/forms/, forms.app/ru/pricing, happy-job.ru/engagement/,
research.ecopsy.ru/engagement, 1c.ru/news/info.jsp?id=34181,
talentrocks.ru/youth-programs.html, uplatforma.ru/graduate.

Запад: cultureamp.com/platform/ai, lattice.zendesk.com (Engagement Insights),
help.leapsome.com (AI summaries), success.15five.com (Amaya), help.workleap.com,
qualtrics.com/support/.../conversational-feedback/ (проверено лично),
learn.microsoft.com/viva/glint/setup/copilot-faqs-comments-summarization,
learn.microsoft.com/viva/solutions/glint-insights-integration-overview,
support.gallup.com (AI/ML on Gallup Access), doc.workday.com/peakon (attrition
prediction methodology), docs.visier.com (predictive models), symba.io/product,
yello.co/blog/yello-acquires-symba, mentorloop.com/mentoring-program-dashboard,
mentorly.com (Intelligence), abodehr.com/product/analytics-insights,
typeform.com/research-flow, surveymonkey.com/product/features/ai.

Опенсорс: github.com/metabase/metabase, github.com/apache/superset,
github.com/grafana/grafana, github.com/getredash/redash,
github.com/cube-js/cube, github.com/formbricks/formbricks,
github.com/langgenius/dify, github.com/infiniflow/ragflow,
github.com/langfuse/langfuse, github.com/567-labs/instructor,
github.com/recharts/recharts, github.com/shadcn-ui/ui,
github.com/emollick/concord (MIT, 215★ — проверено).

## Что не подтвердилось

- bestplacestowork.ru не отвечает; amstef.ru недоступен (блокировка).
- Gallup Help Center отдавал Cloudflare-заглушку — статьи читались через кэш,
  живую страницу подтвердить не удалось.
- «Formless AI» у Typeform отдельной страницы не имеет: в 2026 это Typeform AI
  и Research Flow, формулировку в питче лучше не использовать.
- Числа вендоров (пороги комментариев, лимит follow-up) взяты из документации
  на 13.11.2026 и могут меняться.
