from django.contrib.auth.hashers import check_password
from rest_framework.test import APITestCase
# from backend.models import Student, Course, Slot, CourseSlot
from backend.models import *
# from backend.serializers import StudentSerializer, AddSlotToCourseSerializer
from backend.serializers import *
from rest_framework.exceptions import ValidationError  # Import ValidationError

class StudentSerializerTest(APITestCase):
    def test_create_student(self):
        data = {
            'roll': 'S12345',
            'name': 'Alice Doe',
            'email': 'alice.doe@example.com',
            'password': 'securepassword987'
        }
        serializer = StudentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        student = serializer.save()  # This will trigger the create method

        # Check if the password was hashed
        self.assertTrue(check_password('securepassword987', student.password))

class AddSlotToCourseSerializerTest(APITestCase):
    def setUp(self):
        # Set up course and slot in the database for testing
        self.course = Course.objects.create(code='CS101', title='Computer Science 101', venue='Main Hall')
        self.slot = Slot.objects.create(id='A1', day=1, start_time='09:00:00', duration=120)  # Correct field setup

    def test_validate_course_code_success(self):
        serializer = AddSlotToCourseSerializer()
        validated_code = serializer.validate_course_code('CS101')
        self.assertEqual(validated_code, 'CS101')

    def test_validate_course_code_failure(self):
        serializer = AddSlotToCourseSerializer()
        with self.assertRaises(ValidationError):
            serializer.validate_course_code('INVALID_CODE')

    def test_validate_slot_id_success(self):
        serializer = AddSlotToCourseSerializer()
        validated_slot = serializer.validate_slot_id('A1')
        self.assertEqual(validated_slot, 'A1')

    def test_validate_slot_id_failure(self):
        serializer = AddSlotToCourseSerializer()
        with self.assertRaises(ValidationError):
            serializer.validate_slot_id('INVALID_SLOT')

    def test_create_course_slot(self):
        data = {'course_code': 'CS101', 'slot_id': 'A1'}
        serializer = AddSlotToCourseSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        course_slot = serializer.save()

        # Check if the association was created
        self.assertIsInstance(course_slot, CourseSlot)
        self.assertEqual(course_slot.course, self.course)
        self.assertEqual(course_slot.slot, self.slot)

    def test_create_course_slot_already_exists(self):
        """Test that attempting to create a CourseSlot when it already exists raises a ValidationError."""
        
        # Create the initial CourseSlot association
        CourseSlot.objects.create(course=self.course, slot=self.slot)
        
        # Attempt to create the same association again
        data = {'course_code': 'CS101', 'slot_id': 'A1'}
        serializer = AddSlotToCourseSerializer(data=data)
        
        with self.assertRaises(ValidationError):  # Check for ValidationError
            serializer.is_valid(raise_exception=True)
            serializer.save()  # This should raise a ValidationError
