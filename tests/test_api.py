from django.test import TestCase
from rest_framework.test import APIClient

class EvaluationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_successful_evaluation(self):
        response = self.client.post(
            '/phone-evaluations/evaluate/',
            {
                'brand': 'Xiaomi',
                'ram': '8GB',
                'storage': '128GB',
                'screen_size': '6.4'
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('price', response.data)
        self.assertIsInstance(response.data['price'], (int, float))

    def test_missing_field(self):
        response = self.client.post(
            '/phone-evaluations/evaluate/',
            {'brand': 'Samsung', 'ram': '8GB'},  # Missing fields
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)