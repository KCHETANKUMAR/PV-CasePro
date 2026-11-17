import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path

def backup_database(database_path: Path) -> bytes:
    """Create a consistent SQLite snapshot, including committed WAL content."""
    if not database_path.exists():
        raise FileNotFoundError("The application database has not been initialized.")
    with tempfile.TemporaryDirectory(prefix="pv_casepro_backup_") as temp_dir:
        target = Path(temp_dir) / "pv_casepro_backup.db"
        with closing(sqlite3.connect(database_path)) as source, closing(sqlite3.connect(target)) as destination:
            source.backup(destination)
            destination.commit()
        return target.read_bytes()
