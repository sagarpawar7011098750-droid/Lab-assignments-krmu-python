import json
import logging
from pathlib import Path
try:
    from .book import Book
except ImportError:
    from book import Book

class LibraryInventory:
    def __init__(self, file_path=None):
        # Determine path relative to this file
        if file_path is None:
            # Assumes structure: root/library_manager/inventory.py
            base_path = Path(__file__).resolve().parent.parent
            self.file_path = base_path / 'data' / 'catalog.json'
        else:
            self.file_path = Path(file_path)

        self.books = []
        self.load_books()

    def add_book(self, title, author, isbn):
        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        self.save_books()
        logging.info(f"Book added: {title}")

    def save_books(self):
        data = [book.to_dict() for book in self.books]
        try:
            # Ensure directory exists before saving
            if not self.file_path.parent.exists():
                self.file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            logging.error(f"Failed to save data: {e}")

    def load_books(self):
        if not self.file_path.exists():
            return 
        try:
            with open(self.file_path, 'r') as f:
                content = f.read()
                if not content: return
                data = json.loads(content)
                self.books = [Book(**item) for item in data]
        except (json.JSONDecodeError, IOError):
            logging.error("Data file corrupted or unreadable.")
            self.books = []

    def search_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def search_by_title(self, title):
        results = []
        for book in self.books:
            if title.lower() in book.title.lower():
                results.append(book)
        return results

    def display_all(self):
        if not self.books:
            print("No books in inventory.")
        for book in self.books:
            print(book)