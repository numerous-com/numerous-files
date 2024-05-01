"""Numerous files module."""
__version__ = "0.0.1"

import os

from numerous.files.aws_s3 import FileManager as AwsS3
from numerous.files.memory import FileManager as Memory


def file_manager_factory(**kwargs:dict[str,str]) -> AwsS3|Memory:
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
        env_var_aws_access_key = str(kwargs.get("aws_access_key_id",
                                                "NUMEROUS_FILES_AWS_ACCESS_KEY"))
        env_var_aws_secret_key = str(
            kwargs.get("aws_secret_access_key", "NUMEROUS_FILES_AWS_SECRET_KEY"))
        env_var_bucket = str(
            kwargs.get("bucket", "NUMEROUS_FILES_BUCKET"))
        env_var_base_prefix = str(kwargs.get(
            "base_prefix", "NUMEROUS_FILES_BASE_PREFIX"))

        # Get the credentials from the environment.
        if env_var_aws_access_key in os.environ \
                and env_var_aws_secret_key in os.environ:
            credentials = {
                "aws_access_key_id": os.environ[env_var_aws_access_key],
                "aws_secret_access_key": os.environ[env_var_aws_secret_key],
            }
        else:
            credentials = None
        # If the credentials are not in the environment,
        # set them to None so the aws client will use default auth.

        # Get the bucket from the environment.
        bucket = os.getenv(env_var_bucket, "numerous-files")
        # Get the base prefix from the environment.
        base_prefix = os.environ.get(env_var_base_prefix, "files")

        env_params = {
            "bucket": bucket,
            "base_prefix": base_prefix,
        }
        env_params.update(kwargs) # type: ignore[arg-type]

        return AwsS3(bucket=env_params["bucket"],
                     base_prefix=env_params["base_prefix"], credentials=credentials)

    err_str = f"Unknown file manager type {file_manager}"
    raise ValueError(err_str)
