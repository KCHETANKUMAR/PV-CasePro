def compare_expectedness(training_term, listed_events=None):
    if not listed_events:
        return "Expectedness cannot be assessed — reference safety information not provided."
    if not str(training_term or "").strip():
        return "Expectedness cannot be assessed — training term not selected."
    terms={str(term).strip().casefold() for term in listed_events if str(term).strip()}
    if not terms:
        return "Expectedness cannot be assessed — reference safety information contains no listed events."
    found=str(training_term or "").strip().casefold() in terms
    return "Training term appears in the supplied fictional reference; reviewer assessment required." if found else "Training term is not an exact listed phrase in the supplied fictional reference; reviewer assessment required."
