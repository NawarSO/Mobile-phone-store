from django.test import TestCase
from api.models import PhoneSpecs
from api.ai_service.predict import evaluate_price

class PhoneModelTest(TestCase):
    def setUp(self):
        self.sample_data = {
            'brand': 'Samsung',
            'ram': '8GB',
            'storage': '128GB',
            'screen_size': '6.2',
            'estimated_price': 850.00
        }
        self.phone = PhoneSpecs.objects.create(**self.sample_data)

    def test_model_creation(self):
        """Test if model saves correctly"""
        from_db = PhoneSpecs.objects.get(id=self.phone.id)
        self.assertEqual(from_db.brand, 'Samsung')
        self.assertEqual(from_db.estimated_price, 850.00)

    def test_price_evaluation_flow(self):
        """Test full evaluation workflow"""
        # Test evaluation
        price = evaluate_price({
            'brand': 'Apple',
            'ram': '6GB',
            'storage': '256GB',
            'screen_size': '6.1'
        })
        self.assertIsInstance(price, (int, float))
        
        
        eval_count = PhoneSpecs.objects.count()
        response = self.client.post(
            '/phone-evaluations/evaluate/',
            data={
                'brand': 'Apple',
                'ram': '6GB',
                'storage': '256GB',
                'screen_size': '6.1'
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PhoneSpecs.objects.count(), eval_count + 1)