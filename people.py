
from itertools import count


class Person:
    _id_counter = count(1)

    def __init__(self, name: str, email: str):
        self._person_id = next(Person._id_counter)
        self._name = name
        self._email = email

    @property
    def person_id(self) -> int:
        return self._person_id

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return f"{self._name} <{self._email}>"


class Member(Person):
    BORROW_LIMIT = 3

    def __init__(self, name: str, email: str):
        super().__init__(name, email)
        self._borrowed_item_ids: list[int] = []

    @property
    def borrowed_item_ids(self) -> list[int]:
        return list(self._borrowed_item_ids)  # return a copy: protects internal list

    def can_borrow(self) -> bool:
        return len(self._borrowed_item_ids) < self.BORROW_LIMIT

    def add_borrowed(self, item_id: int) -> None:
        self._borrowed_item_ids.append(item_id)

    def remove_borrowed(self, item_id: int) -> None:
        self._borrowed_item_ids.remove(item_id)

    def __str__(self) -> str:
        return f"Member #{self.person_id}: {self.name} ({len(self._borrowed_item_ids)} borrowed)"


class Librarian(Person):
   

    def __init__(self, name: str, email: str, employee_code: str):
        super().__init__(name, email)
        self._employee_code = employee_code

    def __str__(self) -> str:
        return f"Librarian #{self.person_id}: {self.name} [{self._employee_code}]"
