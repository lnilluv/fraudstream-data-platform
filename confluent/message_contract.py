REQUIRED_FIELDS = {
    "trans_num",
    "unix_time",
    "cc_num",
    "amt",
    "is_fraud",
}


def validate_transaction_payload(payload: dict) -> None:
    if "data" not in payload or not isinstance(payload["data"], dict):
        raise ValueError("payload must include a data object")

    payload_fields = set(payload["data"].keys())
    missing_fields = REQUIRED_FIELDS - payload_fields
    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise ValueError(f"payload missing required fields: {missing}")
