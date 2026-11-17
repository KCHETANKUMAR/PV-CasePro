from services.case_service import create_case
from services.assessment_service import compare_expectedness

def test_assessment_fields_are_unknown_by_default(session,valid_case_data):
    c=create_case(session,valid_case_data)
    assert c.seriousness=="Unknown" and c.causality=="Not assessed" and c.expectedness=="Not assessed"

def test_expectedness_requires_a_supplied_reference():
    assert "reference safety information not provided" in compare_expectedness("Headache")
    assert "appears in the supplied" in compare_expectedness("Headache",["headache"])
