QUESTIONS = [
 ("Which four elements support minimum case validity?",["Patient, reporter, suspect product, event","Age, sex, dose, outcome","Country, date, doctor, diagnosis","Product, seriousness, causality, expectedness"],0,"The four minimum criteria are an identifiable patient, identifiable reporter, suspect product and adverse event."),
 ("Does 'severe' automatically mean a case is serious?",["Yes","No","Only for adults","Only after hospitalisation"],1,"Severity describes intensity; seriousness uses regulatory outcome criteria."),
 ("Which is a seriousness criterion?",["Mild discomfort","Hospitalisation","High dose","Long treatment"],1,"Hospitalisation is a seriousness criterion."),
 ("What is an adverse event?",["Any untoward medical occurrence with product use; causality not required","Only a proven reaction","Only a serious effect","An expected symptom"],0,"An adverse event does not require a causal relationship to be established."),
 ("What distinguishes an adverse drug reaction?",["Suspected causal relationship","Always serious","Occurs only in trials","Has known expectedness"],0,"An ADR implies at least a suspected causal relationship."),
 ("If reporter identity is missing, what should happen?",["Invent one","Assess validity as incomplete and seek information","Close automatically","Assume HCP"],1,"Do not invent information; document the gap and seek follow-up."),
 ("How should an unknown outcome be recorded?",["Recovered","Fatal","Unknown/not reported","Not applicable"],2,"Unknown is distinct from a known outcome."),
 ("A serious criterion is not documented. What is appropriate?",["Assume serious","Document uncertainty and seek review","Mark non-serious automatically","Infer from severity"],1,"Seriousness must be supported by documented information."),
 ("What is a neutral follow-up question?",["Please confirm the event end date, if available","Why did you fail to report?","Was this definitely caused by drug?","Please confirm recovery"],0,"Questions should be neutral and avoid leading the reporter."),
 ("Should follow-up email send automatically?",["Yes","No, prepare a template for human use","Only for serious cases","Only in English"],1,"This training application prepares but does not send messages."),
 ("What is verbatim?",["The reporter's original event wording","A coded term","The diagnosis selected by reviewer","A product name"],0,"Preserve source wording separately from a selected concept."),
 ("Is this training vocabulary official MedDRA?",["Yes","No","Only the preferred terms","Only with a license"],1,"The application uses fictional training concepts, not MedDRA."),
 ("Can expectedness be concluded without reference safety information?",["Yes, always","No","Only for common events","Only for non-serious events"],1,"Expectedness requires a supplied reference safety document."),
 ("What does dechallenge describe?",["Event after stopping/reducing product","Event after restarting product","Product indication","Reporter type"],0,"Dechallenge describes event course after product withdrawal or dose reduction."),
 ("What does rechallenge describe?",["Event after re-exposure","Event after first dose","Patient age","Seriousness"],0,"Rechallenge describes event course after product is restarted."),
 ("Should software automatically determine causality?",["Yes","No, structured assessment and rationale require human judgment","Only when chronology fits","Only for known reactions"],1,"This tool records an educational assessment, not a clinical decision."),
 ("What should a narrative do when age is unavailable?",["Estimate it","State not reported","Use average adult age","Omit all patient details"],1,"Narratives must not fabricate missing information."),
 ("What is the purpose of QC?",["Find completeness and consistency issues","Approve all cases automatically","Replace medical review","Assign causality"],0,"QC supports human review by surfacing gaps and inconsistencies."),
 ("What is the appropriate action for conflicting dates?",["Change one silently","Flag discrepancy for clarification","Delete the case","Choose the earlier date"],1,"Unresolved discrepancies should be documented and clarified."),
 ("Which patient identifier is suitable in this demo?",["A real name","A synthetic training ID","A national ID","A hospital number"],1,"Only fictional identifiers should be used in demo records."),
]
QUESTIONS += [
 (f"Which statement about {topic} is best practice?", options, correct, explanation)
 for topic,options,correct,explanation in [
  ("receipt date",["Record when first received","Use event onset","Estimate from narrative","Leave out"],0,"Receipt date is its own case datum."),
  ("event chronology",["Preserve known dates and identify gaps","Assume event began on therapy start","Infer dates from outcome","Ignore contradictions"],0,"Use supported dates and flag missing chronology."),
  ("product strength",["Record as provided; flag missing details","Assume standard strength","Copy another case","Use indication to guess"],0,"Never infer product details."),
  ("case duplication",["Use similarity as a prompt for human check","Merge automatically","Delete the newer case","Ignore possible matches"],0,"Duplicate detection is assistance, not automatic merging."),
  ("workflow audit",["Log status changes and comments","Overwrite status silently","Delete old state","Keep only final status"],0,"Audit history captures transition context."),
  ("patient age group",["Use documented age/group or unknown","Infer from product","Assume adult","Use reporter's age"],0,"Patient facts must come from the source."),
  ("source narrative",["Retain factual source information","Rewrite to add missing details","Remove uncertainty","Convert to diagnosis"],0,"Maintain an accurate source account."),
  ("non-serious assessment",["Document basis and uncertainty","Base on mild severity only","Assume if no hospitalization mentioned","Use outcome alone"],0,"A supported assessment requires available facts and review."),
  ("case closure",["Follow the authorized workflow and review","Close on intake","Close when data are missing","Close automatically after export"],0,"Workflow status should reflect reviewed case progress."),
  ("educational disclaimer",["Keep visible in app and exports","Show only in README","Remove from reports","Use only for sample data"],0,"The simulation disclaimer applies to the application and its exports."),
 ]]

def evaluate_answers(answers):
    if len(answers) != len(QUESTIONS):
        raise ValueError(f"Expected {len(QUESTIONS)} answers; received {len(answers)}.")
    details=[]
    for (question, options, correct, explanation), answer in zip(QUESTIONS, answers):
        is_correct = answer == options[correct]
        details.append({"question": question, "selected": answer, "correct": is_correct, "explanation": explanation})
    return sum(item["correct"] for item in details), details
