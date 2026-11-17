from database.models import FollowUp

def create_follow_up(session, case_id, data):
    if not str(data.get("missing_information") or "").strip():
        raise ValueError("Describe the missing information before creating a follow-up.")
    item=FollowUp(case_id=case_id, **data)
    session.add(item); session.commit(); return item

def update_follow_up(session, follow_up, data):
    allowed={"missing_information","questions","date_sent","response_date","response_received","status","comments"}
    if "missing_information" in data and not str(data["missing_information"] or "").strip():
        raise ValueError("Missing information cannot be blank.")
    for key,value in data.items():
        if key in allowed: setattr(follow_up,key,value)
    session.commit(); return follow_up
