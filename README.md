
# README (EN + RU)

```markdown
# 🤖 AI Business Analyst / AI Бизнес Аналитик

**AI-powered Business Requirements Document (BRD) generator** for ForteBank and enterprises.  
**Генератор бизнес-требований (BRD) с AI** для ForteBank и корпоративных клиентов.  

Conducts structured interviews, generates BRDs with User Stories and Use Cases, evaluates quality, and builds diagrams in Mermaid format with optional PNG export.  
Проводит структурированные интервью, генерирует BRD с User Stories и Use Cases, оценивает качество и строит диаграммы в формате Mermaid с опциональным экспортом PNG.


## 📋 Table of Contents / Содержание

* [Features / Функционал](#features--функционал)
* [Architecture / Архитектура](#architecture--архитектура)
* [Installation / Установка](#installation--установка)
* [Configuration / Настройка](#configuration--настройка)
* [Usage / Использование](#usage--использование)
* [Outputs / Результаты](#outputs--результаты)
* [Advanced Features / Расширенные возможности](#advanced-features--расширенные-возможности)
* [Troubleshooting / Решение проблем](#troubleshooting--решение-проблем)

---

## ✨ Features / Функционал

### 🎯 Core Functionality / Основное

* **Interactive Dialog / Интерактивный диалог** – 10 шагов для сбора требований
* **Intelligent BRD Generation / Генерация BRD AI** – через GPT-4o
* **Multi-Initiative Support / Поддержка типов инициатив**:

  * **Product / Продуктовая** – опыт клиентов, метрики, монетизация
  * **Process / Процессная** – оптимизация процессов, SLA, время цикла
  * **IT System / ИТ-система** – архитектура, интеграции, безопасность, надежность
  * **Compliance/Risk / Соответствие и Риск** – регуляторные требования, контроль, смягчение рисков

### 📊 BRD Structure / Структура BRD

Each generated BRD includes:  
Каждый BRD содержит:

* **Goal / Цель** – business objective / бизнес-цель
* **Description / Описание** – context and problem statement / контекст и описание проблемы
* **Scope / Объем** – included and excluded scope / включенный и исключенный объем
* **Business Rules / Бизнес-правила** – rules, constraints, SLA / правила, ограничения, SLA
* **KPI** – key performance indicators / ключевые показатели
* **User Stories / User Stories** – требования в формате user story
* **Use Cases / Use Cases** – сценарии с основным и альтернативными потоками
* **Leading Indicators / Лидирующие индикаторы** – early success indicators / ранние индикаторы успеха

### ✅ Quality Analysis / Оценка качества

Automated assessment:  
Автоматическая оценка:

* Completeness, Clarity, Consistency, Feasibility, Business Value (0-100)  
  Полнота, ясность, согласованность, реализуемость, бизнес-ценность (0-100)
* Detection of missing information / Поиск недостающей информации
* Risk identification / Идентификация рисков
* Suggested follow-up questions / Предложения дополнительных вопросов

### 📈 Visual Diagrams / Визуализация

* **Process Diagrams / Процессные диаграммы** – flowcharts / блок-схемы
* **Use Case Diagrams / Диаграммы Use Case** – actors and relations / акторы и связи
* **Mermaid Syntax / Синтаксис Mermaid** – editable / редактируемый
* **PNG Export / Экспорт PNG** – via Kroki (optional) / через Kroki (опционально)
* **Fallback / Резерв** – Mermaid code always available / исходный код Mermaid всегда доступен

### 📤 Export & Integration / Экспорт и интеграция

* Markdown / Markdown экспорт
* HTML with base64-encoded diagrams / HTML с встроенными диаграммами
* Direct Confluence page creation / Создание страниц в Confluence
* Downloadable Mermaid source / Скачиваемый код Mermaid

---

## 🏗️ Architecture / Архитектура

```

┌───────────────────────────┐
│ Streamlit Web Interface   │
├─────────────┬─────────────┤
│ Left Column │ Right Column│
│  Dialog     │ BRD / Quality│
│  (10 Qs)   │ / Diagrams   │
└─────────────┴─────────────┘
│
┌──────▼───────┐
│ OpenAI GPT-4o│
└──────┬───────┘
│
┌──────▼───────┐
│  Kroki / PNG │
└──────┬───────┘
│
┌──────▼───────┐
│ Confluence   │
└──────────────┘

