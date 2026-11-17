from datetime import date
from services.validation_service import missing_criteria, seriousness_from_criteria, date_issues
from services.case_service import possible_duplicates, create_case

def test_four_minimum_criteria(valid_case_data): assert missing_criteria(valid_case_data)==[]
def test_missing_minimum_criteria(): assert len(missing_criteria({}))==4
def test_unknown_distinct_from_missing():
    x={"patient_identifier":"UNKNOWN","reporter_name":"Unknown reporter","product":"Unknown product","event_verbatim":"Unknown reaction"}
    assert not missing_criteria(x)
def test_seriousness_classification():
    assert seriousness_from_criteria(["Hospitalisation"])=="Serious"
    assert seriousness_from_criteria([])=="Unknown"
    assert seriousness_from_criteria([],sufficiently_assessed=True)=="Non-serious"
def test_date_validation(valid_case_data):
    valid_case_data["event_onset"]=date(2025,3,4)
    assert date_issues(valid_case_data)
def test_duplicate_assistance(session,valid_case_data):
    c=create_case(session,valid_case_data)
    assert c in possible_duplicates(session,valid_case_data)
