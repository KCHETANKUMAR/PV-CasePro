from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from config import DATABASE_DIR, DATABASE_URL
from database.models import Base

DATABASE_DIR.mkdir(exist_ok=True)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def init_db(target_engine=None):
    active_engine = target_engine or engine
    Base.metadata.create_all(active_engine)  # additive schema initialization; never drops user data
    # Lightweight additive migrations keep existing local databases usable. This intentionally
    # supports only new nullable columns; destructive or type-changing changes need a reviewed migration.
    inspector = inspect(active_engine)
    with active_engine.begin() as connection:
        for table in Base.metadata.sorted_tables:
            if not inspector.has_table(table.name):
                continue
            existing = {column["name"] for column in inspector.get_columns(table.name)}
            for column in table.columns:
                if column.name in existing:
                    continue
                if not column.nullable and column.default is None and column.server_default is None:
                    raise RuntimeError(f"Cannot safely add required column {table.name}.{column.name} without a migration default")
                col_type = column.type.compile(dialect=active_engine.dialect)
                connection.execute(text(f'ALTER TABLE "{table.name}" ADD COLUMN "{column.name}" {col_type}'))

def get_session():
    return SessionLocal()
