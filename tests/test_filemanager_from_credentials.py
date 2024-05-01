import os
from pathlib import Path
from typing import Generator

import pytest
from numerous.files import file_manager_factory


@pytest.fixture()
def file_text() -> Generator[Path, None, None]:

    path_to_file = Path("test.txt")

    with Path.open(path_to_file, "w") as f:
        f.write("Hello World!")
    yield path_to_file

    Path.unlink(path_to_file)

def test_file_manager_create(file_text: str) -> None:
    os.environ["NUMEROUS_FILES_BACKEND"] = "AWS_S3"
    os.environ["NUMEROUS_FILES_BUCKET"] = "numerous-files-test"
    os.environ["NUMEROUS_FILES_BASE_PREFIX"] = "tests"

    file_manager = file_manager_factory()

    file_manager.put(file_text, "test_aws_filemanager.py")

    file_manager.remove("test_aws_filemanager.py")
