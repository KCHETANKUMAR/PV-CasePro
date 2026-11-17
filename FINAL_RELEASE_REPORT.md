# PV CasePro — Final Release Report

**Prepared:** 2026-11-17
**Release state:** Public GitHub release published; Streamlit Community Cloud deployment is prepared but not yet created.

## Project health

The local project is in good automated-test condition. The Streamlit source imports, schema initialization is additive, and the project includes synthetic records, operator documentation, public read-only mode and a passing test suite.

## Features

Dashboard and chart logic; synthetic case library; local case intake and editing; assessment and terminology training; fictional reference information; follow-up create/update; reviewed narrative; human QC; audited workflow; disclaimer-bearing CSV/XLSX/text outputs; quiz and attempt history; safe backup; confirmed synthetic-record reset.

## Verification

- Tests: **23 passed, 0 failed** (`python -m pytest -v`).
- Compile: **passed** (`python -m compileall .`).
- App import smoke check: **passed** (`APP_IMPORT_OK` in bare Streamlit mode).
- Browser tests: **not verified**; `http://localhost:8765` returned `net::ERR_CONNECTION_REFUSED`. A Streamlit `AppTest` attempt also failed to return and was interrupted; no UI pass is claimed.
- Security scan: no credentials or real patient data found; local DB is synthetic and ignored.

## GitHub and deployment

- Repository: [KCHETANKUMAR/PV-CasePro](https://github.com/KCHETANKUMAR/PV-CasePro), **public**.
- Branch: `main`; `origin` is configured and tracks the published branch.
- Initial commit: `78a4cf8be22fbedd2b9642d07b4ada6005301b8f` (`Initial PV CasePro release`).
- GitHub CLI authentication: verified for `KCHETANKUMAR` using the installed CLI path.
- License: **MIT**, with `Copyright (c) 2026 K Chetan Kumar`, in `LICENSE`.
- Streamlit Community Cloud deployment: **Not deployed**.
- Live demo URL: **None**.

## Remaining work

1. Sign in to Streamlit Community Cloud with the GitHub account that owns the repository.
2. Create an app from `KCHETANKUMAR/PV-CasePro`, branch `main`, entry point `app.py`, keeping demo mode read-only.
3. Open the generated URL and verify the dashboard, case library, reports, navigation and disclaimer before sharing it.
4. Capture screenshots after successful browser review and add them to `screenshots/`.

## Local run commands

```powershell
cd D:\PV_CasePro
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
$env:PV_CASEPRO_DEMO_MODE = "0"
streamlit run app.py
```

For a local read-only preview, set `PV_CASEPRO_DEMO_MODE` to `1` or leave it unset. Use fictional information only.
