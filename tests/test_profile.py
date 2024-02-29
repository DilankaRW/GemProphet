

import unittest
from profile import profile

class TestProfile(unittest.TestCase):


    def test_profile_update_successful(self):
        result = profile("weera", "444", "weerasinghe@gmail.com", "Weerasinghe")
        print(f"Test profile_update_successful: {result}")
        self.assertTrue(result)


    def test_profile_update_successful(self):
        result = profile("dilanka", "321", "dilankarashmika10@hotmail.com", "Dilanka Weerasinghe")
        print(f"Test profile_update_successful: {result}")
        self.assertTrue(result)

    def test_profile_update_successful(self):
        result = profile("rash", "111", "rashmika@gmail.com", "Rashmika")
        print(f"Test profile_update_successful: {result}")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
