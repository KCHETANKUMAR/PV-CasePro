from collections import Counter

def filter_by_received_date(cases, start, end):
    if start is not None and end is not None and start > end:
        raise ValueError("The start date must be on or before the end date.")
    return [
        case for case in cases
        if case.received_date is not None
        and (start is None or case.received_date >= start)
        and (end is None or case.received_date <= end)
    ]

def dashboard_metrics(cases, active_follow_up_case_ids=()):
    case_ids={case.id for case in cases}
    workflow_follow_up_ids={case.id for case in cases if case.status == "Awaiting information"}
    active_follow_up_case_ids=set(active_follow_up_case_ids) & case_ids
    follow_up_case_ids=workflow_follow_up_ids | active_follow_up_case_ids
    awaiting_review=sum(
        case.status != "Closed" and case.human_review_status in {"Not reviewed", "Needs correction"}
        for case in cases
    )
    return {
        "Total cases": len(cases),
        "Initial reports": sum(case.report_type == "Initial" for case in cases),
        "Follow-ups": sum(case.report_type == "Follow-up" for case in cases),
        "Serious": sum(case.seriousness == "Serious" for case in cases),
        "Non-serious": sum(case.seriousness == "Non-serious" for case in cases),
        "Unknown seriousness": sum(case.seriousness not in {"Serious", "Non-serious"} for case in cases),
        "Awaiting review": awaiting_review,
        "QC errors": sum(bool(case.qc_errors) for case in cases),
        "Cases requiring follow-up": len(follow_up_case_ids),
        "Completed": sum(case.status == "Closed" for case in cases),
    }

def category_counts(cases, field, unknown="Unknown"):
    return dict(Counter(getattr(case, field) or unknown for case in cases))

def follow_up_tracking_gaps(cases, active_follow_up_case_ids=()):
    active_ids=set(active_follow_up_case_ids)
    return [case for case in cases if case.status == "Awaiting information" and case.id not in active_ids]

def closed_unreviewed_cases(cases):
    return [case for case in cases if case.status == "Closed" and case.human_review_status != "Reviewed for educational use"]
