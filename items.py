"""
Library item hierarchy.

Demonstrates:
- ABSTRACTION: LibraryItem is an abstract base class (ABC) that defines a
  contract every item type must follow.
- INHERITANCE: Book, DVD, and Magazine all inherit from LibraryItem.
- POLYMORPHISM: each subclass overrides describe() and late_fee_per_day()
  so the same method call behaves differently depending on the object.
- ENCAPSULATION: internal state (like _is_checked_out) is protected and
  only modified through controlled methods/properties.
"""

from abc import ABC, abstractmethod
from itertools import count


class LibraryItem(ABC):
    """Abstract base class for anything that can live in the library."""

    _id_counter = count(1)  # shared across all subclasses

    def __init__(self, title: str, year: int):
        self._item_id = next(LibraryItem._id_counter)
        self._title = title
        self._year = year
        self._is_checked_out = False  # encapsulated state

    # ---- Encapsulated properties (controlled access to private state) ----
    @property
    def item_id(self) -> int:
        return self._item_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def is_checked_out(self) -> bool:
        return self._is_checked_out

    def check_out(self) -> None:
        self._is_checked_out = True

    def check_in(self) -> None:
        self._is_checked_out = False

    # ---- Abstract methods: every subclass MUST implement these ----
    @abstractmethod
    def describe(self) -> str:
        """Return a human-readable description of the item."""
        raise NotImplementedError

    @abstractmethod
    def late_fee_per_day(self) -> float:
        """Return the late fee (in currency units) charged per overdue day."""
        raise NotImplementedError

    def status(self) -> str:
        return "Checked out" if self._is_checked_out else "Available"

    def __str__(self) -> str:
        return f"[{self._item_id}] {self.describe()} - {self.status()}"


class Book(LibraryItem):
    def __init__(self, title: str, year: int, author: str, pages: int):
        super().__init__(title, year)
        self._author = author
        self._pages = pages

    def describe(self) -> str:
        return f"'{self._title}' by {self._author} ({self._year}), {self._pages}p [Book]"

    def late_fee_per_day(self) -> float:
        return 0.25


class DVD(LibraryItem):
    def __init__(self, title: str, year: int, director: str, runtime_minutes: int):
        super().__init__(title, year)
        self._director = director
        self._runtime_minutes = runtime_minutes

    def describe(self) -> str:
        return (f"'{self._title}' dir. {self._director} ({self._year}), "
                f"{self._runtime_minutes} min [DVD]")

    def late_fee_per_day(self) -> float:
        return 1.00


class Magazine(LibraryItem):
    def __init__(self, title: str, year: int, issue_number: int):
        super().__init__(title, year)
        self._issue_number = issue_number

    def describe(self) -> str:
        return f"'{self._title}' Issue #{self._issue_number} ({self._year}) [Magazine]"

    def late_fee_per_day(self) -> float:
        return 0.10
