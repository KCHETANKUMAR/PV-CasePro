from database.models import AuditLog

def log(session, case_id, action, previous=None, new=None, user="Local user", comment=None):
    session.add(AuditLog(case_id=case_id, action=action, previous_value=str(previous) if previous is not None else None,
                         new_value=str(new) if new is not None else None, user=user, comment=comment))
