from django.test import TestCase
from backend.models import *
from backend.serializers import *

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

# Models tests

class ModelTestCase(TestCase):

    def setUp(self):
        # Create instances to be used in the tests
        self.student = Student.objects.create(roll="CS24MT013", name="John Doe", email="john@example.com")
        self.teacher = Teacher.objects.create(id="T001", name="Dr. Smith", email="smith@example.com")
        self.admin = Admin.objects.create(id="A001", name="Admin User", email="admin@example.com")
        self.course = Course.objects.create(code="CS101", title="Intro to CS", venue="Room 101")
        self.slot = Slot.objects.create(id="S01", day=0, start_time="10:00:00", duration=60)
        self.course_slot = CourseSlot.objects.create(course=self.course, slot=self.slot)
        self.course_teacher = CourseTeacher.objects.create(course=self.course, teacher=self.teacher)
        self.ta = TA.objects.create(student=self.student, course=self.course, teacher=self.teacher)
        self.attendance = Attendance.objects.create(student=self.student, course=self.course, date="2024-11-01", status=1)
        self.student_course = StudentCourse.objects.create(student=self.student, course=self.course)

    def test_student_str(self):
        self.assertEqual(str(self.student), "Student object (CS24MT013)")

    def test_teacher_str(self):
        self.assertEqual(str(self.teacher), "Teacher object (T001)")

    def test_admin_str(self):
        self.assertEqual(str(self.admin), "Admin object (A001)")

    def test_course_str(self):
        self.assertEqual(str(self.course), "CS101 - Intro to CS")

    def test_slot_str(self):
        self.assertEqual(str(self.slot), "S01: 0 - 10:00:00 (60 mins)")

    def test_course_slot_str(self):
        self.assertEqual(str(self.course_slot), "CS101 - Intro to CS - S01: 0 - 10:00:00 (60 mins)")

    def test_course_teacher_str(self):
        self.assertEqual(str(self.course_teacher), "CS101 - Intro to CS - Teacher object (T001)")

    def test_ta_str(self):
        self.assertEqual(str(self.ta), "TA: Student object (CS24MT013) - Course: CS101 - Intro to CS - Under Teacher: Teacher object (T001)")

    def test_attendance_str(self):
        self.assertEqual(str(self.attendance), "Student object (CS24MT013) - CS101 - Intro to CS - 2024-11-01: 1")

    def test_student_course_str(self):
        self.assertEqual(str(self.student_course), "Student object (CS24MT013) enrolled in CS101 - Intro to CS")

    def test_student_unique_email(self):
        # Test unique email constraint for student model
        with self.assertRaises(Exception):
            Student.objects.create(roll="CS24MT014", name="Jane Doe", email="john@example.com")

    def test_teacher_unique_email(self):
        # Test unique email constraint for teacher model
        with self.assertRaises(Exception):
            Teacher.objects.create(id="T002", name="Prof. Johnson", email="smith@example.com")

    def test_admin_unique_email(self):
        # Test unique email constraint for admin model
        with self.assertRaises(Exception):
            Admin.objects.create(id="A002", name="Admin2", email="admin@example.com")

    def test_course_slot_unique_together(self):
        # Test unique_together for course_slot model
        with self.assertRaises(Exception):
            CourseSlot.objects.create(course=self.course, slot=self.slot)

    def test_course_teacher_unique_together(self):
        # Test unique_together for course_teacher model
        with self.assertRaises(Exception):
            CourseTeacher.objects.create(course=self.course, teacher=self.teacher)

    def test_ta_unique_together(self):
        # Test unique_together for TA model
        with self.assertRaises(Exception):
            TA.objects.create(student=self.student, course=self.course, teacher=self.teacher)

    def test_attendance_unique_together(self):
        # Test unique_together for attendance model
        with self.assertRaises(Exception):
            Attendance.objects.create(student=self.student, course=self.course, date="2024-11-01", status=0)

    def test_student_course_unique_together(self):
        # Test unique_together for student_course model
        with self.assertRaises(Exception):
            StudentCourse.objects.create(student=self.student, course=self.course)

    def test_valid_course_slot_creation(self):
        # Test valid creation of course_slot model
        course = Course.objects.create(code="CS102", title="Data Structures", venue="Room 102")
        slot = Slot.objects.create(id="S02", day=1, start_time="14:00:00", duration=120)
        course_slot = CourseSlot.objects.create(course=course, slot=slot)
        self.assertEqual(course_slot.course.code, "CS102")
        self.assertEqual(course_slot.slot.id, "S02")

    def test_valid_attendance_creation(self):
        # Test valid creation of attendance model
        attendance = Attendance.objects.create(student=self.student, course=self.course, date="2024-11-02", status=0)
        self.assertEqual(attendance.student, self.student)
        self.assertEqual(attendance.course, self.course)
        self.assertEqual(attendance.status, 0)


