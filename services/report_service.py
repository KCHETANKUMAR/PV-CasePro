from io import BytesIO, StringIO
import csv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from config import DISCLAIMER

def cases_csv(cases):
    out = StringIO(); w = csv.writer(out); w.writerow([DISCLAIMER]); w.writerow(["Case ID","Type","Received","Country","Patient ID","Product","Event","Seriousness","Outcome","Status"])
    for c in cases: w.writerow([c.case_id,c.report_type,c.received_date,c.country,c.patient_identifier,c.product,c.event_verbatim,c.seriousness,c.outcome,c.status])
    return out.getvalue().encode("utf-8-sig")

def cases_excel(cases):
    wb=Workbook(); ws=wb.active; ws.title="Cases"; ws.append([DISCLAIMER]); ws.append(["Case ID","Type","Received","Country","Patient ID","Product","Event","Seriousness","Outcome","Status"])
    ws[1][0].font=Font(bold=True,color="FFFFFF"); ws[1][0].fill=PatternFill("solid",fgColor="12345A")
    for c in cases: ws.append([c.case_id,c.report_type,str(c.received_date or ""),c.country,c.patient_identifier,c.product,c.event_verbatim,c.seriousness,c.outcome,c.status])
    ws.freeze_panes="A3"; ws.auto_filter.ref=ws.dimensions
    for col in ws.columns: ws.column_dimensions[col[0].column_letter].width=min(40,max(14,max(len(str(cell.value or "")) for cell in col)+2))
    b=BytesIO(); wb.save(b); return b.getvalue()

def dataframe_csv(frame):
    """CSV for auxiliary report tables with the training disclaimer as the first row."""
    from io import StringIO
    out=StringIO(); out.write(DISCLAIMER + "\n"); frame.to_csv(out,index=False)
    return out.getvalue().encode("utf-8-sig")
