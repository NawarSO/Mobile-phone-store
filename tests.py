from django.test import TestCase
from ..ai_service.predict import evaluate_price

class AIServiceTests(TestCase):
    """Tests for the AI price evaluation service"""
    
    def test_price_evaluation(self):
        """Test basic price evaluation"""
        test_data = {
            'brand': 'Samsung',
            'ram': '8GB',
            'storage': '128GB',
            'screen_size': '6.2'
        }
        
        result = evaluate_price(test_data)
        self.assertIsNotNone(result, "Evaluation returned None")
        self.assertIsInstance(result, (int, float), "Price should be numeric")
        self.assertGreater(result, 100, "Price should be reasonable")

    def test_invalid_input(self):
        """Test with missing fields"""
        with self.assertRaises(KeyError):
            evaluate_price({'brand': 'Samsung'})  # Missing other fields