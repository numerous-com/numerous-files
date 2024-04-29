from pathlib import Path
from typing import Generator

import pytest  # type: ignore[import-not-found]
from numerous.files.aws_s3 import FileManager


@pytest.fixture() # type: ignore[misc]
def test_file_create() -> Generator[Path, None, None]:

    path_to_file = Path("test.txt")

    with Path.open(path_to_file, "w") as f:
        f.write("Hello World!")
    yield path_to_file
    Path.unlink(path_to_file)

@pytest.fixture() # type: ignore[misc]
def file_manager() -> Generator[FileManager, None, None]:

    file_manager = FileManager(bucket="numerous-files", base_prefix="tests")
    yield file_manager

    # Cleanup
    for file in file_manager.list():
        file_manager.remove(file)



def test_file_put(test_file_create: str, file_manager: FileManager) -> None:

    file_manager.put(test_file_create, "tests/test_aws_filemanager.py")

def test_file_remove(test_file_create: str, file_manager: FileManager) -> None:

    upload_path = "tests/test_aws_filemanager.py"

    file_manager.put(test_file_create, upload_path)
    file_manager.remove(upload_path)

def test_file_list(test_file_create: str, file_manager: FileManager) -> None:

    upload_path = "tests/test_aws_filemanager.py"

    file_manager.put(test_file_create, upload_path)
    results = file_manager.list("tests/")

    assert upload_path in results

def test_file_move(test_file_create: str, file_manager: FileManager) -> None:

    upload_path = "tests/test_aws_filemanager.py"

    file_manager.put(test_file_create, upload_path)
    file_manager.move(upload_path, "tests/test_aws_filemanager2.py")

    assert "tests/test_aws_filemanager2.py" in file_manager.list("tests/")
    assert upload_path not in file_manager.list("tests/")

def test_file_copy(test_file_create: str, file_manager: FileManager) -> None:

    upload_path = "tests/test_aws_filemanager.py"

    file_manager.put(test_file_create, upload_path)
    file_manager.copy(upload_path, "tests/test_aws_filemanager2.py")

    assert "tests/test_aws_filemanager2.py" in file_manager.list("tests/")
    assert upload_path in file_manager.list("tests/")

def test_file_get(test_file_create: str, file_manager: FileManager) -> None:

    upload_path = "tests/test_aws_filemanager.py"

    file_manager.put(test_file_create, upload_path)
    file_manager.get(upload_path, "test_aws_filemanager.py")

    with Path.open(Path("test_aws_filemanager.py")) as f:
        assert f.read() == "Hello World!"

    Path.unlink(Path("test_aws_filemanager.py"))