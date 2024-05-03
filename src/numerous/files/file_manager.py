"""Interface for file management operations."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

StrOrPath = Path | str

class FileManager(ABC):

    """
    Abstract Interface for file management operations.

    This class provides a structured interface for handling files, including
    methods for reading, writing, and deleting files. Implementations should
    provide specific mechanisms for these operations.
    """

    @abstractmethod
    def put(self, src: StrOrPath, dst: str ) -> None:
        """
        Upload a file to a path.

        Args:
            src: Source file path.
            dst: Destination file path.

        """
        ...

    @abstractmethod
    def remove(self, path: str) -> None:
        """
        Remove a file at a path.

        Args:
            path: File path to remove.

        """
        ...

    @abstractmethod
    def list(self, path: str | None) -> List[str]:
        """
        List files at a path.

        Args:
            path: Path to list files from.

        """
        ...

    @abstractmethod
    def move(self, src: str, dst: str) -> None:
        """
        Move a file from a source to a destination.

        Args:
            src: Source file path.
            dst: Destination file path.

        """
        ...

    @abstractmethod
    def copy(self, src: str, dst: str) -> None:
        """
        Copy a file from a source to a destination.

        Args:
            src: Source file path.
            dst: Destination file path.

        """
        ...

    @abstractmethod
    def get(self, src: str, dst: Path|str) -> None:
        """
        Download a file from a source to a destination.

        Args:
            src: Source file path.
            dst: Destination file path.

        """
        ...
