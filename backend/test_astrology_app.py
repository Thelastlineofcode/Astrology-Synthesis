import unittest
from flask import Flask, json
from api.routes import api_bp

class AstrologyAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(api_bp, url_prefix='/api')
        self.client = self.app.test_client()

    def test_health_endpoint(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'healthy')

    def test_chart_endpoint_missing_data(self):
        response = self.client.post('/api/chart', json={})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_chart_endpoint_valid_data(self):
        birth_data = {
            'year': 1990,
            'month': 8,
            'day': 15,
            'hour': 14,
            'minute': 30,
            'latitude': 29.7604,
            'longitude': -95.3698
        }
        payload = {'birthData': birth_data, 'options': {'zodiacType': 'sidereal', 'ayanamsa': 'LAHIRI', 'houseSystem': 'P', 'includeMinorAspects': False}}
        response = self.client.post('/api/chart', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('chart', data)
        self.assertIn('planets', data['chart'])
        self.assertIn('houses', data['chart'])
        self.assertIn('aspects', data['chart'])

if __name__ == '__main__':
    unittest.main()