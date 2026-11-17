# PV CasePro

**PV CasePro** is an educational pharmacovigilance case-processing and quality-management application built with Python, Streamlit, SQLAlchemy and SQLite. It demonstrates fictional Individual Case Safety Report (ICSR) intake, assessment, follow-up, quality review, workflow and reporting concepts for a student portfolio.

> **EDUCATIONAL SIMULATION ONLY — NOT FOR REAL-WORLD PHARMACOVIGILANCE REPORTING.**

**Live demo:** Not deployed yet.

## Screenshots

Add synthetic-data screenshots to `screenshots/` after browser review. Never capture real personal or health information.

## Features

- Dashboard metrics and interactive charts sourced from SQLite, with date filters.
- Structured intake using the four minimum case criteria, date validation and possible-duplicate assistance.
- Case editing, separate seriousness and severity assessments, causality rationale and reference-based expectedness practice.
- Fictional terminology practice clearly separated from reported verbatim wording.
- Follow-up create/update tracking and neutral question templates; no email is sent.
- Editable narrative stored separately from source narrative, QC checklist with human review, workflow audit history.
- Disclaimer-bearing CSV, Excel, text, follow-up and QC exports; consistent SQLite backup.
- 30-question educational quiz and attempt history.
- Safe read-only public demo mode. Local development features remain available by opting into local mode.

## Architecture

```text
app.py                 Streamlit UI and navigation
database/models.py     SQLAlchemy schema
database/db.py         Additive initialization and migrations
services/              Validation, case, dashboard, follow-up, backup, narrative and export logic
sample_data/           Fictional synthetic seed cases
modules/training.py    Quiz content and scoring
tests/                 Pytest coverage
```

The normalized SQLite schema includes cases, patients, reporters, products, events, assessments, follow-ups, fictional reference safety information, QC reviews, audit logs and training attempts. The local database file is `database/pv_casepro.db` and is excluded from Git. Schema startup creates missing tables and adds safe nullable columns without dropping existing records.

## Technology

Python 3.11+, Streamlit, SQLite, SQLAlchemy, Pandas, Plotly and OpenPyXL. Pytest is included through `requirements-dev.txt` for local development.

## Windows 11 setup

```powershell
cd D:\PV_CasePro
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

The default mode is read-only, safe for a public demonstration. To enable local case processing and administrative features:

```powershell
$env:PV_CASEPRO_DEMO_MODE = "0"
streamlit run app.py
```

For read-only mode, leave the variable unset or set it to `1`. The application creates the SQLite schema and inserts 10 synthetic examples if no cases exist.

## Testing

```powershell
python -m compileall .
python -m pytest -v
```

## Sample workflow

Review the synthetic case library and dashboard; in local mode, create or edit a fictional case, record an assessment, track follow-up, review a narrative, perform QC, record a workflow transition and export reports. See [USER_GUIDE.md](USER_GUIDE.md).

## Safe use and limitations

Use fictional data only. This portfolio simulation is not validated for GxP, electronic-record regulation, clinical decision-making or regulatory submission. Training terminology is fictional and is not an official MedDRA database or certification. Causality and seriousness require human assessment. Expectedness requires supplied fictional reference safety information. Public mode uses local ephemeral storage and is read-only; it does not promise durable user data. No external APIs or paid services are needed.

## Project documents

- [Project report](PROJECT_REPORT.md)
- [QA report](QA_REPORT.md)
- [Deployment guide](STREAMLIT_DEPLOYMENT.md)
- [Contributing](CONTRIBUTING.md)
- [Final release report](FINAL_RELEASE_REPORT.md)
