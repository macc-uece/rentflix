from django.test import TestCase

# Create your tests here.

class NaiveTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_naive(self):
        self.assertTrue(True)

