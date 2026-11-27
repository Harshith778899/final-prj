def select_changed_records(old_records, new_records, key="id"):
    """
    Select only new or changed records by comparing
    the new data with the existing data.
    """

    old_data = {
        record.get(key): record
        for record in old_records
        if record.get(key) is not None
    }

    changed_records = []

    for record in new_records:
        record_id = record.get(key)

        # New record
        if record_id not in old_data:
            changed_records.append(record)

        # Existing record but values changed
        elif record != old_data[record_id]:
            changed_records.append(record)

    return changed_records