from django.test import RequestFactory, TestCase
from frontend.context_processors import (
    student_roll,
    student_name,
    teacher_id,
    teacher_name,
    admin_id,
    admin_name
)

class ContextProcessorTests(TestCase):
    def setUp(self):
        # Set up a request factory to create a mock request
        self.factory = RequestFactory()

    def test_student_roll(self):
        request = self.factory.get('/')
        request.session = {'student_roll': '12345'}
        context = student_roll(request)
        self.assertEqual(context, {'student_roll': '12345'})

    def test_student_name(self):
        request = self.factory.get('/')
        request.session = {'student_name': 'John Doe'}
        context = student_name(request)
        self.assertEqual(context, {'student_name': 'John Doe'})

    def test_teacher_id(self):
        request = self.factory.get('/')
        request.session = {'teacher_id': 'T6789'}
        context = teacher_id(request)
        self.assertEqual(context, {'teacher_id': 'T6789'})

    def test_teacher_name(self):
        request = self.factory.get('/')
        request.session = {'teacher_name': 'Jane Smith'}
        context = teacher_name(request)
        self.assertEqual(context, {'teacher_name': 'Jane Smith'})

    def test_admin_id(self):
        request = self.factory.get('/')
        request.session = {'admin_id': 'A001'}
        context = admin_id(request)
        self.assertEqual(context, {'admin_id': 'A001'})

    def test_admin_name(self):
        request = self.factory.get('/')
        request.session = {'admin_name': 'Admin User'}
        context = admin_name(request)
        self.assertEqual(context, {'admin_name': 'Admin User'})

    def test_student_roll_none(self):
        request = self.factory.get('/')
        request.session = {}
        context = student_roll(request)
        self.assertEqual(context, {'student_roll': None})

    def test_student_name_none(self):
        request = self.factory.get('/')
        request.session = {}
        context = student_name(request)
        self.assertEqual(context, {'student_name': None})

    def test_teacher_id_none(self):
        request = self.factory.get('/')
        request.session = {}
        context = teacher_id(request)
        self.assertEqual(context, {'teacher_id': None})

    def test_teacher_name_none(self):
        request = self.factory.get('/')
        request.session = {}
        context = teacher_name(request)
        self.assertEqual(context, {'teacher_name': None})

    def test_admin_id_none(self):
        request = self.factory.get('/')
        request.session = {}
        context = admin_id(request)
        self.assertEqual(context, {'admin_id': None})

    def test_admin_name_none(self):
        request = self.factory.get('/')
        request.session = {}
        context = admin_name(request)
        self.assertEqual(context, {'admin_name': None})
