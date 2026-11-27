from fastapi import APIRouter, UploadFile, File
import csv
import io

from app.services.validation_service import validate_records
from app.services.incremental_service import select_changed_records
from app.services.duplicate_service import find_duplicates
from app.services.entity_matching_service import (
    find_similar_records,
    calculate_similarity
)
from app.services.diagnosis_service import diagnose_record
from app.services.repair_service import (
    decide_action,
    repair_record,
    quarantine_record
)
from app.services.reconciliation_service import reconcile_records
from app.services.database_service import (
    save_processing_run,
    save_duplicate_records,
    save_repaired_records,
    save_quarantined_records,
    save_reconciliation_result
)

router = APIRouter()


@router.get("/merge/status")
def merge_status():
    return {
        "status": "Merge pipeline ready",
        "stages": [
            "Pre-Merge Validation",
            "Incremental Selection",
            "Duplicate Detection",
            "Entity Matching",
            "Diagnosis",
            "Repair / Quarantine",
            "Reconciliation"
        ]
    }


@router.post("/merge/process")
async def process_merge(
    old_file: UploadFile = File(...),
    new_file: UploadFile = File(...)
):
    # Read uploaded files
    old_content = await old_file.read()
    new_content = await new_file.read()

    # Convert CSV files into records
    old_records = list(
        csv.DictReader(
            io.StringIO(old_content.decode("utf-8"))
        )
    )

    new_records = list(
        csv.DictReader(
            io.StringIO(new_content.decode("utf-8"))
        )
    )

    # Step 1: Pre-Merge Validation
    validation_result = validate_records(
        new_records,
        required_fields=["id", "name", "email", "city"]
    )

    valid_records = validation_result["valid_records"]
    invalid_records = validation_result["invalid_records"]

    # Step 2: Incremental Selection
    changed_records = select_changed_records(
        old_records,
        valid_records,
        key="id"
    )

    # Step 3: Duplicate Detection
    duplicates = find_duplicates(
        changed_records,
        key_fields=["id"]
    )

    # Step 4: Entity Matching
    similar_records = []

    for record in changed_records:
        matches = find_similar_records(
            changed_records,
            record,
            fields=["name", "email", "city"],
            threshold=0.5
        )

        for match in matches:
            if match["record"] != record:
                similar_records.append(match)

    # Step 5: Diagnosis
    diagnosis_results = []

    for duplicate in duplicates:
        diagnosis = diagnose_record(
            duplicate,
            duplicate_found=True,
            source="New CSV"
        )

        diagnosis_results.append(diagnosis)

    # Step 6: Repair / Quarantine
    repaired_records = []
    quarantined_records = []

    for duplicate in duplicates:

        # Find the first occurrence of the same ID
        matching_records = [
            record
            for record in changed_records
            if record.get("id") == duplicate.get("id")
        ]

        # Calculate confidence using record similarity
        if len(matching_records) >= 2:

            reference_record = matching_records[0]

            confidence = calculate_similarity(
                reference_record,
                duplicate,
                fields=["name", "email", "city"]
            )

        else:
            confidence = 0

        # Decide action using confidence
        action = decide_action(
            confidence,
            threshold=0.8
        )

        if action == "Repair":

            repaired = repair_record(
                duplicate,
                {"status": "Repaired"}
            )

            repaired_records.append(repaired)

        else:

            quarantined = quarantine_record(
                duplicate,
                f"Low confidence duplicate. Confidence: {confidence:.2f}"
            )

            quarantined_records.append(quarantined)

    # Step 7: Prepare final records
    final_records = []

    for record in valid_records:

        duplicate_found = any(
            record.get("id") == duplicate.get("id")
            for duplicate in duplicates
        )

        if not duplicate_found:
            final_records.append(record)

    # Add repaired records
    for record in repaired_records:
        final_records.append(record)

    # Step 8: Reconciliation
    reconciliation = reconcile_records(
        final_records,
        key="id"
    )

    # Step 9: Save processing summary to MySQL
    run_id = save_processing_run(
        old_record_count=len(old_records),
        new_record_count=len(new_records),
        changed_record_count=len(changed_records),
        duplicate_count=len(duplicates),
        similar_record_count=len(similar_records),
        diagnosis_count=len(diagnosis_results),
        repaired_count=len(repaired_records),
        quarantined_count=len(quarantined_records),
        reconciliation_status=reconciliation["status"]
    )

    # Step 10: Save detailed duplicate records
    if run_id is not None:
        save_duplicate_records(
            run_id,
            duplicates
        )

    # Step 11: Save repaired records
    if run_id is not None:
        save_repaired_records(
            run_id,
            repaired_records
        )

    # Step 12: Save quarantined records
    if run_id is not None:
        save_quarantined_records(
            run_id,
            quarantined_records
        )

    # Step 13: Save reconciliation result
    if run_id is not None:
        save_reconciliation_result(
            run_id,
            reconciliation
        )

    # Final response
    return {
        "run_id": run_id,

        "old_records": len(old_records),
        "new_records": len(new_records),

        "validation": {
            "valid_records": validation_result["valid_count"],
            "invalid_records": validation_result["invalid_count"],
            "invalid_data": invalid_records
        },

        "changed_records": len(changed_records),
        "duplicates_detected": len(duplicates),
        "similar_records_detected": len(similar_records),
        "diagnosis_count": len(diagnosis_results),
        "repaired_records": len(repaired_records),
        "quarantined_records": len(quarantined_records),

        "reconciliation": reconciliation,

        "changed_data": changed_records,
        "duplicate_data": duplicates,
        "similar_data": similar_records,
        "diagnosis_data": diagnosis_results,
        "repaired_data": repaired_records,
        "quarantined_data": quarantined_records,
        "final_data": final_records
    }