# test_asgi.py
from django.test import TestCase
from SAMS.asgi import application

class ASGITest(TestCase):
    def test_asgi_application_import(self):
        # This test verifies that the ASGI application can be imported
        self.assertIsNotNone(application, "ASGI application should not be None")