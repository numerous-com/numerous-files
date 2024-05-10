from pathlib import Path
from typing import Generator

import pytest
from numerous.files.local import FileManager


@pytest.fixture()
def test_file_create() -> Generator[Path, None, None]:

    path_to_file = Path("test.txt")

    with Path.open(path_to_file, "w") as f:
        f.write("Hello World!")
    yield path_to_file
    Path.unlink(path_to_file)


def test_file_manager_create() -> None:

    file_manager = FileManager() # noqa: F841

def test_file_put(test_file_create: str) -> None:

    file_manager = FileManager()

    file_manager.put(test_file_create, "tests/test_memory_filemanager.py")

def test_file_remove(test_file_create: str) -> None:

    file_manager = FileManager()

    upload_path = "tests/test_memory_filemanager.py"

    file_manager.put(test_file_create, upload_path)
    file_manager.remove(upload_path)

def test_file_list(test_file_create: str) -> None:

    file_manager = FileManager()

    upload_path = "tests/test_memory_filemanager.py"

    file_manager.put(test_file_create, upload_path)
    results = file_manager.list("tests/")
    # Replace \\ with / for Windows compatibility
    results = [r.replace("\\", "/") for r in results]
    assert upload_path in results

def test_file_move(test_file_create: str) -> None:

    file_manager = FileManager()

    upload_path = "tests/test_memory_filemanager.py"

    file_manager.put(test_file_create, upload_path)
    file_manager.move(upload_path, "tests/test_memory_filemanager2.py")

    results = file_manager.list("tests/")
    # Replace \\ with / for Windows compatibility
    results = [r.replace("\\", "/") for r in results]

    assert "tests/test_memory_filemanager2.py" in results
    assert upload_path not in results

def test_file_copy(test_file_create: str) -> None:

    file_manager = FileManager()

    upload_path = "tests/test_memory_filemanager.py"

    file_manager.put(test_file_create, upload_path)
    file_manager.copy(upload_path, "tests/test_memory_filemanager2.py")

    file_manager.list("tests/")

    results = file_manager.list("tests/")
    # Replace \\ with / for Windows compatibility
    results = [r.replace("\\", "/") for r in results]

    assert "tests/test_memory_filemanager2.py" in results
    assert upload_path in results

def test_file_get(test_file_create: str) -> None:

    file_manager = FileManager()

    upload_path = "tests/test_memory_filemanager.py"

    file_manager.put(test_file_create, upload_path)
    file_manager.get(upload_path, "test_memory_filemanager.py")

    with Path.open(Path("test_memory_filemanager.py")) as f:
        assert f.read() == "Hello World!"

    Path.unlink(Path("test_memory_filemanager.py"))
