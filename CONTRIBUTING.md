# Contributing

Thank you for helping improve PV CasePro. Keep contributions focused on the educational simulation and use synthetic data only.

## Before submitting

- Do not add personal health information, credentials, secrets, database files, logs, or private backups.
- Keep the disclaimer visible in the UI and all generated exports.
- Do not describe training terms as official MedDRA content or imply validated GxP use.
- Add or update tests for business rules and data changes.
- Run `python -m compileall .` and `python -m pytest -v`.
- Explain schema changes. Startup migrations must be additive and preserve existing data.

## Development setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
$env:PV_CASEPRO_DEMO_MODE = "0"
streamlit run app.py
```

By default, demo mode is read-only. Set it to `0` only for a local development session.
