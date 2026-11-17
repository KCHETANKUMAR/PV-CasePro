# User Guide

> **EDUCATIONAL SIMULATION ONLY — NOT FOR REAL-WORLD PHARMACOVIGILANCE REPORTING.** Use fictional data only.

1. **Dashboard:** filter receipt dates and review case counts and charts. Public demo mode defaults to read-only and displays synthetic examples.
2. **Case intake:** enter the patient identifier, reporter identifier, suspect product and event verbatim. Missing required criteria or inconsistent dates prevent saving. Unknown and unreported information should remain explicitly unknown or blank; never guess.
3. **Case assessment:** document seriousness criteria, severity, causality rationale and expectedness. Severity is distinct from seriousness. Human review is required.
4. **Terminology practice:** keep source verbatim separate from fictional training concepts; this is not MedDRA.
5. **Expectedness & RSI:** add a fictional product reference with version, effective date and listed events. Without matching reference information, expectedness cannot be assessed.
6. **Follow-up:** record missing details, neutral questions and response status. Copy the template for human use; the application does not send email.
7. **Narrative:** edit the generated factual draft and save your reviewed text. Unavailable information is labelled rather than invented.
8. **Quality control:** review checklist results, record human reviewer and final educational review status. Automated checks do not approve a case.
9. **Workflow:** record a status transition and optional user/comment; view the audit trail.
10. **Reports:** download CSV, formatted Excel, follow-up/QC reports or individual text summary. Exports carry the educational disclaimer.
11. **Training assessment:** answer 30 questions, view explanations and prior attempts.
12. **Data & backup (local mode only):** download a consistent SQLite snapshot. Demo deletion is available only after confirming the checkbox and removes records marked as demo.

To enable local editing, set `PV_CASEPRO_DEMO_MODE` to `0` in the PowerShell session before starting Streamlit. Public deployments must leave the setting unset or set it to `1`; they expose only read-only browsing and exports. See `STREAMLIT_DEPLOYMENT.md`.
