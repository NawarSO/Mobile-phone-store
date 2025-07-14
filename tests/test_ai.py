from django.test import TestCase
from api.ai_service.predict import evaluate_price

class AIServiceTest(TestCase):
    def setUp(self):
        """ To Ensure model exists before tests run"""
        from api.ai_service.model import train_model
        train_model()

    def test_price_prediction(self):
        """Must be successful prediction"""
        result = evaluate_price({
            'brand': 'Samsung',
            'ram': '8GB',
            'storage': '128GB',
            'screen_size': '6.2'
        })
        self.assertIsInstance(result, (int, float))
        self.assertGreater(result, 100)  

    def test_invalid_input(self):
        """test missing field handling"""
        with self.assertRaises(KeyError):
            evaluate_price({
                'brand': 'Samsung',
                'ram': '8GB'
                # Missing storage and screen_size
            })