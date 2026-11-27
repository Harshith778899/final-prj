def find_duplicates(records, key_fields):
    """
    Find duplicate records based on the given key fields.
    """

    seen = set()
    duplicates = []

    for record in records:
        key = tuple(record.get(field) for field in key_fields)

        if key in seen:
            duplicates.append(record)
        else:
            seen.add(key)

    return duplicates