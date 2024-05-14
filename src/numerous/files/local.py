"""Local Folder File manager."""

import shutil
from pathlib import Path
from typing import Any

from numerous.files.file_manager import FileManager as FileManagerInterface
from numerous.files.file_manager import StrOrPath


class Open:
    def __init__(self, filename: Path, mode: str = "r") -> None:
        self.filename = filename
        self.mode = mode
        self.file: None | Any = None

    def __enter__(self): # type: ignore[no-untyped-def] # noqa: ANN204
        """Open the file."""
        self.file = Path.open(self.filename, self.mode)
        return self.file

    def __exit__(self, *args: object) -> None:
        """Close the file."""
        if self.file:
            self.file.close()
            # Assuming the operations that modify the file are done,
            # we save it when closing


class FileManager(FileManagerInterface):

    """
    Local Folder File manager.

    This class provides an local folder implementation of the FileManagerInterface.

    Use this class for testing or when you want to store files in a local folder only.
    """

    def __init__(self, workfolder: StrOrPath = "./tmp") -> None:
        """
        Initialize the LocalFolderFileManager.

        Args:
            workfolder: Path to the working folder.

        """
        self._workfolder = Path(workfolder)

        # Ensure the workfolder exists.
        self._workfolder.mkdir(parents=True, exist_ok=True)

    def put(self, src: StrOrPath, dst: StrOrPath) -> None:
        """
        Upload a file to a path.

        Args:
            src: Source path.
            dst: Destination path.

        """
        _path = self._workfolder / Path(dst)
        # Ensure the parent folder exists.
        _path.parent.mkdir(parents=True, exist_ok=True)

        with Path.open(Path(src), "rb") as f:
            shutil.copyfileobj(f, Path.open(_path, "wb"))

    def remove(self, path: StrOrPath) -> None:
        """
        Remove a file at a path.

        Args:
            path: Path to file.

        """
        _path = self._workfolder / Path(path)
        Path(_path).unlink()

    def list(self, path: StrOrPath | None) -> list[str]:
        """
        List files at a path.

        Args:
            path: Path to list files at.

        """
        _path = self._workfolder if path is None else self._workfolder / Path(path)

        # Make all paths relative to the workfolder.
        return [
            str(p.relative_to(self._workfolder))
            for p in _path.rglob("*")
            if p.is_file()
        ]

    def move(self, src: StrOrPath, dst: StrOrPath) -> None:
        """
        Move a file from a source to a destination.

        Args:
            src: Source path.
            dst: Destination path.

        """
        _src = self._workfolder / Path(src)
        _dst = self._workfolder / Path(dst)
        # Ensure the parent folder exists.
        _dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(_src, _dst)

    def copy(self, src: StrOrPath, dst: StrOrPath) -> None:
        """
        Copy a file from a source to a destination.

        Args:
            src: Source path.
            dst: Destination path.

        """
        _src = self._workfolder / Path(src)
        _dst = self._workfolder / Path(dst)
        # Ensure the parent folder exists.
        _dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(_src, _dst)

    def get(self, src: StrOrPath, dest: StrOrPath) -> None:
        """
        Download a file from a source to a destination.

        Args:
            src: Source path.
            dest: Destination path.

        """
        _src = self._workfolder / Path(src)
        # Ensure the parent folder exists.
        Path(dest).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(_src, dest)

    def open(self, path: StrOrPath, mode: str) -> Open: # type: ignore[override]
        """
        Open a file at a path.

        Args:
            path: Path to file.
            mode: Open mode.

        """
        if "w" in mode or "a" in mode:
            # Ensure the parent folder exists.
            Path(self._workfolder / Path(path)).parent.mkdir(
                parents=True, exist_ok=True,
            )
            # Create empty file if it does not exist.
            Path(self._workfolder / Path(path)).touch()

        return Open(self._workfolder / Path(path), mode)
