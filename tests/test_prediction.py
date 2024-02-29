
import unittest
from prediction import prediction

class TestPrediction(unittest.TestCase):

    def test_prediction_successful(self):
        result = prediction("", "", "1", "", "", "1", "", 2, 2, 2, 5)
        print(f"Test prediction_successful: {result}")
        self.assertEqual(result)

    def test_prediction_empty_fields(self):
        result = prediction("", "", "1", "", "", "", "", 5, 2, 2, 5)
        print(f"Test prediction_empty_fields: {result}")
        self.assertEqual(result)

if __name__ == '__main__':
    unittest.main()
