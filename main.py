
from datetime import date, timedelta

from library import Library
from items import Book, DVD, Magazine
from people import Member, Librarian
from exceptions import LibraryError


def seed_data(library: Library) -> tuple[Member, Member]:
    
    library.add_item(Book("The Hobbit", 1937, "J.R.R. Tolkien", 310))
    library.add_item(Book("Dune", 1965, "Frank Herbert", 412))
    library.add_item(DVD("Inception", 2010, "Christopher Nolan", 148))
    library.add_item(Magazine("National Geographic", 2024, 245))

    alice = library.register_member(Member("Alice Smith", "alice@example.com"))
    bob = library.register_member(Member("Bob Jones", "bob@example.com"))
    library.register_member(Librarian("Carla Diaz", "carla@example.com", "EMP-001"))

    return alice, bob


def run_demo(library: Library, alice: Member, bob: Member) -> None:
    print(f"\n=== {library} ===\n")

    print("-- Full catalog --")
    for item in library.all_items():
        print(" ", item)

    print("\n-- Checking out items --") 
    today = date.today()
    due = today + timedelta(days=14)

    try:
        library.checkout(alice.person_id, 1, due)  
        print(f"{alice.name} checked out item #1 (due {due}).")

        library.checkout(bob.person_id, 3, due)  
        print(f"{bob.name} checked out item #3 (due {due}).")

        
        library.checkout(bob.person_id, 1, due)
    except LibraryError as e:
        print(f"  Expected error: {e}")

    print("\n-- Catalog after checkouts --")
    for item in library.all_items():
        print(" ", item)

    print("\n-- Returning an item late --")
    late_return_date = due + timedelta(days=5)
    fee = library.return_item(alice.person_id, 1, late_return_date)
    print(f"{alice.name} returned item #1 on {late_return_date}. Late fee: ${fee:.2f}")

    print("\n-- Searching for 'dune' --")
    for item in library.search("dune"):
        print(" ", item)

    print("\n-- Member status --")
    for member in library.all_members():
        print(" ", member)

    library.save_to_json("library_data.json")
    print("\nSaved snapshot to library_data.json")


def interactive_menu(library: Library, alice: Member, bob: Member) -> None:
    members_by_name = {m.name.lower(): m for m in (alice, bob)}

    menu = """
--- Library Menu ---
1. List all items
2. Search items
3. Check out an item
4. Return an item
5. List members
0. Exit
"""
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            for item in library.all_items():
                print(" ", item)

        elif choice == "2":
            keyword = input("Search keyword: ").strip()
            results = library.search(keyword)
            if results:
                for item in results:
                    print(" ", item)
            else:
                print("  No matches found.")

        elif choice == "3":
            try:
                item_id = int(input("Item ID to check out: ").strip())
                member_name = input("Member name (alice/bob): ").strip().lower()
                member = members_by_name.get(member_name)
                if not member:
                    print("  Unknown member.")
                    continue
                due = date.today() + timedelta(days=14)
                library.checkout(member.person_id, item_id, due)
                print(f"  Checked out. Due {due}.")
            except LibraryError as e:
                print(f"  Error: {e}")
            except ValueError:
                print("  Please enter a valid item ID.")

        elif choice == "4":
            try:
                item_id = int(input("Item ID to return: ").strip())
                member_name = input("Member name (alice/bob): ").strip().lower()
                member = members_by_name.get(member_name)
                if not member:
                    print("  Unknown member.")
                    continue
                fee = library.return_item(member.person_id, item_id, date.today())
                print(f"  Returned. Late fee: ${fee:.2f}")
            except LibraryError as e:
                print(f"  Error: {e}")
            except ValueError:
                print("  Please enter a valid item ID.")

        elif choice == "5":
            for member in library.all_members():
                print(" ", member)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("  Invalid choice, try again.")


if __name__ == "__main__":
    library = Library("Ajmer Public Library")
    alice, bob = seed_data(library)
    run_demo(library, alice, bob)

    print("\n\nWant to try the interactive menu? (y/n)")
    if input("> ").strip().lower().startswith("y"):
        interactive_menu(library, alice, bob)

