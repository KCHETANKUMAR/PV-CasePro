# Database migrations

`database/db.py` performs safe startup migrations for missing tables and new nullable columns. It never drops data. Type changes, renamed columns and non-null additions require a reviewed, explicit migration and a backup plan before release.