# Model Testing

class StudentModelTest(TestCase):
    def setUp(self):
        # Create a sample student instance
        self.student = Student.objects.create(
            roll='CS24MT013',
            name='John Doe',
            email='johndoe@example.com'
        )
    
    def test_student_str_method(self):
        """Test the string representation of the Student model."""
        self.assertEqual(str(self.student), 'Student object (CS24MT013)')
    
    def test_student_roll_field(self):
        """Test that the roll field is unique and correct."""
        # Verify the roll value
        self.assertEqual(self.student.roll, 'CS24MT013')
        
        # Try creating another student with the same roll number and catch the exception
        with self.assertRaises(Exception):
            Student.objects.create(
                roll='CS24MT013',
                name='Jane Smith',
                email='janesmith@example.com'
            )
    
    def test_student_email_field(self):
        """Test that the email field is unique and valid."""
        # Verify the email value
        self.assertEqual(self.student.email, 'johndoe@example.com')
        
        # Try creating another student with the same email and catch the exception
        with self.assertRaises(Exception):
            Student.objects.create(
                roll='CS24MT014',
                name='Jane Smith',
                email='johndoe@example.com'  # Same email as the first student
            )
    
    def test_student_name_field(self):
        """Test that the name field is properly saved and correct."""
        self.assertEqual(self.student.name, 'John Doe')
    
    def test_student_model_creation(self):
        """Test if the student instance is created correctly."""
        # Create a new student and check that the record was added
        student = Student.objects.create(
            roll='CS24MT015',
            name='Alice Brown',
            email='alicebrown@example.com'
        )
        self.assertEqual(student.roll, 'CS24MT015')
        self.assertEqual(student.name, 'Alice Brown')
        self.assertEqual(student.email, 'alicebrown@example.com')
        self.assertEqual(Student.objects.count(), 2)  # Ensure that two students exist

class TeacherModelTest(TestCase):
    def setUp(self):
        # Create a sample teacher instance
        self.teacher = Teacher.objects.create(
            id='T001',
            name='Dr. Alan Smith',
            email='alansmith@example.com'
        )
    
    def test_teacher_str_method(self):
        """Test the string representation of the Teacher model."""
        self.assertEqual(str(self.teacher), 'Teacher object (T001)')
    
    def test_teacher_id_field(self):
        """Test that the teacher ID is unique and correct."""
        # Verify the ID value
        self.assertEqual(self.teacher.id, 'T001')
        
        # Try creating another teacher with the same ID and catch the exception
        with self.assertRaises(Exception):
            Teacher.objects.create(
                id='T001',
                name='Prof. John Doe',
                email='johndoe@example.com'
            )
    
    def test_teacher_email_field(self):
        """Test that the email field is unique and valid."""
        # Verify the email value
        self.assertEqual(self.teacher.email, 'alansmith@example.com')
        
        # Try creating another teacher with the same email and catch the exception
        with self.assertRaises(Exception):
            Teacher.objects.create(
                id='T002',
                name='Prof. Mary Johnson',
                email='alansmith@example.com'  # Same email as the first teacher
            )
    
    def test_teacher_name_field(self):
        """Test that the name field is properly saved and correct."""
        self.assertEqual(self.teacher.name, 'Dr. Alan Smith')
    
    def test_teacher_model_creation(self):
        """Test if the teacher instance is created correctly."""
        # Create a new teacher and check that the record was added
        teacher = Teacher.objects.create(
            id='T002',
            name='Prof. Jane White',
            email='janewhite@example.com'
        )
        self.assertEqual(teacher.id, 'T002')
        self.assertEqual(teacher.name, 'Prof. Jane White')
        self.assertEqual(teacher.email, 'janewhite@example.com')
        self.assertEqual(Teacher.objects.count(), 2)  # Ensure that two teachers exist

class AdminModelTest(TestCase):
    def setUp(self):
        # Create a sample admin instance
        self.admin = Admin.objects.create(
            id='A001',
            name='Admin One',
            email='adminone@example.com'
        )
    
    def test_admin_str_method(self):
        """Test the string representation of the Admin model."""
        self.assertEqual(str(self.admin), 'Admin object (A001)')
    
    def test_admin_id_field(self):
        """Test that the admin ID is unique and correct."""
        # Verify the ID value
        self.assertEqual(self.admin.id, 'A001')
        
        # Try creating another admin with the same ID and catch the exception
        with self.assertRaises(Exception):
            Admin.objects.create(
                id='A001',
                name='Admin Two',
                email='admintwo@example.com'
            )
    
    def test_admin_email_field(self):
        """Test that the email field is unique and valid."""
        # Verify the email value
        self.assertEqual(self.admin.email, 'adminone@example.com')
        
        # Try creating another admin with the same email and catch the exception
        with self.assertRaises(Exception):
            Admin.objects.create(
                id='A002',
                name='Admin Three',
                email='adminone@example.com'  # Same email as the first admin
            )
    
    def test_admin_name_field(self):
        """Test that the name field is properly saved and correct."""
        self.assertEqual(self.admin.name, 'Admin One')
    
    def test_admin_model_creation(self):
        """Test if the admin instance is created correctly."""
        # Create a new admin and check that the record was added
        admin = Admin.objects.create(
            id='A002',
            name='Admin Two',
            email='admintwo@example.com'
        )
        self.assertEqual(admin.id, 'A002')
        self.assertEqual(admin.name, 'Admin Two')
        self.assertEqual(admin.email, 'admintwo@example.com')
        self.assertEqual(Admin.objects.count(), 2)  # Ensure that two admins exist

