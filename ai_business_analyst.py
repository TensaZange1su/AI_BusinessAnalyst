import os
import json
import base64

import streamlit as st
import openai
import requests
import markdown2
from requests.auth import HTTPBasicAuth

# =========================
#  Настройка OpenAI клиента
# =========================


openai.api_key = "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"


# =========================
#  Конфигурация диалога
# =========================

QUESTIONS = [
    {
        "field": "business_goal",
        "title": "Цель",
        "question": "Какова основная бизнес-цель этой инициативы?",
        "textarea": True,
    },
    {
        "field": "problem",
        "title": "Проблема",
        "question": "Какая бизнес-проблема или боль лежит в основе задачи?",
        "textarea": True,
    },
    {
        "field": "target_users",
        "title": "Пользователи",
        "question": "Кто конечные пользователи / заинтересованные стороны?",
        "textarea": True,
    },
    {
        "field": "current_process",
        "title": "Текущий процесс",
        "question": "Опишите текущий процесс. Где узкие места?",
        "textarea": True,
    },
    {
        "field": "scope",
        "title": "Scope",
        "question": "Что входит и что НЕ входит в границы задачи?",
        "textarea": True,
    },
    {
        "field": "systems",
        "title": "Системы и интеграции",
        "question": "С какими системами связана доработка?",
        "textarea": True,
    },
    {
        "field": "business_rules",
        "title": "Бизнес-правила",
        "question": "Какие есть бизнес-правила, ограничения, SLAs?",
        "textarea": True,
    },
    {
        "field": "kpi",
        "title": "KPI и метрики",
        "question": "Какие KPI/метрики важны для успеха?",
        "textarea": True,
    },
    {
        "field": "risks",
        "title": "Риски и допущения",
        "question": "Какие риски и зависимости нужно учитывать?",
        "textarea": True,
    },
    {
        "field": "timeline",
        "title": "Сроки",
        "question": "Целевые сроки, приоритет и этапность (MVP → полная версия)?",
        "textarea": True,
    },
]


def init_state():
    if "dialog_data" not in st.session_state:
        st.session_state.dialog_data = {q["field"]: "" for q in QUESTIONS}
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "brd_data" not in st.session_state:
        st.session_state.brd_data = None
    if "quality_report" not in st.session_state:
        st.session_state.quality_report = None
    if "diagrams" not in st.session_state:
        st.session_state.diagrams = None
    if "diagram_png" not in st.session_state:
        st.session_state.diagram_png = {"process": None, "usecase": None}
    if "initiative_type" not in st.session_state:
        st.session_state.initiative_type = "Продуктовая"
    if "use_png_service" not in st.session_state:
        st.session_state.use_png_service = False


def get_next_question():
    for q in QUESTIONS:
        if not st.session_state.dialog_data.get(q["field"], "").strip():
            return q
    return None


# =========================
#  Вызов OpenAI ChatCompletion
# =========================

def call_openai_chat(messages, model: str = "gpt-4o", temperature: float = 0.3) -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response["choices"][0]["message"]["content"]


# =========================
#  BRD: генерация
# =========================

