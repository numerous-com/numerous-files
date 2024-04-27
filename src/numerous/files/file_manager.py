"""Interface for file management operations."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

StrOrPath = Path | str

class FileManager(ABC):

    """Interface for file management operations."""

    @abstractmethod
    def put(self, src: StrOrPath, dst: str ) -> None:
        """Upload a file to a path."""
        ...

    @abstractmethod
    def remove(self, path: str) -> None:
        """Remove a file at a path."""
        ...

    @abstractmethod
    def list(self, path: str | None) -> List[str]:
        """List files at a path."""
        ...

    @abstractmethod
    def move(self, src: str, dst: str) -> None:
        """Move a file from a source to a destination."""
        ...

    @abstractmethod
    def copy(self, src: str, dst: str) -> None:
        """Copy a file from a source to a destination."""
        ...

    @abstractmethod
    def get(self, src: str, dest: Path|str) -> None:
        """Download a file from a source to a destination."""
        ...
