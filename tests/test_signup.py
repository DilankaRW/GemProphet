
import unittest
from signup import signup

class TestSignUp(unittest.TestCase):

    def test_signup_successful(self):
        result = signup("dilanka", "321", "dilankarashmika10@hotmail.com", "Dilanka Weerasinghe")
        print(f"Test signup_successful: {result}")
        self.assertTrue(result)

    # def test_signup_failure(self):
    #     result = signup("tharu", "45645", "tharugmail.com", "Tharindu")
    #     print(f"Test signup_failure: {result}")
    #     self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
