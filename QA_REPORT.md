# PV CasePro QA Report

**QA date:** 2026-11-17
**Scope:** Existing project inspection, source-level security review, automated service/database/export testing and startup smoke check.

## Results

- `python -m compileall .` — passed.
- `python -m pytest -v` — **23 passed, 0 failed**.
- `python -c "import app; print('APP_IMPORT_OK')"` — completed with `APP_IMPORT_OK`; this imports and executes the default Streamlit script in bare mode, not a browser session.
- Streamlit browser check — **not verified**. Attempted `http://localhost:8765`; the browser returned `net::ERR_CONNECTION_REFUSED`. No browser-level pass is claimed.
- Streamlit `AppTest` — attempted, but did not return within the execution window and was interrupted; it is not counted as a pass or failure in the pytest total.

Automated coverage includes case creation/retrieval/edit and audit entries, validation and date checks, duplicate assistance, seriousness and expectedness safeguards, normalized child-record updates, dashboard date filtering/KPIs, follow-up create/update, quiz scoring, narrative missing-value handling, CSV and XLSX content/disclaimers, additive migration preservation, consistent backup integrity, and guarded demo reset preserving non-demo records.

## Defects found and fixed

1. Windows SQLite backup left the destination connection open, preventing temporary-file cleanup. Connections now close explicitly; the backup test verifies SQLite can read the copy.
2. Existing cases had no edit workflow, and follow-ups could only be added. Local mode now supports case and follow-up edits with normalized child records kept in sync.
3. Saving an edited narrative overwrote source narrative text. Reviewed output now has a separate field and additive schema migration.
4. Expectedness could be selected without any reference information. The assessment screen now limits that choice and displays the unavailable-reference message; the RSI comparison is explicitly educational and needs reviewer assessment.
5. Assessment and terminology edits were not kept in their normalized assessment/event tables. UI saves now synchronize those records.
6. Follow-up and QC CSV exports omitted the simulation disclaimer. All auxiliary CSV exports now include it.
7. Local backup and demo deletion controls were exposed in an unauthenticated app. `DEMO_MODE` is fail-safe/read-only by default; public navigation omits write/admin pages. Full tools require explicit local opt-in (`PV_CASEPRO_DEMO_MODE=0`).
8. App startup migration behavior now has a test proving nullable additions preserve an existing row.

## Security and privacy review

- Heuristic source scan found no API keys, passwords, private-key blocks or `.env` files in project source. No absolute local paths are embedded in Python application configuration; local paths derive from `__file__`.
- The local SQLite file contains 10 synthetic training records, is matched by `.gitignore`, and is not suitable for upload. Database, WAL/SHM, SQLite, logs, backups, virtual environments and secrets are ignored.
- The application and docs carry the educational-only restriction. No real patient data was observed in the sample rows.
- Public demo mode is read-only and hides case intake/edit, assessment updates, follow-up mutation, quiz writes, workflow, database backup and demo reset. Public exports are still available for synthetic records.
- Local SQLite storage on Community Cloud is ephemeral. The guide does not promise persistence.

## Known limitations

- Browser/UI navigation and chart rendering were not verified because the local browser connection was refused in this environment.
- No Git repository or remote exists in the project folder. GitHub CLI is unavailable and no account authentication was detected.
- No license has been selected. A license must be chosen before public publication; no `LICENSE` file or commit has been created.
- The project has not been deployed. There is no live URL.
- The educational app is not validated for GxP, clinical decision-making or real regulatory reporting.
