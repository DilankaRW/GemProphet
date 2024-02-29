import unittest
from auth import login

class TestAuth(unittest.TestCase):

    def test_login_successful(self):
        result = login("tharu", "321")
        print(f"Test login_successful: {result}")
        self.assertTrue(result)

    def test_login_failure(self):
        result = login("tharu", "456")
        print(f"Test login_failure: {result}")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
