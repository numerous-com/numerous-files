"""Interface for file management operations."""
from abc import ABC, abstractmethod
from pathlib import Path

StrOrPath = Path | str

class FileManager(ABC):

    """Interface for file management operations."""

    @abstractmethod
    def put(self, dst: StrOrPath, src: StrOrPath) -> None:
        """Upload a file to a path."""
        ...

    @abstractmethod
    def remove(self, path: StrOrPath) -> None:
        """Remove a file at a path."""
        ...

    @abstractmethod
    def list(self, path: StrOrPath | None) -> None:
        """List files at a path."""
        ...

    @abstractmethod
    def move(self, src: StrOrPath, dst: StrOrPath) -> None:
        """Move a file from a source to a destination."""
        ...

    @abstractmethod
    def copy(self, src: StrOrPath, dst: StrOrPath) -> None:
        """Copy a file from a source to a destination."""
        ...

    @abstractmethod
    def get(self, src: StrOrPath, dest: Path|str) -> None:
        """Download a file from a source to a destination."""
        ...
