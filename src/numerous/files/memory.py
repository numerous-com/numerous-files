"""In Memory File manager."""

import io
from pathlib import Path
from typing import List

from numerous.files.file_manager import FileManager as FileManagerInterface
from numerous.files.file_manager import StrOrPath


class Open:
    def __init__(self, files: dict[str, bytes], filename: str, mode: str = "r") -> None:
        self.filename = filename
        self.mode = mode

        self._files = files
        self.data: io.BytesIO | io.StringIO = io.BytesIO()

    def __enter__(self) -> io.BytesIO | io.StringIO:
        """Open the file."""
        file_content = self._files.get(self.filename, b"")

        # Make a file-like object.
        if self.mode in ("rb", "r+b", "wb", "w+b", "ab", "a+b"):
            self.data = io.BytesIO(file_content)
        elif self.mode in ("r", "r+", "w", "w+", "a", "a+"):
            self.data = io.StringIO(file_content.decode())

        return self.data

    def __exit__(self, *args: object) -> None:
        """Close the file."""
        # Store the file content back in the dictionary.
        if "w" in self.mode or "a" in self.mode:
            if "b" in self.mode:
                self._files[self.filename] = self.data.getvalue() # type: ignore[assignment]
            else:
                self._files[self.filename] = self.data.getvalue().encode() # type: ignore[union-attr]


class FileManager(FileManagerInterface):

    """
    In Memory File manager.

    This class provides an in-memory implementation of the FileManagerInterface.

    Use this class for testing or when you want to store files in memory only.
    This is the default file manager return by the file_manager_factory method.
    """

    def __init__(self) -> None:
        self._files: dict[str, bytes] = {}

    def put(self, src: StrOrPath, dst: str) -> None:
        """
        Upload a file to a path.

        Args:
            src: Source path.
            dst: Destination path.

        """
        with Path.open(Path(src), "rb") as f:
            self._files[dst] = f.read()

    def remove(self, path: str) -> None:
        """
        Remove a file at a path.

        Args:
            path: Path to file.

        """
        del self._files[path]

    def list(self, path: str | None) -> List[str]:
        """
        List files at a path.

        Args:
            path: Path to list files at.

        """
        if path is None:
            return list(self._files.keys())
        return [p for p in self._files if p.startswith(path)]

    def move(self, src: str, dst: str) -> None:
        """
        Move a file from a source to a destination.

        Args:
            src: Source path.
            dst: Destination path.

        """
        self._files[dst] = self._files[src]
        del self._files[src]

    def copy(self, src: str, dst: str) -> None:
        """
        Copy a file from a source to a destination.

        Args:
            src: Source path.
            dst: Destination path.

        """
        self._files[dst] = self._files[src]

    def get(self, src: str, dest: StrOrPath) -> None:
        """
        Download a file from a source to a destination.

        Args:
            src: Source path.
            dest: Destination path.

        """
        with Path.open(Path(dest), "wb") as f:
            f.write(self._files[src])

    def open(self, path: str, mode: str = "r") -> io.BytesIO | io.StringIO:
        """
        Open a file at a path.

        Args:
            path: Path to file.
            mode: Mode to open file in.

        Returns:
            File content.

        """
        if ("r" in mode or "a" in mode) and (path not in self._files):
            err_msg = f"File {path} not found."
            raise FileNotFoundError(err_msg)

        if ("w" in mode or "a" in mode) and (path not in self._files):

            self._files[path] = b""

        return Open(self._files, path, mode) # type: ignore[return-value]
