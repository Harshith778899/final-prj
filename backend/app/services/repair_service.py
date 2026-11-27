def decide_action(confidence, threshold=0.8):
    """
    Decide whether a record should be repaired
    or moved to quarantine.
    """

    if confidence >= threshold:
        return "Repair"

    return "Quarantine"


def repair_record(record, updates):
    """
    Apply approved updates to a record.
    """

    repaired_record = record.copy()
    repaired_record.update(updates)

    return repaired_record


def quarantine_record(record, reason):
    """
    Store an uncertain record with the reason
    for further review.
    """

    return {
        "record": record,
        "reason": reason,
        "status": "Quarantined"
    }