````

**Data Flow / Поток данных:**

1. User inputs → 10-question dialog / Пользователь отвечает на 10 вопросов  
2. BRD generated → GPT-4o JSON / BRD создается GPT-4o
3. Quality analysis → GPT-4o scoring / Оценка качества
4. Diagram creation → Mermaid code / Создание диаграмм Mermaid
5. PNG conversion → Kroki (optional) / Конвертация в PNG (опционально)
6. Confluence page → HTML with embedded images (optional) / Страница Confluence с изображениями (опционально)

---

## 🚀 Installation / Установка

### Prerequisites / Требования

* Python 3.10+
* pip
* OpenAI API Key
* Optional: Confluence API token for publishing / токен Confluence (опционально)

### Setup / Установка

```bash
git clone <repo-url>
cd AI_BusinessAnalyst
python -m venv venv
# Activate virtual environment:
# Windows PowerShell: venv\Scripts\Activate.ps1
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
````

Verify / Проверка:

```bash
python -c "import streamlit; import openai; print('✅ OK')"
```

---

## ⚙️ Configuration / Настройка

### OpenAI API Key

> The key is set **directly in the code** / Ключ задается **в коде**:

```python
import openai
openai.api_key = "sk-your-key"  # Insert your key here / Вставьте сюда свой ключ
```

> For production, using environment variables or secrets files is recommended for security.
> Для продакшн лучше использовать переменные окружения или файлы secrets для безопасности.

### Confluence (Optional / Опционально)

Sidebar fields / Поля в боковой панели:

| Field / Поле   | Description / Описание                 |
| -------------- | -------------------------------------- |
| URL            | Base Confluence URL / Базовый URL      |
| Email          | Atlassian account email / Email        |
| API Token      | Generate in Atlassian settings / Токен |
| Space Key      | Target space / Пространство            |
| Parent Page ID | Optional / Родительская страница       |

### PNG Generation (Optional / Генерация PNG)

Enable "Generate PNG via Kroki / Генерировать PNG через Kroki" in sidebar.

---

## 📖 Usage / Использование

```bash
streamlit run ai_business_analyst.py
```

1. Select initiative type / Выберите тип инициативы

2. Answer 10 questions in dialog / Ответьте на 10 вопросов в диалоге

3. Generate BRD / Сгенерируйте BRD:

   * AI generates JSON BRD / AI создает JSON BRD
   * Quality analysis / Оценка качества
   * Mermaid diagrams / Диаграммы Mermaid
   * Optional PNGs via Kroki / Опциональные PNG через Kroki

4. Review results in right column / Просмотрите результаты:

   * BRD
   * Quality scores / Оценки качества
   * Diagrams / Диаграммы (Mermaid + PNG)

5. Export or publish / Экспорт или публикация:

   * Markdown
   * Confluence page with embedded diagrams / Страница Confluence с диаграммами

---

## 📤 Outputs / Результаты

* **Markdown BRD / BRD.md**
* **Quality report / Отчет по качеству**
* **Mermaid diagrams / Диаграммы Mermaid**
* **PNG diagrams / PNG диаграммы (optional)**
* **Confluence page / Страница Confluence (optional)**

---

## 🔧 Advanced Features / Расширенные возможности

* Custom initiative types in `build_brd_prompt()` / Пользовательские типы инициатив
* Adjust AI behavior via `call_openai_chat()` / Настройка поведения AI
* Detailed Mermaid logging in browser / Логирование Mermaid в браузере

---

## 🐛 Troubleshooting / Решение проблем

* OpenAI API key missing → check code / отсутствует ключ → проверьте код
* Mermaid syntax errors → refresh browser / ошибки синтаксиса → обновите страницу
* PNG diagrams not generated → check internet / PNG не создаются → проверьте интернет
* Confluence publishing fails → verify credentials / Ошибка публикации → проверьте учетные данные

---
