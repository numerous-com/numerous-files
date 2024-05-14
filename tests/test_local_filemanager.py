import shutil
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


@pytest.fixture()
def file_manager() -> Generator[FileManager, None, None]:
    workfolder = Path("./tmp")

    file_manager = FileManager(workfolder=workfolder)
    yield file_manager

    # Cleanup
    shutil.rmtree(workfolder)


def test_file_put(file_manager: FileManager, test_file_create: str) -> None:

    file_manager.put(test_file_create, "tests/test.txt")


def test_file_remove(file_manager: FileManager, test_file_create: str) -> None:
    upload_path = "tests/test.txt"

    file_manager.put(test_file_create, upload_path)
    file_manager.remove(upload_path)


def test_file_list(file_manager: FileManager, test_file_create: str) -> None:
    upload_path = "tests/test.txt"

    file_manager.put(test_file_create, upload_path)
    results = file_manager.list("tests/")
    # Replace \\ with / for Windows compatibility
    results = [r.replace("\\", "/") for r in results]
    assert upload_path in results


def test_file_move(file_manager: FileManager, test_file_create: str) -> None:
    upload_path = "tests/test.txt"

    file_manager.put(test_file_create, upload_path)
    file_manager.move(upload_path, "tests/test2.txt")

    results = file_manager.list("tests/")
    # Replace \\ with / for Windows compatibility
    results = [r.replace("\\", "/") for r in results]

    assert "tests/test2.txt" in results
    assert upload_path not in results


def test_file_copy(file_manager: FileManager, test_file_create: str) -> None:
    upload_path = "tests/test.txt"

    file_manager.put(test_file_create, upload_path)
    file_manager.copy(upload_path, "tests/test2.txt")

    file_manager.list("tests/")

    results = file_manager.list("tests/")
    # Replace \\ with / for Windows compatibility
    results = [r.replace("\\", "/") for r in results]

    assert "tests/test2.txt" in results
    assert upload_path in results


def test_file_get(file_manager: FileManager, test_file_create: str) -> None:
    upload_path = "tests/test.txt"

    file_manager.put(test_file_create, upload_path)
    file_manager.get(upload_path, "test_download.txt")

    with Path.open(Path("test_download.txt")) as f:
        assert f.read() == "Hello World!"

    Path.unlink(Path("test_download.txt"))


def test_file_open_read(file_manager: FileManager, test_file_create: str) -> None:
    upload_path = "tests/test.txt"

    file_manager.put(test_file_create, upload_path)
    with file_manager.open(upload_path, "r") as f:
        assert f.read() == "Hello World!"


def test_file_open_write(file_manager: FileManager) -> None:
    upload_path = "tests/test.txt"

    with file_manager.open(upload_path, "w") as f:
        f.write("Hello Again!")

    with file_manager.open(upload_path, "r") as f:
        assert f.read() == "Hello Again!"


def test_file_open_append(file_manager: FileManager) -> None:
    upload_path = "tests/test.txt"

    with file_manager.open(upload_path, "w") as f:
        f.write("Hello Again!")

    with file_manager.open(upload_path, "a") as f:
        f.write("Hello Again!")

    with file_manager.open(upload_path, "r") as f:
        assert f.read() == "Hello Again!Hello Again!"


def test_file_open_write_binary(file_manager: FileManager) -> None:
    upload_path = "tests/test.txt"

    with file_manager.open(upload_path, "wb") as f:
        f.write(b"Hello Again!")

    with file_manager.open(upload_path, "rb") as f:
        assert f.read() == b"Hello Again!"
