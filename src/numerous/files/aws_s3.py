"""In Memory File manager."""

import tempfile
from pathlib import Path
from typing import Any, Dict, List

import boto3
from numerous.files.file_manager import FileManager as FileManagerInterface
from numerous.files.file_manager import StrOrPath


class Open:
    def __init__(
        self,
        file_manager: Any, # noqa: ANN401
        filename: str,
        mode: str = "r",
    ) -> None:
        self.file_manager = file_manager
        self.filename = filename
        self.mode = mode
        self.file = None
        self.file_path: None|Path = None

    def __enter__(self): # type: ignore[no-untyped-def] # noqa: ANN204
        """Open the file and return the file object."""
        tempfile_ = tempfile.NamedTemporaryFile(delete=False)
        self.file_path = Path(tempfile_.name)
        tempfile_.close()

        if self.file_manager.exists(self.filename):
            self.file_manager.get(self.filename, self.file_path)
        elif "w" in self.mode:
            Path.touch(self.file_path)
        elif "r" in self.mode:
            err_msg = f"File {self.filename} does not exist."
            raise FileNotFoundError(err_msg)

        self.file = Path.open(self.file_path, self.mode) # type: ignore[assignment]
        return self.file

    def __exit__(self, *args: object) -> None:
        """Close the file and save it if needed."""
        if self.file:
            self.file.close()
            # Assuming the operations that modify the file are done,
            # we save it when closing
            if "w" in self.mode or "a" in self.mode:
                self.file_manager.put(self.file.name, self.filename)
            # Delete the temporary file.
            Path.unlink(self.file.name)


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

    def __init__(
        self, bucket: str, base_prefix: str, credentials: Dict[str, Any] | None = None,
    ) -> None:
        self._bucket = bucket
        self._base_prefix = base_prefix

        if credentials is not None:
            self._client = boto3.client("s3", **credentials)
        else:
            # Use the default session.
            self._client = boto3.client("s3")

    def _wrap_path(self, path: str) -> str:
        if self._base_prefix == "":
            return path
        return f"{self._base_prefix}/{path}"

    def _unwrap_path(self, path: str) -> str:
        if self._base_prefix == "":
            return path
        return path.replace(f"{self._base_prefix}/", "", 1)


    def put(self, src: StrOrPath, dst: str) -> None:
        """
        Upload a file to a path.

        Args:
            src: Source path.
            dst: Destination path.

        """
        self._client.upload_file(str(src), self._bucket, self._wrap_path(dst))

    def remove(self, path: str) -> None:
        """
        Remove a file at a path.

        Args:
            path: Path to file.

        """
        self._client.delete_object(
            Bucket=self._bucket, Key=self._wrap_path(path),
        )

    def list(self, path: str | None = None) -> List[str]:
        """
        List files at a path.

        Args:
            path: Path to list files at.

        """
        if path is None:
            path = self._base_prefix

        query_result = self._client.list_objects(
            Bucket=self._bucket, Prefix=self._wrap_path(path),
        )
        if "Contents" not in query_result:
            return []
        list_results = [obj["Key"] for obj in query_result["Contents"]]

        # Remove the base prefix from the results. But only first occurence.
        return [
            self._unwrap_path(result) for result in list_results
        ]

    def exists(self, path: str) -> bool:
        """
        Check if a file exists at a path.

        Args:
            path: Path to file.

        Returns:
            True if the file exists, False otherwise.

        """
        query_result = self._client.list_objects(
            Bucket=self._bucket, Prefix=self._wrap_path(path),
        )

        return "Contents" in query_result

    def move(self, src: str, dst: str) -> None:
        """
        Move a file from a source to a destination.

        Args:
            src: Source path.
            dst: Destination path.

        """
        self._client.copy_object(
            Bucket=self._bucket,
            CopySource=f"{self._bucket}/"+self._wrap_path(src),
            Key=self._wrap_path(dst),
        )
        self._client.delete_object(
            Bucket=self._bucket, Key=self._wrap_path(src),
        )

    def copy(self, src: str, dst: str) -> None:
        """
        Copy a file from a source to a destination.

        Args:
            src: Source path.
            dst: Destination path.

        """
        self._client.copy_object(
            Bucket=self._bucket,
            CopySource=f"{self._bucket}/"+self._wrap_path(src),
            Key=f"{self._base_prefix}/{dst}",
        )

    def get(self, src: str, dest: StrOrPath) -> None:
        """
        Download a file from a source to a destination.

        Args:
            src: Source path.
            dest: Destination path.

        """
        self._client.download_file(
            self._bucket,
            self._wrap_path(src),
            str(dest),
        )

    def open(self, path: str, mode: str = "r") -> Open:
        """
        Open a file at a path.

        Args:
            path: Path to file.
            mode: Mode to open file in.

        Returns:
            File content.

        """
        return Open(self, path, mode)


if __name__ == "__main__":
    list_files = FileManager("numerous-files", "tests").list()
