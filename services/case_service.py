from database.models import Case, Patient, Reporter, Product, Event, Assessment, AuditLog
from services.audit_service import log
from services.validation_service import missing_criteria, date_issues

def next_case_id(session):
    from sqlalchemy import func
    # Monotonic IDs remain unique after records are removed or a transaction rolls back.
    existing = session.query(Case.case_id).filter(Case.case_id.like("PVC-%")).all()
    suffixes = [int(row[0][4:]) for row in existing if row[0][4:].isdigit()]
    return f"PVC-{max(suffixes, default=0)+1:06d}"

def create_case(session, data, is_demo=False):
    missing = missing_criteria(data)
    if missing: raise ValueError("Missing minimum ICSR criteria: " + ", ".join(missing))
    issues = date_issues(data)
    if issues: raise ValueError("Date validation failed: " + "; ".join(issues))
    case = Case(case_id=data.get("case_id") or next_case_id(session), is_demo=is_demo, **{k:v for k,v in data.items() if k != "case_id"})
    session.add(case); session.flush()
    session.add_all([Patient(case_id=case.id, identifier=case.patient_identifier, age_group=case.age_group, sex=case.sex),
                     Reporter(case_id=case.id, reporter_type=case.reporter_type, name=case.reporter_name, contact=case.reporter_contact),
                     Product(case_id=case.id, name=case.product, strength=case.strength, dose=case.dose, route=case.route, indication=case.indication),
                     Event(case_id=case.id, verbatim=case.event_verbatim, training_term=case.training_term, onset=case.event_onset, outcome=case.outcome),
                     Assessment(case_id=case.id, seriousness=case.seriousness, seriousness_criteria=case.serious_criteria, severity=case.severity, causality=case.causality, expectedness=case.expectedness)])
    log(session, case.case_id, "Case created", new=case.status, comment="Synthetic demonstration data" if is_demo else None)
    session.commit(); return case

def update_status(session, case, new_status, user="Local user", comment=None):
    if new_status == case.status:
        return case
    old = case.status; case.status = new_status
    log(session, case.case_id, "Workflow status changed", old, new_status, user, comment); session.commit()
    return case

def update_case(session, case, data):
    allowed = {"patient_identifier", "reporter_name", "reporter_contact", "product", "strength", "dose", "route", "event_verbatim", "event_onset", "event_end", "outcome", "comments"}
    before = {key: getattr(case, key) for key in allowed if key in data}
    values = {key: value for key, value in data.items() if key in allowed}
    merged = {key: getattr(case, key) for key in allowed}; merged.update(values)
    missing = missing_criteria(merged)
    if missing:
        raise ValueError("Missing minimum ICSR criteria: " + ", ".join(missing))
    issues = date_issues({key: getattr(case, key) for key in ("received_date", "event_onset", "event_end", "therapy_start", "therapy_stop")} | values)
    if issues:
        raise ValueError("Date validation failed: " + "; ".join(issues))
    for key, value in values.items(): setattr(case, key, value)
    patient = session.query(Patient).filter_by(case_id=case.id).one_or_none()
    reporter = session.query(Reporter).filter_by(case_id=case.id).one_or_none()
    product = session.query(Product).filter_by(case_id=case.id).one_or_none()
    event = session.query(Event).filter_by(case_id=case.id).one_or_none()
    if patient:
        patient.identifier=case.patient_identifier
    if reporter:
        reporter.name=case.reporter_name; reporter.contact=case.reporter_contact
    if product:
        product.name=case.product; product.strength=case.strength; product.dose=case.dose; product.route=case.route
    if event:
        event.verbatim=case.event_verbatim; event.onset=case.event_onset; event.outcome=case.outcome
    for key, old in before.items():
        if old != values[key]: log(session, case.case_id, f"Case field updated: {key}", old, values[key])
    session.commit()
    return case

def possible_duplicates(session, data):
    q = session.query(Case)
    if data.get("patient_identifier"): q = q.filter(Case.patient_identifier == data["patient_identifier"])
    elif data.get("event_verbatim"): q = q.filter(Case.event_verbatim.ilike(f"%{data['event_verbatim']}%"))
    else: return []
    return q.limit(10).all()

def reset_demo_data(session, confirmed=False):
    if not confirmed:
        raise ValueError("Explicit confirmation is required before deleting demo data.")
    from database.models import FollowUp, QCReview, AuditLog
    demo=session.query(Case).filter(Case.is_demo.is_(True)).all()
    ids=[case.id for case in demo]; refs=[case.case_id for case in demo]
    if ids:
        for model in (FollowUp,QCReview,Patient,Reporter,Product,Event,Assessment):
            session.query(model).filter(model.case_id.in_(ids)).delete(synchronize_session=False)
        session.query(AuditLog).filter(AuditLog.case_id.in_(refs)).delete(synchronize_session=False)
    count=session.query(Case).filter(Case.is_demo.is_(True)).delete(synchronize_session=False)
    session.commit(); return count