def build_brd_prompt(dialog_data: dict, initiative_type: str) -> str:
    """
    Формируем промпт для генерации BRD с учётом типа инициативы.
    """
    type_comment = {
        "Продуктовая": "Фокус на клиентском опыте, продуктовых метриках, воронке и монетизации.",
        "Процессная": "Фокус на оптимизации процессов, SLA, времени цикла, операционной эффективности.",
        "ИТ-система": "Фокус на архитектуре, интеграциях, надёжности, безопасности и технических ограничениях.",
        "Compliance/Риск": "Фокус на регуляторных требованиях, политике, контролях и снижении рисков.",
    }.get(initiative_type, "")

    return f"""
Ты опытный бизнес-аналитик в крупном банке.
Тип инициативы: {initiative_type}.
Особенности: {type_comment}

На основе данных ниже составь структурированное бизнес-требование (BRD).

Исходные данные:
- Цель: {dialog_data.get('business_goal')}
- Проблема: {dialog_data.get('problem')}
- Пользователи: {dialog_data.get('target_users')}
- Текущий процесс: {dialog_data.get('current_process')}
- Scope: {dialog_data.get('scope')}
- Системы: {dialog_data.get('systems')}
- Бизнес-правила: {dialog_data.get('business_rules')}
- KPI: {dialog_data.get('kpi')}
- Риски: {dialog_data.get('risks')}
- Сроки: {dialog_data.get('timeline')}

Сформируй BRD ТОЛЬКО в формате JSON (без текста, без markdown):

{{
  "цель": "краткое описание",
  "описание": "понятное описание контекста",
  "scope": "что входит и что не входит",
  "бизнес_правила": ["правило 1", "правило 2"],
  "KPI": {{"метрика 1": "описание", "метрика 2": "описание"}},
  "user_stories": [
    {{
      "роль": "кто",
      "цель": "что хочет",
      "ценность": "зачем",
      "описание": "as a ... I want ... so that ..."
    }}
  ],
  "use_cases": [
    {{
      "название": "UC1. Название",
      "область_действия": "область",
      "участники": ["участник 1"],
      "основное_действующее_лицо": "актор",
      "предусловие": "условие",
      "триггер": "событие",
      "основной_поток": ["шаг 1", "шаг 2"],
      "альтернативный_поток": ["альт 1"],
      "результат": "результат"
    }}
  ],
  "лидирующие_индикаторы": ["индикатор 1"]
}}

ВАЖНО: Ответ ТОЛЬКО JSON, без пояснений!
"""


def generate_brd(dialog_data: dict, initiative_type: str):
    prompt = build_brd_prompt(dialog_data, initiative_type)
    messages = [
        {"role": "system", "content": "Ты опытный бизнес-аналитик. Возвращай ТОЛЬКО валидный JSON."},
        {"role": "user", "content": prompt},
    ]
    raw = call_openai_chat(messages)

    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()

    try:
        data = json.loads(cleaned)
        return data, raw
    except json.JSONDecodeError as e:
        return None, raw


# =========================
#  Анализ качества BRD
# =========================

def build_quality_prompt(dialog_data: dict, brd: dict, initiative_type: str) -> str:
    return f"""
Ты ведущий бизнес-аналитик и методолог. Оцени качество BRD.
Тип инициативы: {initiative_type}.

Исходные данные:
{json.dumps(dialog_data, ensure_ascii=False, indent=2)[:500]}...

BRD:
{json.dumps(brd, ensure_ascii=False, indent=2)[:500]}...

Вернись ТОЛЬКО JSON (без текста):

{{
  "overall_score": 85,
  "summary": "краткая оценка",
  "scores": {{
    "completeness": {{"value": 85, "comment": "текст"}},
    "clarity": {{"value": 80, "comment": "текст"}},
    "consistency": {{"value": 90, "comment": "текст"}},
    "feasibility": {{"value": 75, "comment": "текст"}},
    "business_value": {{"value": 88, "comment": "текст"}}
  }},
  "missing_information": ["что уточнить"],
  "risks": ["какие риски"],
  "suggested_questions": ["вопрос заказчику"]
}}

ВАЖНО: ТОЛЬКО JSON!
"""


def generate_quality_report(dialog_data: dict, brd: dict, initiative_type: str):
    prompt = build_quality_prompt(dialog_data, brd, initiative_type)
    messages = [
        {"role": "system", "content": "Возвращай ТОЛЬКО валидный JSON."},
        {"role": "user", "content": prompt},
    ]
    raw = call_openai_chat(messages)

    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()

    try:
        data = json.loads(cleaned)
        return data, raw
    except json.JSONDecodeError:
        return None, raw


