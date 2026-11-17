from services.validation_service import missing_criteria

def narrative(case):
    def val(v): return str(v) if v not in (None, "") else "Not reported."
    age = case.age or case.age_group
    chronology = f"Event onset: {val(case.event_onset)}; event end: {val(case.event_end)}; therapy start: {val(case.therapy_start)}; therapy stop: {val(case.therapy_stop)}."
    return "\n\n".join([
        f"Patient information: Fictional patient {val(case.patient_identifier)}, age/age group {val(age)}, sex {val(case.sex)}.",
        f"Medical history: {val(case.medical_history)}. Concomitant medications: {val(case.concomitant_meds)}.",
        f"Suspect product: {val(case.product)}, strength {val(case.strength)}, dose {val(case.dose)}, route {val(case.route)}, frequency {val(case.frequency)}, indication {val(case.indication)}.",
        f"Adverse event description: Reported verbatim: {val(case.event_verbatim)}. Training concept (not official MedDRA): {val(case.training_term)}.",
        f"Relevant chronology: {chronology}",
        f"Treatment and outcome: Outcome {val(case.outcome)}; dechallenge {val(case.dechallenge)}; rechallenge {val(case.rechallenge)}.",
        f"Seriousness assessment: {val(case.seriousness)}; documented criteria: {val(case.serious_criteria)}. Severity: {val(case.severity)}. Medical review may be required.",
        f"Available clinical information: {val(case.narrative_source)} {val(case.comments)}",
        "Missing information: " + (", ".join(missing_criteria({k:getattr(case,k,None) for k in ('patient_identifier','reporter_name','product','event_verbatim')})) or "No minimum-criteria fields currently missing; other unreported details are identified above.")
    ])
