import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

@pytest.fixture
def session(tmp_path):
    engine=create_engine(f"sqlite:///{tmp_path/'test.db'}")
    Base.metadata.create_all(engine); s=sessionmaker(bind=engine,expire_on_commit=False)()
    yield s; s.close(); engine.dispose()

@pytest.fixture
def valid_case_data():
    from datetime import date
    return {"report_type":"Initial","received_date":date(2025,3,3),"reporter_name":"Synthetic reporter","patient_identifier":"TRAINING-TEST","product":"Training medicine","event_verbatim":"Headache","event_onset":date(2025,3,1),"outcome":"Recovered"}
