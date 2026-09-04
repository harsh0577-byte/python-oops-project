
class LibraryError(Exception):
   
    pass


class ItemNotFoundError(LibraryError):
   
    pass


class ItemNotAvailableError(LibraryError):
    
    pass


class MemberNotFoundError(LibraryError):
  
    pass


class BorrowLimitReachedError(LibraryError):
   
    pass


class ItemNotBorrowedError(LibraryError):
    
    pass
