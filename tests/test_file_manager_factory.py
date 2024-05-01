import os

import pytest
from numerous.files import file_manager_factory
from numerous.files.aws_s3 import FileManager as AwsS3
from numerous.files.memory import FileManager as Memory


def test_file_manager_factory_default() -> None:
    """Test the file manager factory with the default file manager."""
    file_manager = file_manager_factory()
    assert file_manager is not None
    assert isinstance(file_manager, Memory)

def test_file_manager_factory_memory() -> None:
    """Test the file manager factory with the memory file manager."""
    os.environ["NUMEROUS_FILES_BACKEND"] = "INMEMORY"
    file_manager = file_manager_factory()
    assert file_manager is not None
    assert isinstance(file_manager, Memory)

    # Cleanup
    del os.environ["NUMEROUS_FILES_BACKEND"]

def test_file_manager_factory_aws_s3(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the file manager factory with the aws s3 file manager."""
    monkeypatch.setenv("NUMEROUS_FILES_BACKEND", "AWS_S3")
    monkeypatch.setenv("NUMEROUS_FILES_BUCKET", "numerous-files")
    monkeypatch.setenv("NUMEROUS_FILES_BASE_PREFIX", "tests")

    file_manager = file_manager_factory()
    assert file_manager is not None
    assert isinstance(file_manager, AwsS3)
