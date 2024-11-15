from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from django.db.models import Avg
from datetime import date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.utils.dateparse import parse_date

from django.shortcuts import get_object_or_404

# from sams:
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .views import *


def login_api(request):
    if request.method == "POST":
        try:
            # Parse the incoming JSON request body
            data = json.loads(request.body)

            print(data)

            username = data.get('username')
            password = data.get('password')
            role = data.get('role')

            if not username or not password or not role:
                return JsonResponse({'status': 'error', 'message': 'Username, password, and role are required'}, status=400)

            # Determine the model based on the role
            user_model = None
            if role == 'student':
                user_model = Student
                user = user_model.objects.get(roll=username)
            elif role == 'teacher':
                user_model = Teacher
                user = user_model.objects.get(id=username)
            elif role == 'admin':
                user_model = Admin
                user = user_model.objects.get(id=username)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid role'}, status=400)

            try:
                # Try to get the user based on the username (assuming primary key is username)
                
                
                # Authenticate by checking the password
                if check_password(password, user.password):
                    print("correct password")
                    # Update the last login time for the user
                    user.last_login = timezone.now()
                    user.save()

                    # Return a successful response with relevant user data
                    return JsonResponse({
                        'status': 'success',
                        'message': f'{role.capitalize()} logged in successfully',
                        'data': {
                            'name': user.name,  # Assuming `name` is a field in your models
                            'id': user.pk  # Primary key is used as user identifier
                        }
                    }, status=200)
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid password'}, status=401)
            except user_model.DoesNotExist:
                # User not found in the database
                return JsonResponse({'status': 'error', 'message': f'{role.capitalize()} not found'}, status=404)

        except json.JSONDecodeError:
            # If the request body is not valid JSON
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON request body'}, status=400)

        except Exception as e:
            # General exception handler for any other unexpected errors
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    # If the request method is not POST
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


