# Streamlit Community Cloud deployment

## Deployment safety

The app defaults to `PV_CASEPRO_DEMO_MODE=1`, a read-only public experience with Dashboard, Case library, Reports & export, and About. Case intake, assessment edits, quiz writes, workflow, backup, and demo-reset controls are not shown in demo mode. Do not set this flag to `0` on a public deployment.

The SQLite database is initialized locally on the deployment filesystem and populated with synthetic cases. Streamlit Community Cloud storage is ephemeral; a restart or redeploy can reset it. The app does not promise durable records, and public visitors cannot add or edit records in demo mode. No external paid database is required.

## Deploy steps

1. Publish the repository `PV-CasePro` to GitHub after selecting a license and confirming the files intended for public release.
2. Sign in at [Streamlit Community Cloud](https://share.streamlit.io/) and choose **Create app**.
3. Select the GitHub repository, branch `main`, and main file path `app.py`.
4. Use the Python 3.11 runtime if the workspace settings offer a Python version selector. Dependencies are read from `requirements.txt`.
5. Keep `PV_CASEPRO_DEMO_MODE` unset or set it to `"1"` in app secrets. The code defaults to safe read-only mode when the setting is missing.
6. Deploy, then open the generated application URL and verify Dashboard, Case library, Reports & export, navigation and visible disclaimer.

Do not enter any patient or personal information into a public instance. This project is not suitable for real PV operations or regulatory reporting.

## Local full-functionality mode

```powershell
$env:PV_CASEPRO_DEMO_MODE = "0"
streamlit run app.py
```

This enables local intake and editing tools. Use synthetic training data only. Remove the environment variable or set it back to `1` to restore read-only demo mode.

No live deployment URL exists yet. A URL must only be recorded after the app is actually deployed and opened successfully.