class CourseModelTest(TestCase):
    def setUp(self):
        # Create a sample course instance
        self.course = Course.objects.create(
            code='CS101',
            title='Introduction to Computer Science',
            venue='Room 101'
        )
    
    def test_course_str_method(self):
        """Test the string representation of the Course model."""
        self.assertEqual(str(self.course), 'CS101 - Introduction to Computer Science')
    
    def test_course_code_field(self):
        """Test that the course code is unique and correct."""
        # Verify the code value
        self.assertEqual(self.course.code, 'CS101')
        
        # Try creating another course with the same code and catch the exception
        with self.assertRaises(Exception):
            Course.objects.create(
                code='CS101',
                title='Data Structures',
                venue='Room 102'
            )
    
    def test_course_title_field(self):
        """Test that the title field is properly saved and correct."""
        self.assertEqual(self.course.title, 'Introduction to Computer Science')
    
    def test_course_venue_field(self):
        """Test that the venue field is properly saved and correct."""
        self.assertEqual(self.course.venue, 'Room 101')
    
    def test_course_model_creation(self):
        """Test if the course instance is created correctly."""
        # Create a new course and check that the record was added
        course = Course.objects.create(
            code='CS102',
            title='Data Structures',
            venue='Room 102'
        )
        self.assertEqual(course.code, 'CS102')
        self.assertEqual(course.title, 'Data Structures')
        self.assertEqual(course.venue, 'Room 102')
        self.assertEqual(Course.objects.count(), 2)  # Ensure that two courses exist

'''
class SlotModelTest(TestCase):
    def setUp(self):
        # Create a sample slot instance
        self.slot = Slot.objects.create(
            id='A1',
            day=0,  # Monday
            start_time='09:00:00',
            duration=60  # 1 hour
        )
    
    def test_slot_str_method(self):
        """Test the string representation of the Slot model."""
        # Format: "A1: 0 - 09:00:00 (60 mins)"
        self.assertEqual(str(self.slot), 'A1: 0 - 09:00:00 (60 mins)')
    
    def test_slot_id_field(self):
        """Test that the slot id is correct."""
        self.assertEqual(self.slot.id, 'A1')
    
    def test_slot_day_field(self):
        """Test that the day field is saved correctly."""
        # Day 0 should correspond to Monday
        self.assertEqual(self.slot.day, 0)
        
        # Test other day values (1 for Tuesday, 2 for Wednesday, etc.)
        self.slot.day = 2  # Wednesday
        self.slot.save()
        self.assertEqual(self.slot.day, 2)
    
    def test_slot_start_time_field(self):
        """Test that the start time field is correct."""
        self.assertEqual(self.slot.start_time.strftime('%H:%M:%S'), '09:00:00')
    
    def test_slot_duration_field(self):
        """Test that the duration field is correct."""
        self.assertEqual(self.slot.duration, 60)
    
    def test_slot_model_creation(self):
        """Test if the Slot instance is created correctly."""
        # Create a new slot and check that the record was added
        slot = Slot.objects.create(
            id='B2',
            day=1,  # Tuesday
            start_time='10:00:00',
            duration=90  # 1.5 hours
        )
        self.assertEqual(slot.id, 'B2')
        self.assertEqual(slot.day, 1)  # Tuesday
        self.assertEqual(slot.start_time.strftime('%H:%M:%S'), '10:00:00')
        self.assertEqual(slot.duration, 90)
        self.assertEqual(Slot.objects.count(), 2)  # Ensure that two slots exist
    
    def test_invalid_slot_day(self):
        """Test invalid day value for the Slot model."""
        with self.assertRaises(ValueError):
            Slot.objects.create(
                id='C3',
                day=7,  # Invalid day (not in 0-6 range)
                start_time='11:00:00',
                duration=120
            )
    
    def test_invalid_duration(self):
        """Test invalid duration for the Slot model."""
        with self.assertRaises(ValueError):
            Slot.objects.create(
                id='C4',
                day=4,  # Friday
                start_time='14:00:00',
                duration=-30  # Invalid duration (negative value)
            )
'''


