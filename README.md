

## 🤖 AI Business Analyst

**AI-powered Business Requirements Document (BRD) generator** for ForteBank and enterprises. Conducts structured interviews, generates BRDs with User Stories and Use Cases, evaluates quality, and builds diagrams in Mermaid format with optional PNG export.

### 📋 Table of Contents

* [Features](#features)
  * [Architecture](#architecture)
  * [Installation](#installation)
  * [Configuration](#configuration)
  * [Usage](#usage)
  * [Outputs](#outputs)
  * [Advanced Features](#advanced-features)
  * [Troubleshooting](#troubleshooting)


## ✨ Features

### 🎯 Core Functionality

* **Interactive Dialog** – 10-step structured conversation to gather essential business requirements.
  * **Intelligent BRD Generation** – AI-powered BRD creation via GPT-4o.
  * **Multi-Initiative Support** – Tailored prompts for initiative types:

    * **Продуктовая** (Product) – customer experience, metrics, monetization.
    * **Процессная** (Process) – process optimization, SLAs, cycle time.
    * **ИТ-система** (IT System) – architecture, integrations, security, reliability.
    * **Compliance/Риск** (Compliance/Risk) – regulatory requirements, controls, risk mitigation.

### 📊 BRD Structure

Each generated BRD includes:

* **Цель** – Clear business objective
  * **Описание** – Context and problem statement
  * **Scope** – Included and excluded scope
  * **Бизнес-правила** – Rules, constraints, SLAs
  * **KPI** – Key performance indicators
  * **User Stories** – Requirements in user story format
  * **Use Cases** – Detailed use case descriptions with main and alternative flows
  * **Лидирующие индикаторы** – Early indicators to track success

### ✅ Quality Analysis

Automated assessment including:

* Completeness, Clarity, Consistency, Feasibility, Business Value (0-100)
  * Detection of missing information
  * Risk identification
  * Suggested follow-up questions

### 📈 Visual Diagrams

* **Process Diagrams** – Flowchart-based visualization
  * **Use Case Diagrams** – Actor and use case relationships
  * **Mermaid Syntax** – Editable diagrams
  * **PNG Export** – via Kroki service for Confluence pages (optional)
  * **Fallback** – Mermaid source always available if PNG fails

### 📤 Export & Integration

* Markdown export for further processing
  * HTML with base64-encoded diagrams for Confluence
  * Direct Confluence page creation
  * Downloadable Mermaid source code

---

## 🏗️ Architecture

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
```

**Data Flow:**

1. User inputs → 10-question dialog
   2. BRD generated → GPT-4o JSON
   3. Quality analysis → GPT-4o scoring
   4. Diagram creation → Mermaid code
   5. PNG conversion → Kroki (optional)
   6. Confluence page → HTML with embedded images (optional)

---

## 🚀 Installation

### Prerequisites

* Python 3.10+
  * pip
  * OpenAI API Key
  * Optional: Confluence API token for publishing

### Setup

```bash
git clone <repo-url>
cd AI_BusinessAnalyst
python -m venv venv
# Activate virtual environment:
# Windows PowerShell: venv\Scripts\Activate.ps1
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
```

Verify:

```bash
python -c "import streamlit; import openai; print('✅ OK')"
```

---

## ⚙️ Configuration

### OpenAI API Key
> Key setted **in code**

OPENAI_API_KEY = "sk-your-key" 

### Confluence (Optional)

Sidebar fields:

| Field          | Description                    |
| -------------- | ------------------------------ |
| URL            | Base Confluence URL            |
| Email          | Atlassian account email        |
| API Token      | Generate in Atlassian settings |
| Space Key      | Target space                   |
| Parent Page ID | Optional                       |

### PNG Generation (Optional)

Enable "Генерировать PNG через Kroki" in sidebar.

---

## 📖 Usage

```bash
streamlit run ai_business_analyst.py
```

1. Select initiative type.
   2. Answer 10 questions in dialog.
   3. Generate BRD:

      * AI generates JSON BRD
      * Quality analysis
      * Mermaid diagrams
      * Optional PNGs via Kroki
   4. Review results in right column:

      * BRD
      * Quality scores
      * Diagrams (Mermaid and PNG)
   5. Export or publish:

      * Markdown
      * Confluence page with embedded diagrams

---

## 📤 Outputs

* **Markdown BRD** (`BRD.md`)
  * **Quality report** (scores and missing info)
  * **Mermaid diagrams** (editable, downloadable)
  * **PNG diagrams** (optional)
  * **Confluence page** (optional, HTML + embedded images)

---

## 🔧 Advanced Features

* Custom initiative types in `build_brd_prompt()`
  * Adjust AI behavior via `call_openai_chat()`
  * Detailed Mermaid logging in browser

---

## 🐛 Troubleshooting

* OpenAI API key missing → check `.streamlit/secrets.toml` or environment
  * Mermaid syntax errors → refresh browser, regenerate diagrams
  * PNG diagrams not generated → check internet connection / disable Kroki
  * Confluence publishing fails → verify credentials, space, parent page

---



