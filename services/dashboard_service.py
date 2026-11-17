from collections import Counter

def filter_by_received_date(cases, start, end):
    return [case for case in cases if case.received_date is None or start <= case.received_date <= end]

def dashboard_metrics(cases, open_followups=0):
    return {
        "Total cases": len(cases),
        "Initial reports": sum(case.report_type == "Initial" for case in cases),
        "Follow-ups": sum(case.report_type == "Follow-up" for case in cases),
        "Serious": sum(case.seriousness == "Serious" for case in cases),
        "Non-serious": sum(case.seriousness == "Non-serious" for case in cases),
        "Awaiting review": sum(case.human_review_status == "Not reviewed" for case in cases),
        "QC errors": sum(bool(case.qc_errors) for case in cases),
        "Cases requiring follow-up": open_followups,
        "Completed": sum(case.status == "Closed" for case in cases),
    }

def category_counts(cases, field, unknown="Unknown"):
    return dict(Counter(getattr(case, field) or unknown for case in cases))
