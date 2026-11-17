from datetime import date
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from database.db import init_db
from database.models import Base, Case, FollowUp, AuditLog
from modules.training import QUESTIONS, evaluate_answers
from services.backup_service import backup_database
from services.case_service import create_case, update_case, update_status, reset_demo_data
from services.dashboard_service import dashboard_metrics, filter_by_received_date
from services.follow_up_service import create_follow_up, update_follow_up
from services.report_service import dataframe_csv
import pandas as pd
import sqlite3
import pytest

def test_case_edit_updates_normalized_data_and_audit(session, valid_case_data):
    case=create_case(session,valid_case_data)
    update_case(session,case,{"product":"Training medicine B","event_verbatim":"Nausea"})
    assert case.product=="Training medicine B" and case.event_verbatim=="Nausea"
    assert session.query(__import__('database.models',fromlist=['Product']).Product).one().name=="Training medicine B"
    assert session.query(AuditLog).count()==3

def test_follow_up_create_update_persists(session,valid_case_data):
    case=create_case(session,valid_case_data)
    follow=create_follow_up(session,case.id,{"missing_information":"Event end date","questions":"When did it resolve?","status":"Open"})
    update_follow_up(session,follow,{"status":"Response received","response_received":"Not known"})
    assert session.query(FollowUp).one().status=="Response received"

def test_dashboard_metrics_and_date_filter(session,valid_case_data):
    case=create_case(session,valid_case_data)
    assert dashboard_metrics([case],open_followups=2)["Total cases"]==1
    assert dashboard_metrics([case])["Initial reports"]==1
    assert filter_by_received_date([case],date(2025,3,1),date(2025,3,5))==[case]
    assert filter_by_received_date([case],date(2025,3,4),date(2025,3,5))==[]

def test_quiz_scoring_and_attempt_shape():
    answers=[options[correct] for _,options,correct,_ in QUESTIONS]
    score,details=evaluate_answers(answers)
    assert len(QUESTIONS)==30 and score==30 and all(item["correct"] for item in details)
    with pytest.raises(ValueError): evaluate_answers([])

def test_backup_snapshot_is_readable(tmp_path,valid_case_data):
    dbfile=tmp_path/"local.db";engine=create_engine(f"sqlite:///{dbfile}");Base.metadata.create_all(engine)
    session=sessionmaker(bind=engine,expire_on_commit=False)();create_case(session,valid_case_data);session.close()
    image=tmp_path/"backup.db";image.write_bytes(backup_database(dbfile))
    with sqlite3.connect(image) as conn: assert conn.execute("select count(*) from cases").fetchone()[0]==1
    engine.dispose()

def test_reset_requires_confirmation_and_preserves_non_demo(session,valid_case_data):
    from sample_data.seed_data import seed
    assert seed(session)==10
    regular=create_case(session,valid_case_data)
    with pytest.raises(ValueError): reset_demo_data(session,confirmed=False)
    assert reset_demo_data(session,confirmed=True)==10
    assert session.query(Case).count()==1 and session.query(Case).one().id==regular.id

def test_auxiliary_csv_contains_disclaimer():
    content=dataframe_csv(pd.DataFrame([{"case_id":"PVC-000001"}])).decode("utf-8-sig")
    assert content.startswith("EDUCATIONAL SIMULATION ONLY")

def test_additive_schema_upgrade_preserves_existing_row(tmp_path):
    dbfile=tmp_path/"legacy.db";legacy_engine=create_engine(f"sqlite:///{dbfile}")
    case_table=Case.__table__
    old_columns=[column._copy() for column in case_table.columns if column.name not in {"reviewed_narrative","seriousness_rationale"}]
    from sqlalchemy import Table, MetaData
    legacy=Table("cases",MetaData(),*old_columns)
    legacy.create(legacy_engine)
    with legacy_engine.begin() as conn:
        conn.execute(legacy.insert().values(case_id="PVC-000001",report_type="Initial",status="New",seriousness="Unknown",severity="Unknown",causality="Not assessed",expectedness="Not assessed",human_review_status="Not reviewed",is_demo=False))
    init_db(legacy_engine)
    cols={column["name"] for column in inspect(legacy_engine).get_columns("cases")}
    with legacy_engine.connect() as conn: assert conn.execute(__import__('sqlalchemy').text("select count(*) from cases")).scalar_one()==1
    assert {"reviewed_narrative","seriousness_rationale"} <= cols
    legacy_engine.dispose()
