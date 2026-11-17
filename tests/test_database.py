from database.models import Case
from services.case_service import create_case

def test_database_creation_and_case_retrieval(session,valid_case_data):
    c=create_case(session,valid_case_data)
    assert session.query(Case).filter_by(case_id=c.case_id).one().patient_identifier=="TRAINING-TEST"

def test_case_update_and_audit(session,valid_case_data):
    from services.case_service import update_status
    c=create_case(session,valid_case_data);update_status(session,c,"Intake review")
    assert c.status=="Intake review"
    logs=session.query(__import__('database.models',fromlist=['AuditLog']).AuditLog).order_by(__import__('database.models',fromlist=['AuditLog']).AuditLog.id).all()
    assert len(logs)==2
    assert logs[-1].previous_value=="New" and logs[-1].new_value=="Intake review" and logs[-1].timestamp is not None