# =========================
#  Диаграммы (Mermaid)
# =========================

def build_diagram_prompt(dialog_data: dict, brd: dict, initiative_type: str) -> str:
    return f"""
Ты системный аналитик. Сгенерируй две Mermaid диаграммы.

Тип инициативы: {initiative_type}.

Вернись ТОЛЬКО JSON (без текста, без markdown):

{{
  "process_diagram_mermaid": "flowchart TD\\n    A[Start]\\n    B[Process]\\n    A --> B",
  "usecase_diagram_mermaid": "flowchart TD\\n    A[Actor]\\n    B[Use Case]\\n    A --> B"
}}

Требования:
1. process_diagram_mermaid: используй flowchart TD или flowchart LR синтаксис
   - Пример: flowchart TD\\n    Start[Начало]\\n    Process[Процесс]\\n    End[Конец]\\n    Start --> Process\\n    Process --> End
2. usecase_diagram_mermaid: используй flowchart TD или flowchart LR синтаксис (НЕ usecase)
   - Пример: flowchart TD\\n    User[Пользователь]\\n    UC1[Вариант использования]\\n    User --> UC1
3. Используй \\\\n для переносов строк (двойной backslash!)
4. Используй только ASCII символы и кириллицу в квадратных скобках
5. ТОЛЬКО JSON, без пояснений, без markdown!

Диалог (кратко): {json.dumps(dialog_data, ensure_ascii=False)[:200]}...
BRD (кратко): {json.dumps(brd, ensure_ascii=False)[:200]}...
"""


def generate_diagrams(dialog_data: dict, brd: dict, initiative_type: str):
    prompt = build_diagram_prompt(dialog_data, brd, initiative_type)
    messages = [
        {"role": "system", "content": "Ты системный аналитик. Возвращай ТОЛЬКО валидный JSON."},
        {"role": "user", "content": prompt},
    ]
    raw = call_openai_chat(messages)

    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()

    try:
        data = json.loads(cleaned)
        return data, raw
    except json.JSONDecodeError:
        return None, raw


# =========================
#  Генерация PNG через Kroki
# =========================

def generate_mermaid_png_safe(mermaid_code: str) -> bytes | None:
    """Генерируем PNG через Kroki с заменой \\n на \n."""
    if not mermaid_code.strip():
        return None
    try:
        mermaid_code = mermaid_code.replace("\\n", "\n")  # исправляем переносы
        resp = requests.post(
            "https://kroki.io/mermaid/png",
            data=mermaid_code.encode("utf-8"),
            timeout=15,
        )
        if resp.status_code == 200:
            return resp.content
        st.warning(f"Kroki вернул статус {resp.status_code}")
        return None
    except Exception as e:
        st.warning(f"Ошибка генерации PNG: {e}")
        return None


# =========================
#  Confluence API
# =========================

def create_confluence_page(
    base_url: str,
    email: str,
    api_token: str,
    space_key: str,
    title: str,
    html_body: str,
    parent_page_id: str | None = None,
):
    """Создаём страницу в Confluence."""
    url = f"{base_url.rstrip('/')}/rest/api/content"

    headers = {"Content-Type": "application/json"}

    data = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": html_body,
                "representation": "storage",
            }
        },
    }

    if parent_page_id:
        data["ancestors"] = [{"id": parent_page_id}]

    resp = requests.post(
        url,
        headers=headers,
        auth=HTTPBasicAuth(email, api_token),
        json=data,
        timeout=20,
    )

    if resp.status_code not in (200, 201):
        raise Exception(f"Ошибка Confluence API: {resp.status_code} — {resp.text}")

    return resp.json()


# =========================
#  BRD → Markdown → HTML
# =========================

