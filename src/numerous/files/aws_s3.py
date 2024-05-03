"""In Memory File manager."""
from typing import Any, Dict, List

import boto3

from numerous.files.file_manager import FileManager as FileManagerInterface
from numerous.files.file_manager import StrOrPath


class FileManager(FileManagerInterface):

    """
    AWS S3 Bucket File manager.

    This class provides an AWS S3 implementation of the FileManagerInterface,
    the files handled by this class are stored in an AWS S3 bucket.

    Set the env variable `NUMEROUS_FILES_BACKEND` to `AWS_S3`
    to get an instance of this class when using the file_manager_factory method.

    To save files on AWS S3 a bucket and a base prefix is needed to be specified
    using the env variables `NUMEROUS_FILES_BUCKET` and `NUMEROUS_FILES_BASE_PREFIX`.

    In order for the file_manager to access your files on aws,
    you need to provide authentication to access AWS.

    If you set the env variables `NUMEROUS_FILES_AWS_ACCESS_KEY`
    and `NUMEROUS_FILES_AWS_SECRET_KEY` with your aws credentials
    they will be used for  authenticatication.

    In case these env variables are not set the client will
    authenticate with the AWS credentials from your environment.

    If needed you can supply the names of the env variables you use to store
    information of the bucket, base_prefix, aws_access and aws_secrets to
    the file_manager_factory method as the following key word arguments:
    bucket, base_prfix, aws_access_key_id, and aws_secret_access_key.

    """

    def __init__(self, bucket: str, base_prefix: str,
                 credentials:Dict[str,Any]|None=None) -> None:
        self._bucket = bucket
        self._base_prefix = base_prefix

        if credentials is not None:
            self._client = boto3.client("s3", **credentials)
        else:
            # Use the default session.
            self._client = boto3.client("s3")


    def put(self, src: StrOrPath, dst: str ) -> None:
        """
        Upload a file to a path.

        Args:
            src: Source path.
            dst: Destination path.

        """
        self._client.upload_file(str(src), self._bucket, f"{self._base_prefix}/{dst}")

    def remove(self, path: str) -> None:
        """
        Remove a file at a path.

        Args:
            path: Path to file.

        """
        self._client.delete_object(Bucket=self._bucket,
                                   Key=f"{self._base_prefix}/{path}")

    def list(self, path: str|None=None) -> List[str]:
        """
        List files at a path.

        Args:
            path: Path to list files at.

        """
        if path is None:
            path = self._base_prefix

        query_result = self._client.list_objects(
            Bucket=self._bucket, Prefix=f"{self._base_prefix}/{path}")
        if "Contents" not in query_result:
            return []
        list_results = [obj["Key"] for obj in query_result["Contents"]]

        # Remove the base prefix from the results. But only first occurence.
        return [result.replace(
            f"{self._base_prefix}/", "", 1) for result in list_results]

    def move(self, src: str, dst: str) -> None:
        """
        Move a file from a source to a destination.

        Args:
            src: Source path.
            dst: Destination path.

        """
        self._client.copy_object(Bucket=self._bucket,
                                 CopySource=f"{self._bucket}/{self._base_prefix}/{src}",
                                 Key=f"{self._base_prefix}/{dst}")
        self._client.delete_object(Bucket=self._bucket,
                                   Key=f"{self._base_prefix}/{src}")

    def copy(self, src: str, dst: str) -> None:
        """
        Copy a file from a source to a destination.

        Args:
            src: Source path.
            dst: Destination path.

        """
        self._client.copy_object(Bucket=self._bucket,
                                 CopySource=f"{self._bucket}/{self._base_prefix}/{src}",
                                 Key=f"{self._base_prefix}/{dst}")

    def get(self, src: str, dest: StrOrPath) -> None:
        """
        Download a file from a source to a destination.

        Args:
            src: Source path.
            dest: Destination path.

        """
        self._client.download_file(self._bucket,
                                   f"{self._base_prefix}/{src}", str(dest))


if __name__ == "__main__":
    list_files = FileManager("numerous-files", "tests").list()
