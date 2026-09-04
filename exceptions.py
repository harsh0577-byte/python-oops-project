"""Custom exceptions for the Library Management System."""


class LibraryError(Exception):
    """Base exception for all library-related errors."""
    pass


class ItemNotFoundError(LibraryError):
    """Raised when an item cannot be found in the catalog."""
    pass


class ItemNotAvailableError(LibraryError):
    """Raised when trying to borrow an item that's already checked out."""
    pass


class MemberNotFoundError(LibraryError):
    """Raised when a member ID doesn't exist."""
    pass


class BorrowLimitReachedError(LibraryError):
    """Raised when a member tries to borrow beyond their allowed limit."""
    pass


class ItemNotBorrowedError(LibraryError):
    """Raised when trying to return an item that wasn't borrowed by that member."""
    pass
