def dataset_uri(bucket: str, zone: str, dataset: str) -> str:
    return f"s3a://{bucket}/{zone}/{dataset}"


def table_name(zone: str, dataset: str) -> str:
    return f"{zone}_{dataset}"