def brd_to_markdown(brd: dict) -> str:
    """Конвертируем BRD в Markdown."""
    md = "# Бизнес-требование (BRD)\n\n"

    md += "## Цель\n"
    md += f"{brd.get('цель', '')}\n\n"

    md += "## Описание\n"
    md += f"{brd.get('описание', '')}\n\n"

    md += "## Scope\n"
    md += f"{brd.get('scope', '')}\n\n"

    md += "## Бизнес-правила\n"
    rules = brd.get("бизнес_правила", [])
    if isinstance(rules, list):
        for r in rules:
            md += f"- {r}\n"
    else:
        md += f"{rules}\n"
    md += "\n"

    md += "## KPI\n"
    kpi = brd.get("KPI", {})
    if isinstance(kpi, dict):
        for k, v in kpi.items():
            md += f"- **{k}**: {v}\n"
    elif isinstance(kpi, list):
        for item in kpi:
            md += f"- {item}\n"
    else:
        md += f"{kpi}\n"
    md += "\n"

    md += "## User Stories\n"
    for idx, us in enumerate(brd.get("user_stories", []), 1):
        if isinstance(us, dict):
            md += f"### US{idx}\n"
            md += f"- Роль: {us.get('роль', '')}\n"
            md += f"- Цель: {us.get('цель', '')}\n"
            md += f"- Ценность: {us.get('ценность', '')}\n"
            md += f"- Описание: {us.get('описание', '')}\n\n"
        else:
            md += f"- {us}\n"

    md += "## Use Cases\n"
    for idx, uc in enumerate(brd.get("use_cases", []), 1):
        md += f"### UC{idx}: {uc.get('название', 'Нет данных')}\n"
        md += f"- Область действия: {uc.get('область_действия', 'Нет данных')}\n"
        md += f"- Участники: {', '.join(uc.get('участники', []) or [])}\n"
        md += f"- Основное действующее лицо: {uc.get('основное_действующее_лицо', 'Нет данных')}\n"
        md += f"- Предусловие: {uc.get('предусловие', 'Нет данных')}\n"
        md += f"- Триггер: {uc.get('триггер', 'Нет данных')}\n"
        md += f"- Основной поток:\n"
        for step in uc.get("основной_поток", []) or []:
            md += f"  - {step}\n"
        md += f"- Альтернативный поток:\n"
        for step in uc.get("альтернативный_поток", []) or []:
            md += f"  - {step}\n"
        md += f"- Результат: {uc.get('результат', 'Нет данных')}\n\n"

    md += "## Лидирующие индикаторы\n"
    for li in brd.get("лидирующие_индикаторы", []) or []:
        md += f"- {li}\n"

    return md


def build_confluence_html(md_content: str, proc_png: bytes | None, uc_png: bytes | None) -> str:
    """Конвертируем Markdown в HTML и добавляем PNG-диаграммы."""
    try:
        html_body = markdown2.markdown(md_content)
    except Exception:
        html_body = f"<pre>{md_content}</pre>"

    extra_parts = []

    if proc_png:
        b64 = base64.b64encode(proc_png).decode("utf-8")
        extra_parts.append(
            "<h2>Диаграмма процесса</h2>"
            f'<img src="data:image/png;base64,{b64}" alt="Process diagram" style="max-width:100%;" />'
        )

    if uc_png:
        b64 = base64.b64encode(uc_png).decode("utf-8")
        extra_parts.append(
            "<h2>Диаграмма вариантов использования</h2>"
            f'<img src="data:image/png;base64,{b64}" alt="Use case diagram" style="max-width:100%;" />'
        )

    if extra_parts:
        html_body += "<hr/>" + "".join(extra_parts)

    return html_body


# =========================
#  Mermaid отрисовка
# =========================

