from datetime import date

REQUIRED = {"patient_identifier": "Identifiable patient", "reporter_name": "Identifiable reporter",
            "product": "Suspect medicinal product", "event_verbatim": "Adverse event or reaction"}

def minimum_criteria(data):
    return {label: bool(str(data.get(field) or "").strip()) for field, label in REQUIRED.items()}

def missing_criteria(data):
    return [label for label, passed in minimum_criteria(data).items() if not passed]

def date_issues(data):
    issues = []
    received, onset, end, start, stop = (data.get(k) for k in ("received_date", "event_onset", "event_end", "therapy_start", "therapy_stop"))
    for label, value in (("Event onset", onset), ("Event end", end), ("Therapy start", start), ("Therapy stop", stop)):
        if value and received and value > received: issues.append(f"{label} is after first receipt date")
    if start and stop and stop < start: issues.append("Therapy stop date is before therapy start date")
    if onset and end and end < onset: issues.append("Event end date is before event onset date")
    return issues

def seriousness_from_criteria(criteria, sufficiently_assessed=False):
    """Return an educational classification; absent criteria alone is not enough to conclude non-serious."""
    if criteria:
        return "Serious"
    return "Non-serious" if sufficiently_assessed else "Unknown"
