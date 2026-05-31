import unittest
from app import calculate_success_rate, get_applications_by_status, get_upcoming_actions

class TestBusinessLogic(unittest.TestCase):
    
    def test_calculate_success_rate_empty(self):
        self.assertEqual(calculate_success_rate([]), 0)
    
    def test_calculate_success_rate_all_success(self):
        apps = [
            {'status': 'offer'},
            {'status': 'accepted'},
            {'status': 'offer'}
        ]
        self.assertEqual(calculate_success_rate(apps), 100.0)
    
    def test_calculate_success_rate_mixed(self):
        apps = [
            {'status': 'applied'},
            {'status': 'offer'},
            {'status': 'rejected'},
            {'status': 'accepted'}
        ]
        self.assertEqual(calculate_success_rate(apps), 50.0)
    
    def test_calculate_success_rate_no_success(self):
        apps = [
            {'status': 'applied'},
            {'status': 'reviewing'},
            {'status': 'rejected'}
        ]
        self.assertEqual(calculate_success_rate(apps), 0)
    
    def test_filter_by_status(self):
        apps = [
            {'status': 'applied'},
            {'status': 'offer'},
            {'status': 'applied'},
            {'status': 'rejected'}
        ]
        result = get_applications_by_status(apps, 'applied')
        self.assertEqual(len(result), 2)
    
    def test_filter_by_status_not_found(self):
        apps = [{'status': 'applied'}, {'status': 'offer'}]
        result = get_applications_by_status(apps, 'accepted')
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()