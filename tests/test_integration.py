import unittest
from auth import login
from profile import profile
from prediction import prediction
from signup import signup

class TestIntegration(unittest.TestCase):

    def test_login_signup_profile_prediction(self):

        signup_result = signup("tharu", "321", "tharu@gmail.com", "Tharindu")
        self.assertTrue(signup_result)
        print(f"Signup Result: {signup_result}")


        login_result = login("tharu", "321")
        self.assertTrue(login_result)
        print(f"Login Result: {login_result}")


        profile_update_result = profile("tharu", "tharu@gmail.com", "1234", "Tharindu")
        self.assertTrue(profile_update_result)
        print(f"Profile Update Result: {profile_update_result}")


        prediction_result = prediction("Male", "Yes", "1", "Graduate", "Yes", "1", "Urban", 5000, 2000, 150000, 5)
        self.assertEqual(prediction_result, "Approved")
        print(f"Prediction Result: {prediction_result}")

if __name__ == '__main__':
    unittest.main()
