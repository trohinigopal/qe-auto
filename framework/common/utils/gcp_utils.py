from __future__ import annotations

from common.utils.logger import get_logger

LOGGER = get_logger("framework.gcp")


def upload_report_to_gcp(bucket_name: str, local_path: str, blob_name: str) -> None:
    """
    Placeholder utility for GCP upload.
    Add google-cloud-storage implementation in your environment.
    """
    LOGGER.info("GCP upload requested: bucket=%s file=%s blob=%s", bucket_name, local_path, blob_name)
