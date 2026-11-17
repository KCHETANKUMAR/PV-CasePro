from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "pv_casepro.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"
DISCLAIMER = "EDUCATIONAL SIMULATION ONLY — NOT FOR REAL-WORLD PHARMACOVIGILANCE REPORTING."
WORKFLOW_STATUSES = ["New", "Intake review", "Awaiting information", "Assessment pending", "QC pending", "Ready for educational review", "Closed"]
# Fail closed: set PV_CASEPRO_DEMO_MODE=0 explicitly for the owner's local workspace.
DEMO_MODE = os.getenv("PV_CASEPRO_DEMO_MODE", "1").strip().lower() not in {"0", "false", "no"}
