def validate_records(records, required_fields=None):
    """
    Validate incoming records before merge processing.
    Separates valid and invalid records.
    """

    if required_fields is None:
        required_fields = ["id", "name", "email", "city"]

    valid_records = []
    invalid_records = []

    for record in records:
        missing_fields = []

        for field in required_fields:
            value = record.get(field)

            if value is None or str(value).strip() == "":
                missing_fields.append(field)

        if missing_fields:
            invalid_records.append({
                "record": record,
                "reason": "Missing required fields",
                "missing_fields": missing_fields
            })
        else:
            valid_records.append(record)

    return {
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "valid_count": len(valid_records),
        "invalid_count": len(invalid_records)
    }