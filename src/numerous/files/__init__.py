"""Numerous files module."""
__version__ = "0.0.1"

import os
from typing import Any

from numerous.files.aws_s3 import FileManager as AwsS3
from numerous.files.memory import FileManager as Memory


def file_manager_factory(**kwargs:dict[str,Any]) -> AwsS3|Memory:
    """
    Create file manager.

    Checks value of ENVIRONMENT variable <NUMEROUS_FILES_BACKEND>
    to determine the file manager to create.

    Args:
    ----
        file_manager: File manager type.
        **kwargs: Keyword arguments to pass to the file

    """
    # Get the file manager type from the environment.
    file_manager = os.environ.get("NUMEROUS_FILES_BACKEND", "INMEMORY")

    if file_manager == "INMEMORY":
        return Memory(**kwargs)

    if file_manager == "AWS_S3":
        # Get the credentials from the environment.
        if "NUMEROUS_FILES_AWS_ACCESS_KEY" in os.environ:
            credentials = {
                "aws_access_key_id": os.environ["NUMEROUS_FILES_AWS_ACCESS_KEY"],
                "aws_secret_access_key": os.environ["NUMEROUS_FILES_AWS_SECRET_KEY"],
            }
        else:
            credentials = None
        # If the credentials are not in the environment,
        # set them to None so the aws client will use default auth.

        # Get the bucket from the environment.
        bucket = os.environ["NUMEROUS_FILES_BUCKET"]
        # Get the base prefix from the environment.
        base_prefix = os.environ.get("NUMEROUS_FILES_BASE_PREFIX", "")

        env_params = {
            "bucket": bucket,
            "base_prefix": base_prefix,
        }
        env_params.update(kwargs) # type: ignore[arg-type]

        return AwsS3(bucket=env_params["bucket"],
                     base_prefix=env_params["base_prefix"], credentials=credentials)

    err_str = f"Unknown file manager type {file_manager}"
    raise ValueError(err_str)
