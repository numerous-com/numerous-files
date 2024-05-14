from pathlib import Path
from typing import Generator

import pytest
from numerous.files.memory import FileManager


@pytest.fixture()
def test_file_create() -> Generator[Path, None, None]:
    path_to_file = Path("test.txt")

    with Path.open(path_to_file, "w") as f:
        f.write("Hello World!")
    yield path_to_file
    Path.unlink(path_to_file)


def test_file_manager_create() -> None:
    file_manager = FileManager()  # noqa: F841


def test_file_put(test_file_create: str) -> None:
    file_manager = FileManager()

    file_manager.put(test_file_create, "tests/text.txt")


def test_file_remove(test_file_create: str) -> None:
    file_manager = FileManager()

    upload_path = "tests/text.txt"

    file_manager.put(test_file_create, upload_path)
    file_manager.remove(upload_path)


def test_file_list(test_file_create: str) -> None:
    file_manager = FileManager()

    upload_path = "tests/text.txt"

    file_manager.put(test_file_create, upload_path)
    results = file_manager.list("tests/")
    assert upload_path in results


def test_file_move(test_file_create: str) -> None:
    file_manager = FileManager()

    upload_path = "tests/text.txt"

    file_manager.put(test_file_create, upload_path)
    file_manager.move(upload_path, "tests/text2.txt")

    file_manager.list("tests/")
    assert "tests/text2.txt" in file_manager.list("tests/")
    assert upload_path not in file_manager.list("tests/")


def test_file_copy(test_file_create: str) -> None:
    file_manager = FileManager()

    upload_path = "tests/tests/text.txt"

    file_manager.put(test_file_create, upload_path)
    file_manager.copy(upload_path, "tests/text2.txt")

    file_manager.list("tests/")
    assert "tests/text2.txt" in file_manager.list("tests/")
    assert upload_path in file_manager.list("tests/")


def test_file_get(test_file_create: str) -> None:
    file_manager = FileManager()

    upload_path = "tests/text.txt"

    file_manager.put(test_file_create, upload_path)
    file_manager.get(upload_path, "text_download.txt")

    with Path.open(Path("text_download.txt")) as f:
        assert f.read() == "Hello World!"

    Path.unlink(Path("text_download.txt"))


def test_file_open_read(test_file_create: str) -> None:
    file_manager = FileManager()

    upload_path = "tests/text.txt"

    file_manager.put(test_file_create, upload_path)

    with file_manager.open(upload_path, "r") as f:
        assert f.read() == "Hello World!"


def test_file_open_write_string() -> None:
    file_manager = FileManager()

    upload_path = "tests/text.txt"

    with file_manager.open(upload_path, "w") as f:
        f.write("Hello Again!") # type: ignore[arg-type]

    with file_manager.open(upload_path) as f:
        assert f.read() == "Hello Again!"
