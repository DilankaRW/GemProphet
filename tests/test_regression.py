
import unittest
from auth import login
from profile import profile
from prediction import prediction
from signup import signup
from view import view_prediction_history # new

class TestRegression(unittest.TestCase):

    def test_login_regression(self):

        result = login("tharu", "321")
        self.assertTrue(result)

    # Add new features

    def test_view_prediction_history_regression(self):

        history = view_prediction_history()
        self.assertIsInstance(history, list)
        self.assertTrue(len(history) > 0)
