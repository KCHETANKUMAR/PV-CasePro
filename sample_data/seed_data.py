from datetime import date, timedelta
from database.models import Case, Patient, Reporter, Product, Event, Assessment
from services.audit_service import log

def seed(session):
    if session.query(Case).count(): return 0
    examples = [
        ("Headache","Headache","Non-serious","Recovered","New"),("Nausea","Nausea","Non-serious","Recovering","Intake review"),
        ("Skin rash","Rash","Unknown","Unknown","Awaiting information"),("Dizziness","Dizziness","Non-serious","Recovered","Assessment pending"),
        ("Hospital admission for vomiting","Vomiting","Serious","Recovering","QC pending"),("Headache","Headache","Unknown","Unknown","New"),
        ("Nausea","Nausea","Non-serious","Not recovered","Closed"),("Skin rash","Rash","Non-serious","Recovered","Awaiting information"),
        ("Dizziness","Dizziness","Unknown","Unknown","Assessment pending"),("Headache","Headache","Non-serious","Recovered","Ready for educational review")]
    for i,(event,term,ser,out,status) in enumerate(examples,1):
        c=Case(case_id=f"PVC-DEMO-{i:03d}",report_type="Follow-up" if i in (3,8) else "Initial",received_date=date.today()-timedelta(days=i*3),country="Training country",reporter_type="Healthcare professional",reporter_name=f"Reporter Demo {i}",patient_identifier=f"TRAINING-{i:03d}",age_group="Adult",sex="Not provided",product="Training medicine" if i!=3 else "Unknown",strength="10 mg" if i!=9 else None,dose="10 mg daily",route="Oral",frequency="Daily",indication="Training indication",therapy_start=date.today()-timedelta(days=35),event_verbatim=event,training_term=term,event_onset=date.today()-timedelta(days=i*2),outcome=out,seriousness=ser,serious_criteria="Hospitalisation reported" if ser=="Serious" else None,severity="Moderate",causality="Not assessed",expectedness="Not assessed",status=status,is_demo=True,medical_history="Not provided",concomitant_meds="Not provided",narrative_source="Synthetic training case.")
        session.add(c); session.flush()
        session.add_all([Patient(case_id=c.id,identifier=c.patient_identifier,age_group=c.age_group,sex=c.sex), Reporter(case_id=c.id,reporter_type=c.reporter_type,name=c.reporter_name), Product(case_id=c.id,name=c.product,strength=c.strength), Event(case_id=c.id,verbatim=event,training_term=term,onset=c.event_onset,outcome=out), Assessment(case_id=c.id,seriousness=ser,seriousness_criteria=c.serious_criteria,severity=c.severity)])
        log(session,c.case_id,"Demo case seeded",new=status,comment="Synthetic training data")
    session.commit(); return len(examples)
