import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from library_manager.book import Book

class TestBook(unittest.TestCase):
    def test_initialization(self):
        b = Book("Python 101", "Guido", "12345")
        self.assertEqual(b.title, "Python 101")
        self.assertEqual(b.status, "available")

    def test_issue_return(self):
        b = Book("Test Book", "Me", "000")
        b.issue()
        self.assertEqual(b.status, "issued")
        b.return_book()
        self.assertEqual(b.status, "available")

if __name__ == '__main__':
    unittest.main()