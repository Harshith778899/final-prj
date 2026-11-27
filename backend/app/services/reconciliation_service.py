def reconcile_records(records, key="id"):
    """
    Check the final dataset for duplicate keys
    and missing required IDs.
    """

    seen_ids = set()
    duplicate_ids = []
    missing_ids = 0

    for record in records:
        record_id = record.get(key)

        if record_id is None:
            missing_ids += 1
        elif record_id in seen_ids:
            duplicate_ids.append(record_id)
        else:
            seen_ids.add(record_id)

    passed = len(duplicate_ids) == 0 and missing_ids == 0

    return {
        "total_records": len(records),
        "duplicate_ids": duplicate_ids,
        "missing_ids": missing_ids,
        "checks_passed": passed,
        "status": "Pass" if passed else "Fail"
    }