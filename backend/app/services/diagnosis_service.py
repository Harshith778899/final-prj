def diagnose_record(record, duplicate_found=False, source=None):
    """
    Identify possible causes of a data-quality issue.
    """

    issues = []

    if duplicate_found:
        issues.append("Duplicate record detected")

    if source:
        issues.append(f"Source: {source}")

    missing_fields = []

    for field, value in record.items():
        if value is None or str(value).strip() == "":
            missing_fields.append(field)

    if missing_fields:
        issues.append(
            f"Missing fields: {', '.join(missing_fields)}"
        )

    if not issues:
        issues.append("No major issue detected")

    return {
        "record": record,
        "issues": issues,
        "issue_count": len(issues)
    }