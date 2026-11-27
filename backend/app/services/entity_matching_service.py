def calculate_similarity(record1, record2, fields):
    """
    Calculate simple similarity between two records.
    Returns a value between 0 and 1.
    """

    if not fields:
        return 0

    matches = 0

    for field in fields:
        value1 = str(record1.get(field, "")).strip().lower()
        value2 = str(record2.get(field, "")).strip().lower()

        if value1 == value2:
            matches += 1

    return matches / len(fields)


def find_similar_records(records, target_record, fields, threshold=0.5):
    """
    Find records that are similar to the target record.
    """

    similar_records = []

    for record in records:
        similarity = calculate_similarity(
            record,
            target_record,
            fields
        )

        if similarity >= threshold:
            similar_records.append({
                "record": record,
                "similarity": similarity
            })

    return similar_records