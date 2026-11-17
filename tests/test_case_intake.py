import pytest
from services.case_service import create_case

def test_invalid_case_not_saved(session):
    with pytest.raises(ValueError): create_case(session,{})
    assert session.query(__import__('database.models',fromlist=['Case']).Case).count()==0