def render_mermaid(mermaid_code: str):
    if not mermaid_code:
        st.warning("Код диаграммы не предоставлен.")
        return

    mermaid_code = mermaid_code.strip().strip("`").replace("`", "\\`")

    html = f"""
    <div id="mermaid-container" style="overflow-x:auto;"></div>

    <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
    <script>
        const graphDefinition = `{mermaid_code}`;
        mermaid.initialize({{ startOnLoad: false, securityLevel: 'loose' }});
        mermaid.render('theGraph', graphDefinition, (svgCode) => {{
            document.getElementById('mermaid-container').innerHTML = svgCode;
        }});
    </script>
    """

    st.components.v1.html(html, height=700, scrolling=True)

# =========================
#  UI
# =========================

st.set_page_config(page_title="AI Business Analyst", layout="wide")
init_state()

# ----- SIDEBAR -----

with st.sidebar:
    st.header("⚙️ Настройки")

    st.session_state.initiative_type = st.selectbox(
        "Тип инициативы",
        ["Продуктовая", "Процессная", "ИТ-система", "Compliance/Риск"],
    )

    st.session_state.use_png_service = st.checkbox(
        "Генерировать PNG через Kroki",
        value=st.session_state.use_png_service,
    )

    st.markdown("---")
    st.subheader("📄 Confluence (опционально)")

    conf_url = st.text_input("URL", placeholder="https://xxx.atlassian.net/wiki")
    conf_email = st.text_input("Email", placeholder="your@email.com")
    conf_token = st.text_input("API Token", type="password", placeholder="xxx...")
    conf_space = st.text_input("Space Key", placeholder="MYSPACE")
    conf_parent = st.text_input("Parent Page ID", placeholder="12345")

    st.markdown("---")
    st.info("🔒 Ваши учётные данные не сохраняются")


st.title("🤖 AI Business Analyst")
st.markdown(
    "Агент ведёт диалог, собирает требования, генерирует BRD с User Stories и Use Cases, "
    "оценивает качество, строит диаграммы и публикует в Confluence."
)

col_chat, col_brd = st.columns([2, 3])

# ====== Левая колонка: диалог ======

