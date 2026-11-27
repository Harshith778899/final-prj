from app.database import get_db_connection


def save_processing_run(
    old_record_count,
    new_record_count,
    changed_record_count,
    duplicate_count,
    similar_record_count,
    diagnosis_count,
    repaired_count,
    quarantined_count,
    reconciliation_status
):
    connection = get_db_connection()

    if connection is None:
        return None

    cursor = connection.cursor()

    query = """
        INSERT INTO processing_runs (
            old_record_count,
            new_record_count,
            changed_record_count,
            duplicate_count,
            similar_record_count,
            diagnosis_count,
            repaired_count,
            quarantined_count,
            reconciliation_status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        old_record_count,
        new_record_count,
        changed_record_count,
        duplicate_count,
        similar_record_count,
        diagnosis_count,
        repaired_count,
        quarantined_count,
        reconciliation_status
    )

    cursor.execute(query, values)
    connection.commit()

    run_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return run_id


def save_duplicate_records(run_id, duplicates):
    connection = get_db_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    query = """
        INSERT INTO duplicate_records (
            run_id,
            record_id,
            name,
            email,
            city,
            issue
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    for record in duplicates:
        values = (
            run_id,
            record.get("id"),
            record.get("name"),
            record.get("email"),
            record.get("city"),
            "Duplicate record detected"
        )

        cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


def save_repaired_records(run_id, repaired_records):
    connection = get_db_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    query = """
        INSERT INTO repaired_records (
            run_id,
            record_id,
            name,
            email,
            city,
            repair_status
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    for record in repaired_records:
        values = (
            run_id,
            record.get("id"),
            record.get("name"),
            record.get("email"),
            record.get("city"),
            record.get("status", "Repaired")
        )

        cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


def save_quarantined_records(run_id, quarantined_records):
    connection = get_db_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    query = """
        INSERT INTO quarantined_records (
            run_id,
            record_id,
            name,
            email,
            city,
            reason,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    for item in quarantined_records:
        record = item.get("record", {})

        values = (
            run_id,
            record.get("id"),
            record.get("name"),
            record.get("email"),
            record.get("city"),
            item.get("reason"),
            item.get("status", "Quarantined")
        )

        cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


def save_reconciliation_result(run_id, reconciliation):
    connection = get_db_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    query = """
        INSERT INTO reconciliation_results (
            run_id,
            total_records,
            duplicate_ids_count,
            missing_ids_count,
            checks_passed,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        run_id,
        reconciliation.get("total_records", 0),
        len(reconciliation.get("duplicate_ids", [])),
        reconciliation.get("missing_ids", 0),
        reconciliation.get("checks_passed", False),
        reconciliation.get("status", "Fail")
    )

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()