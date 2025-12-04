import sys
import os
import logging

# 1. Add project root to path so we can import library_manager
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from library_manager.inventory import LibraryInventory
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import library modules. {e}")
    print(f"Checked path: {project_root}")
    sys.exit(1)

# Logging Setup
logging.basicConfig(
    filename='library.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def print_menu():
    print("\n" + "="*30)
    print(" LIBRARY INVENTORY MANAGER")
    print("="*30)
    print("1. Add New Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. Search for Book")
    print("5. View All Books")
    print("6. Exit")
    print("="*30)

def main():
    library = LibraryInventory()

    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ").strip()

        try:
            if choice == '1':
                print("\n--- Add New Book ---")
                title = input("Enter Title: ").strip()
                author = input("Enter Author: ").strip()
                isbn = input("Enter ISBN: ").strip()
                if title and author and isbn:
                    library.add_book(title, author, isbn)
                    print(f"Success: '{title}' added.")
                else:
                    print("Error: All fields are required.")

            elif choice == '2':
                isbn = input("Enter ISBN to issue: ").strip()
                book = library.search_by_isbn(isbn)
                if book:
                    if book.issue():
                        library.save_books()
                        print(f"Success: '{book.title}' issued.")
                    else:
                        print(f"Warning: '{book.title}' is already issued.")
                else:
                    print("Error: Book not found.")

            elif choice == '3':
                isbn = input("Enter ISBN to return: ").strip()
                book = library.search_by_isbn(isbn)
                if book:
                    book.return_book()
                    library.save_books()
                    print(f"Success: '{book.title}' returned.")
                else:
                    print("Error: Book not found.")

            elif choice == '4':
                term = input("Enter Title or ISBN: ").strip()
                found = library.search_by_title(term)
                if not found:
                    res = library.search_by_isbn(term)
                    if res: found = [res]

                if found:
                    print(f"\nFound {len(found)} matches:")
                    for b in found: print(b)
                else:
                    print("No matches found.")

            elif choice == '5':
                print("\n--- Current Catalog ---")
                library.display_all()

            elif choice == '6':
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")

        except Exception as e:
            logging.error(f"Runtime Error: {e}")
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()