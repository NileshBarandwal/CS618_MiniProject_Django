from django.test import TestCase
from backend.models import *
from backend.views import *
from backend.serializers import *

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from datetime import date
from django.contrib.auth.hashers import make_password
from unittest.mock import patch
import random
import time 
from django.contrib.auth import get_user_model


class APITests(APITestCase):

    def setUp(self):
        # Sample data setup for testing
        self.student = Student.objects.create(roll='12345', name='Test Student', email='student@example.com', password=make_password('password'))
        self.teacher = Teacher.objects.create(id='teacher1', name='Test Teacher', email='teacher@example.com', password=make_password('password'))
        self.course = Course.objects.create(code='COURSE1', title='Sample Course')
        self.admin = Admin.objects.create(id='admin1', name='Test Admin', email='admin@example.com', password=make_password('password'))

    def test_login_student(self):
        # Test login as a student
        url = reverse('login')
        data = {
            'username': self.student.roll,
            'password': 'password',
            'role': 'student'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], 'success')

    def test_login_teacher(self):
        # Test login as a teacher
        url = reverse('login')
        data = {
            'username': self.teacher.id,
            'password': 'password',
            'role': 'teacher'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], 'success')
    
    def test_login_admin(self):
        # Test login as an admin
        url = reverse('login')
        data = {
            'username': self.admin.id,
            'password': 'password',
            'role': 'admin'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], 'success')

    def test_invalid_role(self):
        # Test login with an invalid role
        url = reverse('login')
        data = {
            'username': self.student.roll,
            'password': 'password',
            'role': 'invalid_role'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['status'], 'error')
        self.assertEqual(response.json()['message'], 'Invalid role')
    
    def test_missing_username(self):
        # Test login with a missing username
        url = reverse('login')
        data = {
            'password': 'password',
            'role': 'student'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['status'], 'error')
        self.assertEqual(response.json()['message'], 'Username, password, and role are required')

    def test_invalid_password(self):
        # Test login with an incorrect password
        url = reverse('login')
        data = {
            'username': self.student.roll,
            'password': 'wrongpassword',
            'role': 'student'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['status'], 'error')
        self.assertEqual(response.json()['message'], 'Invalid password')

    def test_missing_password(self):
        # Test login with a missing password
        url = reverse('login')
        data = {
            'username': self.student.roll,
            'role': 'student'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['status'], 'error')
        self.assertEqual(response.json()['message'], 'Username, password, and role are required')

    def test_invalid_json(self):
        # Test login with an invalid JSON body
        url = reverse('login')
        data = "invalid json string"
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['status'], 'error')
        self.assertEqual(response.json()['message'], 'Invalid JSON request body')

    def test_invalid_http_method(self):
        # Test invalid HTTP method (GET instead of POST)
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.json()['status'], 'error')
        self.assertEqual(response.json()['message'], 'Invalid request method')

    # def test_user_not_found(self):
    #     url = reverse('login')
    #     data = {
    #         'username': 'nonexistent_user',
    #         'password': 'password',
    #         'role': 'student'
    #     }
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     self.assertEqual(response.json()['status'], 'error')
    #     self.assertEqual(response.json()['message'], 'Student not found')

    
    def test_login_missing_role(self):
        # Test login with a missing role
        url = reverse('login')
        data = {
            'username': self.student.roll,
            'password': 'password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['status'], 'error')
        self.assertEqual(response.json()['message'], 'Username, password, and role are required')

    def test_get_student_courses_attendance(self):
        # Test retrieving student courses and attendance
        StudentCourse.objects.create(student=self.student, course=self.course)
        url = reverse('get_student_courses_attendance', args=[self.student.roll])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('courses', response.json())

    def test_get_student_course_attendance(self):
        # Test retrieving attendance records for a specific course
        Attendance.objects.create(student=self.student, course=self.course, date='2023-01-01', status=1)
        url = reverse('get_student_course_attendance', args=[self.student.roll, self.course.code])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('attendance_records', response.json())

    def test_get_student_profile(self):
        # Test retrieving the student profile
        url = reverse('get_student_profile', args=[self.student.roll])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], self.student.name)

    def test_update_student_profile(self):
        # Test updating the student profile
        url = reverse('update_student')
        data = {'roll': self.student.roll, 'name': 'Updated Student', 'email': 'updated@example.com'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, 'Updated Student')

    def test_mark_attendances(self):
        # Test marking multiple attendance records
        url = reverse('mark_attendances')
        data = {
            'attendances': [
                {
                    'student_roll': self.student.roll,
                    'course_code': self.course.code,
                    'status': 1,
                    'date_value': '2023-01-01'
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_teacher(self):
        # Test creating a teacher
        url = reverse('create_teacher')
        data = {'id': 'teacher2', 'name': 'New Teacher', 'email': 'newteacher@example.com', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_enroll_student_in_course(self):
        # Test enrolling a student in a course
        url = reverse('enroll_student_in_course')
        data = {'student_roll': self.student.roll, 'course_code': self.course.code}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_enroll_ta(self):
        # Test enrolling a student as a TA
        url = reverse('enroll_ta')
        data = {'student_roll': self.student.roll, 'course_code': self.course.code, 'teacher_id': self.teacher.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_student_valid_data(self):
        # Use a unique roll number to avoid conflicts with existing students
        unique_roll = f"12345_{int(time.time())}"  # Adding timestamp to make the roll number unique
        
        valid_data = {
            'roll': unique_roll,
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'password': 'password123'
        }
        
        response = self.client.post(reverse('create_student'), data=valid_data, format='json')

        # If the response status is 400, print the error response for debugging
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            print("Validation Errors:", response.json())  # This will print validation errors if any
        
        # Assert the status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check the response contains roll, name, and email
        self.assertIn('roll', response.data)
        self.assertIn('name', response.data)
        self.assertIn('email', response.data)

class SwaggerUITestCase(TestCase):

    def setUp(self):
        # Create a user for testing purposes (if login_required is in use)
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123'
        )
        
        # URL for the swagger UI page
        self.url = reverse('swagger_docs')  # Update this with the actual URL name

    def test_swagger_ui_authenticated(self):
        # Log in as the user
        self.client.login(username='testuser', password='password123')
        
        # Access the swagger UI page
        response = self.client.get(self.url)
        
        # Assert that the page loads successfully (status 200)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'swagger.html')  # Check that the correct template is used


# class GetStudentCoursesAttendanceTest(APITestCase):

#     def setUp(self):
#         # Set up a student and related data
#         self.student = Student.objects.create(roll="S12345", name="John Doe", email="john.doe@example.com")
#         self.course = Course.objects.create(code="CS101", title="Computer Science 101", venue="Main Hall")
#         self.student_course = StudentCourse.objects.create(student=self.student, course=self.course)
#         Attendance.objects.create(student=self.student, course=self.course, status=1, date=date.today())  # Add 'date' field

#     def test_get_student_courses_attendance_success(self):
#         """Test retrieving courses and attendance for an existing student"""
#         response = self.client.get(f'/api/students/{self.student.roll}/courses/attendance/')  # Corrected URL
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('courses', response.data)
#         self.assertEqual(len(response.data['courses']), 1)  # Only one course for the student
#         self.assertEqual(response.data['courses'][0]['code'], self.course.code)
#         self.assertEqual(response.data['courses'][0]['attendance'], 100.0)

#     def test_student_not_found(self):
#         """Test that student not found raises 404 error"""
#         response = self.client.get('/api/students/INVALID_ROLL/courses/attendance/')  # Corrected URL
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
#         # Assuming the error message is returned as a JSON response
#         response_data = response.json()  # Use .json() to parse the JSON response
#         self.assertEqual(response_data['error'], 'Student not found, INVALID_ROLL')

#     def test_generic_error(self):
#         """Test that any unexpected error raises a 500 error"""
#         with patch('backend.views.get_student_courses_attendance') as mock_view:
#             mock_view.side_effect = Exception("Unexpected error")
            
#             # Simulate the API call that should cause the exception
#             response = self.client.get('/api/students/12345/courses/attendance/')  # Corrected URL
#             self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            
#             # Optionally, check the response content if your view returns a message on error
#             response_data = response.json()
#             self.assertEqual(response_data['error'], 'Unexpected error')




# class StudentCourseAttendanceTestCase(APITestCase):

    # def setUp(self):
    #     # Sample data setup for testing
    #     self.student = Student.objects.create(roll='12345', name='Test Student', email='student@example.com', password=make_password('password'))
    #     self.teacher = Teacher.objects.create(id='teacher1', name='Test Teacher', email='teacher@example.com', password=make_password('password'))
    #     self.course = Course.objects.create(code='COURSE1', title='Sample Course')
    #     self.admin = Admin.objects.create(id='admin1', name='Test Admin', email='admin@example.com', password=make_password('password'))
        
    #     # Enroll the student in the course
    #     StudentCourse.objects.create(student=self.student, course=self.course)

    #     # Create some attendance records
    #     self.attendance_1 = Attendance.objects.create(student=self.student, course=self.course, date='2023-01-01', status=1)  # Present
    #     self.attendance_2 = Attendance.objects.create(student=self.student, course=self.course, date='2023-01-02', status=0)  # Absent

    # def test_get_student_course_attendance_valid(self):
    #     # Test case for valid student and course
    #     url = reverse('get_student_course_attendance', args=[self.student.roll, self.course.code])
    #     response = self.client.get(url)
        
    #     # Check that the response status is 200 OK
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    #     # Check that the attendance records are correctly returned
    #     self.assertEqual(len(response.json()['attendance_records']), 2)
    #     self.assertEqual(response.json()['student_roll'], self.student.roll)
    #     self.assertEqual(response.json()['course_code'], self.course.code)
        
    #     # Ensure the attendance status matches
    #     attendance_records = response.json()['attendance_records']
    #     self.assertEqual(attendance_records[0]['status'], 1)  # Present
    #     self.assertEqual(attendance_records[1]['status'], 0)  # Absent

    # def test_student_not_found(self):
    #     # Test case for student not found
    #     url = reverse('get_student_course_attendance', args=['999', self.course.code])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(response.json()['error'], 'Student not found')

    # def test_course_not_found(self):
    #     # Test case for course not found
    #     url = reverse('get_student_course_attendance', args=[self.student.roll, 'MATH101'])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(response.json()['error'], 'Course not found')

    # def test_student_not_enrolled_in_course(self):
    #     # Test case for student not enrolled in the course
    #     new_course = Course.objects.create(code='CS102', title='Advanced CS')
    #     url = reverse('get_student_course_attendance', args=[self.student.roll, new_course.code])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(response.json()['error'], 'Student is not enrolled in this course')

    # def test_attendance_records_empty(self):
    #     # Test case for no attendance records
    #     new_student = Student.objects.create(roll='67890', name='New Student', email='newstudent@example.com', password=make_password('password'))
    #     StudentCourse.objects.create(student=new_student, course=self.course)  # Enroll in the same course

    #     url = reverse('get_student_course_attendance', args=[new_student.roll, self.course.code])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.json()['attendance_records'], [])

    # def test_general_exception(self):
    #     # Test case for a general exception (e.g., database issue)
    #     url = reverse('get_student_course_attendance', args=['999', '999'])
    #     response = self.client.get(url)
        
    #     # Ensure that an exception is properly raised if needed (i.e., 404 or 500 error)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(response.json()['error'], 'Student or course not found')