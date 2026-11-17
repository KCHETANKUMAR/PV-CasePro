from services.case_service import create_case
from services.report_service import cases_csv,cases_excel
from openpyxl import load_workbook
from io import BytesIO

def test_csv_and_excel_exports(session,valid_case_data):
    c=create_case(session,valid_case_data)
    assert b"EDUCATIONAL SIMULATION ONLY" in cases_csv([c])
    data=cases_excel([c]); assert data[:2]==b"PK"
    ws=load_workbook(BytesIO(data),read_only=True).active
    assert ws["A1"].value.startswith("EDUCATIONAL SIMULATION ONLY")
    assert ws["A3"].value==c.case_id