with col_chat:
    st.subheader("💬 Диалог")

    for msg in st.session_state.chat_history:
        if msg["role"] == "assistant":
            st.markdown(f"**BA:** {msg['content']}")
        else:
            st.markdown(f"**Вы:** {msg['content']}")

    next_q = get_next_question()

    if next_q:
        if not st.session_state.chat_history:
            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": f"Привет! Я AI-бизнес-аналитик. Тип: **{st.session_state.initiative_type}**. "
                    "Давай разберём твою задачу по 10 ключевым вопросам.",
                }
            )
            st.rerun()

        st.markdown(f"**BA:** {next_q['question']}")

        if next_q["textarea"]:
            answer = st.text_area("Ваш ответ", key=f"answer_{next_q['field']}", height=100)
        else:
            answer = st.text_input("Ваш ответ", key=f"answer_{next_q['field']}")

        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("✅ Отправить", use_container_width=True):
                if not answer.strip():
                    st.warning("Пожалуйста, введите ответ.")
                else:
                    st.session_state.dialog_data[next_q["field"]] = answer.strip()
                    st.session_state.chat_history.append({"role": "user", "content": answer.strip()})
                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": f"✓ Спасибо! Ответ на **{next_q['title']}** получен.",
                        }
                    )
                    st.rerun()
    else:
        st.success("✅ Все вопросы заполнены!")

        if st.button("🚀 Сгенерировать BRD", use_container_width=True, type="primary"):
            with st.spinner("🔄 Генерируем BRD..."):
                brd_data, raw_brd = generate_brd(st.session_state.dialog_data, st.session_state.initiative_type)
                if brd_data is None:
                    st.error("❌ Ошибка парсинга JSON от GPT")
                    st.code(raw_brd[:500])
                else:
                    st.session_state.brd_data = brd_data
                    st.success("✅ BRD готов!")

                    with st.spinner("📊 Анализируем качество..."):
                        q_data, _ = generate_quality_report(
                            st.session_state.dialog_data, brd_data, st.session_state.initiative_type
                        )
                        if q_data:
                            st.session_state.quality_report = q_data

                    with st.spinner("📈 Строим диаграммы..."):
                        d_data, _ = generate_diagrams(
                            st.session_state.dialog_data, brd_data, st.session_state.initiative_type
                        )
                        if d_data:
                            st.session_state.diagrams = d_data

                            # PNG через Kroki
                            if st.session_state.use_png_service:
                                proc_code = d_data.get("process_diagram_mermaid", "")
                                uc_code = d_data.get("usecase_diagram_mermaid", "")
                                st.session_state.diagram_png["process"] = generate_mermaid_png_safe(proc_code)
                                st.session_state.diagram_png["usecase"] = generate_mermaid_png_safe(uc_code)
                    st.rerun()

    if st.button("🔄 Новый диалог", use_container_width=True):
        for key in ["dialog_data", "chat_history", "brd_data", "quality_report", "diagrams", "diagram_png"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


# ====== Правая колонка: результаты ======

with col_brd:
    st.subheader("📊 Результаты")

    tabs = st.tabs(["📄 BRD", "✅ Качество", "📈 Диаграммы"])

    # ----- BRD -----
    with tabs[0]:
        if st.session_state.brd_data:
            brd = st.session_state.brd_data

            st.markdown("### 🎯 Цель")
            st.info(brd.get("цель", ""))

            st.markdown("### 📋 Описание")
            st.write(brd.get("описание", ""))

            st.markdown("### 📦 Scope")
            st.write(brd.get("scope", ""))

            st.markdown("### ⚖️ Бизнес-правила")
            rules = brd.get("бизнес_правила", [])
            if isinstance(rules, list):
                for r in rules:
                    st.write(f"• {r}")
            else:
                st.write(rules)

            st.markdown("### 📊 KPI")
            kpi = brd.get("KPI", {})
            if isinstance(kpi, dict):
                for k, v in kpi.items():
                    st.write(f"• **{k}**: {v}")
            elif isinstance(kpi, list):
                for item in kpi:
                    st.write(f"• {item}")

            st.markdown("### 👥 User Stories")
            for idx, us in enumerate(brd.get("user_stories", []), 1):
                if isinstance(us, dict):
                    st.write(
                        f"**US{idx}**: {us.get('роль')} → {us.get('цель')} ({us.get('ценность')})"
                    )
                else:
                    st.write(f"• {us}")

            st.markdown("### 📚 Use Cases")
            for idx, uc in enumerate(brd.get("use_cases", []), 1):
                with st.expander(f"UC{idx}: {uc.get('название', 'Нет данных')}"):
                    st.write(f"**Область**: {uc.get('область_действия')}")
                    st.write(f"**Участники**: {', '.join(uc.get('участники', []) or [])}")
                    st.write(f"**Основной актор**: {uc.get('основное_действующее_лицо')}")
                    st.write(f"**Предусловие**: {uc.get('предусловие')}")
                    st.write(f"**Триггер**: {uc.get('триггер')}")
                    st.write("**Основной поток**:")
                    for step in uc.get("основной_поток", []) or []:
                        st.write(f"  {step}")
                    st.write("**Альтернативный поток**:")
                    for step in uc.get("альтернативный_поток", []) or []:
                        st.write(f"  {step}")
                    st.write(f"**Результат**: {uc.get('результат')}")

            st.markdown("### 🚦 Лидирующие индикаторы")
            for li in brd.get("лидирующие_индикаторы", []) or []:
                st.write(f"• {li}")

            md_content = brd_to_markdown(brd)

            col1, col2 = st.columns([1, 1])
            with col1:
                st.download_button(
                    "⬇️ Markdown",
                    md_content.encode("utf-8"),
                    file_name="BRD.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

            with col2:
                if st.button("📄 В Confluence", use_container_width=True):
                    if not (conf_url and conf_email and conf_token and conf_space):
                        st.error("⚠️ Заполни Confluence настройки в левой панели")
                    else:
                        try:
                            proc_png = st.session_state.diagram_png.get("process")
                            uc_png = st.session_state.diagram_png.get("usecase")
                            html_body = build_confluence_html(md_content, proc_png, uc_png)

                            result = create_confluence_page(
                                base_url=conf_url,
                                email=conf_email,
                                api_token=conf_token,
                                space_key=conf_space,
                                title=f"BRD — {brd.get('цель', 'Новое требование')}",
                                html_body=html_body,
                                parent_page_id=conf_parent or None,
                            )
                            link = result.get("_links", {}).get("base", "") + result.get("_links", {}).get("webui", "")
                            st.success("✅ Страница создана в Confluence!")
                            st.markdown(f"[🔗 Открыть]({link})")
                        except Exception as e:
                            st.error(f"❌ Ошибка: {str(e)[:200]}")
        else:
            st.info("BRD появится здесь после генерации")

    # ----- Качество -----
    with tabs[1]:
        qr = st.session_state.quality_report
        if qr:
            score = qr.get("overall_score", 0)
            summary = qr.get("summary", "")

            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("Общая оценка", f"{score}/100")
            with col2:
                st.write(f"*{summary}*")

            st.markdown("#### Критерии")
            scores = qr.get("scores", {})
            cols = st.columns(len(scores))

            for idx, (name, data) in enumerate(scores.items()):
                with cols[idx]:
                    value = data.get("value", 0)
                    st.metric(name.capitalize(), f"{value}/100")
                    st.caption(data.get("comment", ""))

            if qr.get("missing_information"):
                st.markdown("#### ❓ Что не хватает")
                for item in qr.get("missing_information", []):
                    st.write(f"• {item}")

            if qr.get("risks"):
                st.markdown("#### ⚠️ Риски")
                for r in qr.get("risks", []):
                    st.write(f"• {r}")

            if qr.get("suggested_questions"):
                st.markdown("#### ❓ Уточняющие вопросы")
                for q in qr.get("suggested_questions", []):
                    st.write(f"• {q}")
        else:
            st.info("Оценка качества появится после генерации BRD")

    # ====== Диаграммы с надежным fallback ======
    with tabs[2]:
        dg = st.session_state.diagrams
        if dg:
            proc_png = st.session_state.diagram_png.get("process")
            uc_png = st.session_state.diagram_png.get("usecase")

            # Показываем PNG если есть, иначе предупреждение
            if proc_png:
                st.image(proc_png, caption="Диаграмма процесса (PNG)", use_column_width=True)
            else:
                st.info("PNG диаграмма процесса отсутствует")

            if uc_png:
                st.image(uc_png, caption="Диаграмма Use Cases (PNG)", use_column_width=True)
            else:
                st.info("PNG диаграмма Use Cases отсутствует")

            # Показываем исходники Mermaid
            proc_code = dg.get("process_diagram_mermaid", "")
            uc_code = dg.get("usecase_diagram_mermaid", "")

            if proc_code or uc_code:
                st.markdown("#### Исходники Mermaid (для редактирования в сторонних редакторах)")
                if proc_code:
                    with st.expander("Диаграмма процесса"):
                        st.code(proc_code, language="mermaid")
                if uc_code:
                    with st.expander("Диаграмма Use Cases"):
                        st.code(uc_code, language="mermaid")

                # Скачать все исходники
                diagrams_md = "# Диаграммы\n\n"
                if proc_code:
                    diagrams_md += f"## Процесс\n```mermaid\n{proc_code}\n```\n\n"
                if uc_code:
                    diagrams_md += f"## Use Cases\n```mermaid\n{uc_code}\n```\n"

                st.download_button(
                    "⬇️ Скачать Mermaid исходники",
                    diagrams_md.encode("utf-8"),
                    file_name="diagrams.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
        else:
            st.info("Диаграммы появятся после генерации BRD")