# 1. Get course details and attendance percentage for a student
@api_view(['GET'])
def get_student_courses_attendance(request, roll):
    try:
        student = Student.objects.get(roll=roll)
        student_courses = StudentCourse.objects.filter(student=student).select_related('course')

        course_details = []
        for sc in student_courses:
            course = sc.course
            attendance_avg = Attendance.objects.filter(student=student, course=course).aggregate(average=Avg('status'))['average']

            # Default to 0.0 if there is no attendance data
            attendance_percentage = round(attendance_avg * 100, 2) if attendance_avg is not None else 0.0

            course_details.append({
                'code': course.code,
                'name': course.title,
                'attendance': attendance_percentage
            })

        return Response({'courses': course_details}, status=status.HTTP_200_OK)
    
    except Student.DoesNotExist:
        return Response({'error': f'Student not found, {roll}'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 2. Get detailed attendance records for a student in a specific course
@api_view(['GET'])
def get_student_course_attendance(request, roll, course_code):
    try:
        student = Student.objects.get(roll=roll)
        course = Course.objects.get(code=course_code)
        attendance_records = Attendance.objects.filter(student=student, course=course).values('date', 'status')

        return Response({
            'student_roll': student.roll,
            'course_code': course.code,
            'attendance_records': list(attendance_records)
        }, status=status.HTTP_200_OK)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 3. Get student's profile
@api_view(['GET'])
def get_student_profile(request, roll):
    try:
        student = Student.objects.get(roll=roll)
        return Response({
            'roll': student.roll,
            'name': student.name,
            'email': student.email
        }, status=status.HTTP_200_OK)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 5. get student courses:
@api_view(['GET'])
def get_student_courses(request, roll):
    try:
        student = Student.objects.get(roll=roll)
        student_courses = StudentCourse.objects.filter(student=student).select_related('course')

        courses = []
        for sc in student_courses:
            course = sc.course
            courses.append({
                'code': course.code,
                'name': course.title,
            })

        return Response({'courses': courses}, status=status.HTTP_200_OK)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def mark_attendances(request):
    attendances = request.data.get('attendances', [])  # Expecting an array of attendance records

    if not attendances:
        return JsonResponse({"error": "No attendance data provided"}, status=400)

    results = []
    flag = False  # Track if at least one attendance entry is successfully processed

    for attendance_data in attendances:
        student_roll = attendance_data.get('student_roll')
        course_code = attendance_data.get('course_code')
        status = attendance_data.get('status')
        date_value = parse_date(attendance_data.get('date_value', str(date.today())))  # Parse or default to today

        try:
            # Get the student and course from the database
            student = Student.objects.get(roll=student_roll)
            course = Course.objects.get(code=course_code)

            # Validate the status
            if status not in [0, 1]:
                results.append({"student_roll": student_roll, "status": "failed", "error": "Invalid status"})
                continue

            # Attempt to get or create the Attendance record
            attendance, created = Attendance.objects.update_or_create(
                student=student, course=course, date=date_value,
                defaults={'status': status}
            )

            # Track result
            if created:
                results.append({"student_roll": student_roll, "status": "created"})
            else:
                results.append({"student_roll": student_roll, "status": "updated"})
            
            flag = True

        except Student.DoesNotExist:
            results.append({"student_roll": student_roll, "status": "failed", "error": "Student not found"})
            flag = False
        except Course.DoesNotExist:
            results.append({"student_roll": student_roll, "status": "failed", "error": "Course not found"})
            flag = False
        except Exception as e:
            results.append({"student_roll": student_roll, "course_code": course_code, "date": date_value, "status": "failed", "error": str(e)})
            flag = False

    # Return success message if any attendance was recorded successfully
    if flag:
        return JsonResponse({"message": "Attendance marked successfully!", "results": results}, status=201)
    else:
        return JsonResponse({"message": "No attendance records processed successfully", "results": results}, status=400)


class TACourseListView(APIView):
    def get(self, request, roll_no):
        try:
            student = Student.objects.get(roll=roll_no)
            ta_courses = TA.objects.filter(student=student)
            courses = Course.objects.filter(code__in=[ta.course.code for ta in ta_courses]).distinct()

            courses = [{"code": course.code, "title": course.title} for course in courses]
            
            return Response(courses, status=status.HTTP_200_OK)
        
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

class TeacherCourseListView(APIView):
    def get(self, request, teacher_id):
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_courses = CourseTeacher.objects.filter(teacher=teacher)
            courses = Course.objects.filter(code__in=[tc.course.code for tc in teacher_courses]).distinct()

            courses = [{"code": course.code, "title": course.title} for course in courses]
            
            return Response(courses, status=status.HTTP_200_OK)
        
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

class CourseStudentListView(APIView):
    def get(self, request, course_code):
        try:
            course = Course.objects.get(code=course_code)
            student_courses = StudentCourse.objects.filter(course=course)
            
            student_data = [
                {"roll": sc.student.roll, "name": sc.student.name}
                for sc in student_courses
            ]
            
            return Response(student_data, status=status.HTTP_200_OK)
        
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['PUT'])
def update_student(request):
    try:
        roll = request.data.get('roll')
        # Find the student by roll number
        student = Student.objects.get(roll=roll)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Partial updates allow us to only update fields that are provided in the request
    serializer = StudentSerializer(student, data=request.data, partial=True)
    
    if serializer.is_valid():
        if 'password' in request.data:
            # Hash the password if it's provided in the request
            serializer.validated_data['password'] = make_password(request.data['password'])
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # If validation fails, return an error response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_teacher(request):
    try:
        id = request.data.get('id')
        # Find the teacher by id
        teacher = Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Partial updates allow us to only update fields that are provided in the request
    serializer = TeacherSerializer(teacher, data=request.data, partial=True)
    
    if serializer.is_valid():
        if 'password' in request.data:
            # Hash the password if it's provided in the request
            serializer.validated_data['password'] = make_password(request.data['password'])
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # If validation fails, return an error response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def update_admin(request):
    try:
        id = request.data.get('id')
        # Find the admin by id
        admin = Admin.objects.get(id=id)
    except Admin.DoesNotExist:
        return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Partial updates allow us to only update fields that are provided in the request
    serializer = AdminSerializer(admin, data=request.data, partial=True)
    
    if serializer.is_valid():
        if 'password' in request.data:
            # Hash the password if it's provided in the request
            serializer.validated_data['password'] = make_password(request.data['password'])
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # If validation fails, return an error response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# # 1. API for Student List and Creation
# class StudentListCreateView(APIView):
#     def get(self, request):
#         students = Student.objects.all()
#         serializer = StudentSerializer(students, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         request_body=StudentSerializer,
#         responses={201: StudentSerializer(many=False)}
#     )

#     def post(self, request):
#         serializer = StudentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # 2. API for Teacher List and Creation
# class TeacherListCreateView(APIView):
#     def get(self, request):
#         teachers = Teacher.objects.all()
#         serializer = TeacherSerializer(teachers, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     @swagger_auto_schema(
#         request_body=TeacherSerializer,
#         responses={201: TeacherSerializer(many=False)}
#     )

#     def post(self, request):
#         serializer = TeacherSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # 3. API for Course List and Creation
# class CourseListCreateView(APIView):
#     def get(self, request):
#         courses = Course.objects.all()
#         serializer = CourseSerializer(courses, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         request_body=CourseSerializer,
#         responses={201: CourseSerializer(many=False)}
#     )

#     def post(self, request):
#         serializer = CourseSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # 4. API for Attendance
# class AttendanceListCreateView(APIView):
#     def get(self, request):
#         attendance_records = Attendance.objects.all()
#         serializer = AttendanceSerializer(attendance_records, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         request_body=AttendanceSerializer,
#         responses={201: AttendanceSerializer(many=False)}
#     )

#     def post(self, request):
#         serializer = AttendanceSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # API for Slot List and Creation
# class SlotListCreateView(APIView):
#     def get(self, request):
#         slots = Slot.objects.all()
#         serializer = SlotSerializer(slots, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(request_body=SlotSerializer, responses={201: SlotSerializer(many=False)})
#     def post(self, request):
#         serializer = SlotSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # API for CourseSlot List and Creation
# class CourseSlotListCreateView(APIView):
#     def get(self, request):
#         course_slots = CourseSlot.objects.all()
#         serializer = CourseSlotSerializer(course_slots, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(request_body=CourseSlotSerializer, responses={201: CourseSlotSerializer(many=False)})
#     def post(self, request):
#         serializer = CourseSlotSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # API for CourseTeacher List and Creation
# class CourseTeacherListCreateView(APIView):
#     def get(self, request):
#         course_teachers = CourseTeacher.objects.all()
#         serializer = CourseTeacherSerializer(course_teachers, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(request_body=CourseTeacherSerializer, responses={201: CourseTeacherSerializer(many=False)})
#     def post(self, request):
#         serializer = CourseTeacherSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # API for TA List and Creation
# class TAListCreateView(APIView):
#     def get(self, request):
#         tas = TA.objects.all()
#         serializer = TASerializer(tas, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(request_body=TASerializer, responses={201: TASerializer(many=False)})
#     def post(self, request):
#         serializer = TASerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def create_teacher(request):
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    
@api_view(['POST'])
def create_course(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
@api_view(['POST'])
def create_slot(request):
    serializer = SlotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def enroll_teacher(request):
    teacher_id = request.data.get('teacher_id')
    course_code = request.data.get('course_code')
    
    # Validate teacher and course existence
    try:
        teacher = Teacher.objects.get(id=teacher_id)
        course = Course.objects.get(code=course_code)
    except Teacher.DoesNotExist:
        return Response({'message': 'Teacher not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Course.DoesNotExist:
        return Response({'message': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if the teacher is already enrolled in the course
    if CourseTeacher.objects.filter(teacher=teacher, course=course).exists():
        return Response({'message': 'Teacher is already enrolled in this course.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create the CourseTeacher entry
    serializer = CourseTeacherSerializer(data={'teacher': teacher.id, 'course': course.code})
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Teacher enrolled successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

@api_view(['POST'])
def add_slot_to_course(request):
    course_code = request.data.get('course_code')
    slot_id = request.data.get('slot_id')

    if not course_code or not slot_id:
        return Response(
            {"error": "course_code and slot_id are required fields."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        course = Course.objects.get(code=course_code)
        slot = Slot.objects.get(id=slot_id)
    except Course.DoesNotExist:
        return Response(
            {"error": f"Course with code {course_code} does not exist."},
            status=status.HTTP_404_NOT_FOUND
        )
    except Slot.DoesNotExist:
        return Response(
            {"error": f"Slot with ID {slot_id} does not exist."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Check if the association already exists
    if CourseSlot.objects.filter(course=course, slot=slot).exists():
        return Response(
            {"error": "This slot is already associated with the course."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create the CourseSlot association
    CourseSlot.objects.create(course=course, slot=slot)
    return Response(
        {"message": f"Slot {slot_id} added to course {course_code} successfully."},
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
def enroll_ta(request):
    student_roll = request.data.get('student_roll')
    course_code = request.data.get('course_code')
    teacher_id = request.data.get('teacher_id')

    # Validate data
    if not student_roll or not course_code or not teacher_id:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch related models
        student = Student.objects.get(roll=student_roll)
        course = Course.objects.get(code=course_code)
        teacher = Teacher.objects.get(id=teacher_id)

        # Check if the student is already enrolled as a TA in the course under the teacher
        if TA.objects.filter(student=student, course=course, teacher=teacher).exists():
            return Response({'message': 'The student is already a TA for this course and teacher'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the TA enrollment
        ta_enrollment = TA(student=student, course=course, teacher=teacher)
        ta_enrollment.save()

        # Optionally, you can serialize the TA object before returning it
        # serializer = TAEnrollmentSerializer(ta_enrollment)

        return Response({'message': 'Student enrolled as TA successfully'}, status=status.HTTP_201_CREATED)

    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    except Teacher.DoesNotExist:
        return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def enroll_student_in_course(request):
    if request.method == 'POST':
        student_roll = request.data.get('student_roll')
        course_code = request.data.get('course_code')

        # Check if both student and course exist
        try:
            student = Student.objects.get(roll=student_roll)
            course = Course.objects.get(code=course_code)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if student is already enrolled
        if StudentCourse.objects.filter(student=student, course=course).exists():
            return Response({'message': 'Student is already enrolled in this course'}, status=status.HTTP_400_BAD_REQUEST)

        # Enroll student
        student_course = StudentCourse(student=student, course=course)
        student_course.save()

        # You can return a serializer response for better structure, e.g.:
        serializer = StudentCourseSerializer(student_course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)








@api_view(['GET'])
def teacher_dashboard_courses(request, id):
    # Check if the teacher exists
    teacher = get_object_or_404(Teacher, id=id)
    
    # Get all courses associated with this teacher
    course_teachers = CourseTeacher.objects.filter(teacher=teacher)
    
    # Build response data
    courses_data = []
    for course_teacher in course_teachers:
        course = course_teacher.course
        # Count the number of students enrolled in this course
        student_count = StudentCourse.objects.filter(course=course).count()
        courses_data.append({
            'course_code': course.code,
            'course_title': course.title,
            'student_count': student_count
        })
    
    return Response(courses_data, status=status.HTTP_200_OK)



@api_view(['DELETE'])
def delete_student(request, roll):
    # Retrieve the student based on roll
    student = get_object_or_404(Student, roll=roll)
    
    # Delete the student
    student.delete()
    return Response({"message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def delete_teacher(request, id):
    # Retrieve the teacher based on id
    teacher = get_object_or_404(Teacher, id=id)
    
    # Delete the teacher
    teacher.delete()
    return Response({"message": "Teacher deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def delete_admin(request, id):
    # Retrieve the admin based on id
    admin = get_object_or_404(Admin, id=id)
    
    # Delete the admin
    admin.delete()
    return Response({"message": "Admin deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def delete_course(request, code):
    # Retrieve the course based on the code
    course = get_object_or_404(Course, code=code)
    
    # Delete the course
    course.delete()
    return Response({"message": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def delete_slot(request, id):
    # Retrieve the slot based on id
    slot = get_object_or_404(Slot, id=id)
    
    # Delete the slot
    slot.delete()
    return Response({"message": "Slot deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def delete_course_slot(request, course_code, slot_id):
    # Retrieve the course and slot based on the provided parameters
    course = get_object_or_404(Course, code=course_code)
    slot = get_object_or_404(Slot, id=slot_id)
    
    # Retrieve the CourseSlot object to delete
    course_slot = get_object_or_404(CourseSlot, course=course, slot=slot)
    
    # Delete the CourseSlot object
    course_slot.delete()
    return Response({"message": "CourseSlot deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def delete_course_teacher(request, course_code, teacher_id):
    # Retrieve the course and teacher based on the provided parameters
    course = get_object_or_404(Course, code=course_code)
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    # Retrieve the CourseTeacher object to delete
    course_teacher = get_object_or_404(CourseTeacher, course=course, teacher=teacher)
    
    # Delete the CourseTeacher object
    course_teacher.delete()
    return Response({"message": "CourseTeacher deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def delete_ta(request, student_roll, course_code, teacher_id):
    # Retrieve the student, course, and teacher based on the provided parameters
    student = get_object_or_404(Student, roll=student_roll)
    course = get_object_or_404(Course, code=course_code)
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    # Retrieve the TA object to delete
    ta = get_object_or_404(TA, student=student, course=course, teacher=teacher)
    
    # Delete the TA object
    ta.delete()
    return Response({"message": "Teaching Assistant association deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# @api_view(['DELETE'])
# def delete_attendance(request, student_roll, course_code, date):
#     # Retrieve the student and course based on the provided parameters
#     student = get_object_or_404(Student, roll=student_roll)
#     course = get_object_or_404(Course, code=course_code)
    
#     # Retrieve the Attendance record to delete
#     attendance = get_object_or_404(Attendance, student=student, course=course, date=date)
    
#     # Delete the Attendance object
#     attendance.delete()
#     return Response({"message": "Attendance record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def delete_student_course(request, student_roll, course_code):
    # Retrieve the student and course based on the provided parameters
    student = get_object_or_404(Student, roll=student_roll)
    course = get_object_or_404(Course, code=course_code)
    
    # Retrieve the StudentCourse object to delete
    student_course = get_object_or_404(StudentCourse, student=student, course=course)
    
    # Delete the StudentCourse object
    student_course.delete()
    return Response({"message": "Student-Course association deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



# 1. Get all students
@api_view(['GET'])
def get_all_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

# 2. Get all teachers
@api_view(['GET'])
def get_all_teachers(request):
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)

# 3. Get all admins
@api_view(['GET'])
def get_all_admins(request):
    admins = Admin.objects.all()
    serializer = AdminSerializer(admins, many=True)
    return Response(serializer.data)

# 4. Get all courses
@api_view(['GET'])
def get_all_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

# 5. Get all slots
@api_view(['GET'])
def get_all_slots(request):
    slots = Slot.objects.all()
    serializer = SlotSerializer(slots, many=True)
    return Response(serializer.data)

# 6. Get all course slots (associating courses with slots)
@api_view(['GET'])
def get_all_course_slots(request):
    course_slots = CourseSlot.objects.all()
    serializer = CourseSlotSerializer(course_slots, many=True)
    return Response(serializer.data)

# 7. Get all course teachers (associating courses with teachers)
@api_view(['GET'])
def get_all_course_teachers(request):
    course_teachers = CourseTeacher.objects.all()
    serializer = CourseTeacherSerializer(course_teachers, many=True)
    return Response(serializer.data)

# 8. Get all teaching assistants (TAs)
@api_view(['GET'])
def get_all_tas(request):
    tas = TA.objects.all()
    serializer = TAEnrollmentSerializer(tas, many=True)
    return Response(serializer.data)

# 9. Get all attendances
@api_view(['GET'])
def get_all_attendances(request):
    attendances = Attendance.objects.all()
    serializer = AttendanceSerializer(attendances, many=True)
    return Response(serializer.data)

# 10. Get all student courses (associating students with courses)
@api_view(['GET'])
def get_all_student_courses(request):
    student_courses = StudentCourse.objects.all()
    serializer = StudentCourseSerializer(student_courses, many=True)
    return Response(serializer.data)