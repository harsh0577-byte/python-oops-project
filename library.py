
import json
from datetime import date

from exceptions import (
    ItemNotFoundError,
    ItemNotAvailableError,
    MemberNotFoundError,
    BorrowLimitReachedError,
    ItemNotBorrowedError,
)
from items import Book, DVD, Magazine, LibraryItem
from people import Member


class Library:
    def __init__(self, name: str):
        self._name = name
        self._catalog: dict[int, LibraryItem] = {}
        self._members: dict[int, Member] = {}
        self._due_dates: dict[tuple[int, int], date] = {}  # (member_id, item_id) -> due date

    # ---------------- Catalog management ----------------
    def add_item(self, item: LibraryItem) -> LibraryItem:
        self._catalog[item.item_id] = item
        return item

    def register_member(self, member: Member) -> Member:
        self._members[member.person_id] = member
        return member

    def _get_item(self, item_id: int) -> LibraryItem:
        if item_id not in self._catalog:
            raise ItemNotFoundError(f"No item with id {item_id} in catalog.")
        return self._catalog[item_id]

    def _get_member(self, member_id: int) -> Member:
        if member_id not in self._members:
            raise MemberNotFoundError(f"No member with id {member_id}.")
        return self._members[member_id]

    # ---------------- Core operations ----------------
    def checkout(self, member_id: int, item_id: int, due: date) -> None:
        member = self._get_member(member_id)
        item = self._get_item(item_id)

        if item.is_checked_out:
            raise ItemNotAvailableError(f"'{item.title}' is already checked out.")
        if not member.can_borrow():
            raise BorrowLimitReachedError(
                f"{member.name} has reached the {Member.BORROW_LIMIT}-item borrow limit."
            )

        item.check_out()
        member.add_borrowed(item_id)
        self._due_dates[(member_id, item_id)] = due

    def return_item(self, member_id: int, item_id: int, returned_on: date) -> float:
        """Returns the late fee owed (0.0 if on time)."""
        member = self._get_member(member_id)
        item = self._get_item(item_id)

        if item_id not in member.borrowed_item_ids:
            raise ItemNotBorrowedError(f"{member.name} did not borrow '{item.title}'.")

        due = self._due_dates.pop((member_id, item_id), None)
        item.check_in()
        member.remove_borrowed(item_id)

        if due and returned_on > due:
            days_late = (returned_on - due).days
            return round(days_late * item.late_fee_per_day(), 2)
        return 0.0

    def search(self, keyword: str) -> list[LibraryItem]:
        keyword = keyword.lower()
        return [item for item in self._catalog.values() if keyword in item.title.lower()]

    def available_items(self) -> list[LibraryItem]:
        return [item for item in self._catalog.values() if not item.is_checked_out]

    def all_items(self) -> list[LibraryItem]:
        return list(self._catalog.values())

    def all_members(self) -> list[Member]:
        return list(self._members.values())

    # ---------------- Persistence ----------------
    def save_to_json(self, path: str) -> None:
        data = {
            "name": self._name,
            "items": [],
            "members": [],
        }
        for item in self._catalog.values():
            entry = {
                "id": item.item_id,
                "type": type(item).__name__,
                "title": item.title,
                "checked_out": item.is_checked_out,
            }
            data["items"].append(entry)

        for member in self._members.values():
            entry = {
                "id": member.person_id,
                "name": member.name,
                "type": type(member).__name__,
            }
            # Only Members (not Librarians) track borrowed items.
            if hasattr(member, "borrowed_item_ids"):
                entry["borrowed"] = member.borrowed_item_ids
            data["members"].append(entry)

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def __str__(self) -> str:
        return f"Library '{self._name}' ({len(self._catalog)} items, {len(self._members)} members)"
