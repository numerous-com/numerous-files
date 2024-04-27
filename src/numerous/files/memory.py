"""In Memory File manager."""
from pathlib import Path
from typing import List

from numerous.files.file_manager import FileManager as FileManagerInterface
from numerous.files.file_manager import StrOrPath


class FileManager(FileManagerInterface):

    """In Memory File manager."""

    def __init__(self) -> None:
        self._files: dict[str, bytes] = {}

    def put(self, src: StrOrPath, dst: str ) -> None:
        """
        Upload a file to a path.

        Args:
        ----
            src: Source path.
            dst: Destination path.

        """
        with Path.open(Path(src), "rb") as f:
            self._files[dst] = f.read()

    def remove(self, path: str) -> None:
        """
        Remove a file at a path.

        Args:
        ----
            path: Path to file.

        """
        del self._files[path]

    def list(self, path: str|None) -> List[str]:
        """
        List files at a path.

        Args:
        ----
            path: Path to list files at.

        """
        if path is None:
            return list(self._files.keys())
        return [p for p in self._files if p.startswith(path)]

    def move(self, src: str, dst: str) -> None:
        """
        Move a file from a source to a destination.

        Args:
        ----
            src: Source path.
            dst: Destination path.

        """
        self._files[dst] = self._files[src]
        del self._files[src]

    def copy(self, src: str, dst: str) -> None:
        """
        Copy a file from a source to a destination.

        Args:
        ----
            src: Source path.
            dst: Destination path.

        """
        self._files[dst] = self._files[src]

    def get(self, src: str, dest: StrOrPath) -> None:
        """
        Download a file from a source to a destination.

        Args:
        ----
            src: Source path.
            dest: Destination path.

        """
        with Path.open(Path(dest), "wb") as f:
            f.write(self._files[src])


