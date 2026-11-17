from services.case_service import create_case
from services.narrative_service import narrative

def test_narrative_preserves_unknown(session,valid_case_data):
    c=create_case(session,valid_case_data); text=narrative(c)
    assert "Headache" in text and "Not reported" in text and "fictional" in text.lower()
