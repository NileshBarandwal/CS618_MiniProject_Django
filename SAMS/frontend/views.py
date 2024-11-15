import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import date

API_BASE_URL = "http://127.0.0.1:8000/api"

def login_page(request):
    return render(request, 'login/index.html')


def save_data(request):
    role = request.GET.get('role', 'student')
    user_id = request.GET.get('user_id', 'CS24MT013')
    user_name = request.GET.get('user_name', 'Generic Name')

    if role == 'student':
        request.session['student_roll'] = user_id
        request.session['student_name'] = user_name
        return student_dashboard(request)
    elif role == 'teacher':
        request.session['teacher_id'] = user_id
        request.session['teacher_name'] = user_name
        return courses(request)
    elif role == 'admin':
        request.session['admin_id'] = user_id
        request.session['admin_name'] = user_name
        return admin_profile(request)


def forgot_password_view(request):
    return render(request, 'login/forgot_password.html')

# @login_required
def teacher_course_attendance(request):
    # Check if the user is associated with the Teacher model
    # if not Teacher.objects.filter(user=request.user).exists():
        # return HttpResponseForbidden("You are not authorized to access this page.")
    
    return render(request, 'teacher/courses_attendance.html')
 
# @login_required   
def teacher_course_take_attendance(request):
    # if not Teacher.objects.filter(user=request.user).exists():
        # return HttpResponseForbidden("You are not authorized to access this page.")
    
    return render(request, 'teacher/take_attendance.html')

# @login_required
def teacher_manage_courses_attendance(request):
    # if not Teacher.objects.filter(user=request.user).exists():
        # return HttpResponseForbidden("You are not authorized to access this page.")
    
    return render(request, 'teacher/manage_courses_attendance.html')

# @login_required
def courses(request):
    # if not Teacher.objects.filter(user=request.user).exists():
        # return HttpResponseForbidden("You are not authorized to access this page.")
    teacher_id = request.session.get('teacher_id')

    api_url = f"{API_BASE_URL}/teacher/dashboard/{teacher_id}/courses/"
    
    # Fetch data from the API
    try:
        response = requests.get(api_url)
        
        if response.status_code == 200:
            response_data = response.json()

            courses = response_data,  # Use an empty list if 'courses' key does not exist

            print(courses[0])

            return render(request, 'teacher/courses.html', {'courses': courses[0]})
        
        else:
            # If the response is not successful, handle the error
            error_message = response.json().get('error', 'Could not fetch data')
            return JsonResponse({'error': error_message}, status=response.status_code)
    
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions (e.g., network issues)
        return JsonResponse({'error': str(e)}, status=500)


# @login_required
def teacher_manage_attendance(request):
        courses = [
        {'code': 'CS 101', 'name': 'Computer Science', 'attendance': 85},
        {'code': 'MAH 201', 'name': 'Calculus', 'attendance': 90},
        {'code': 'PHY 102', 'name': 'Physics', 'attendance': 78},
        {'code': 'CHE 103', 'name': 'Chemistry', 'attendance': 88},
        {'code': 'CS 101', 'name': 'Computer Science', 'attendance': 85},
        {'code': 'MAH 201', 'name': 'Calculus', 'attendance': 90},
        {'code': 'PHY 102', 'name': 'Physics', 'attendance': 78},
        {'code': 'CHE 103', 'name': 'Chemistry', 'attendance': 88},
        {'code': 'CS 101', 'name': 'Computer Science', 'attendance': 85},
        {'code': 'MAH 201', 'name': 'Calculus', 'attendance': 90},
        {'code': 'PHY 102', 'name': 'Physics', 'attendance': 78},
        # Add more courses as needed...
    ]
        return render(request, 'teacher/manage_attendance.html', {'courses': courses})

# @login_required
def teacher_profile(request):
    return render(request, 'teacher/profile.html')

# @login_required
def demo(request):
    return render(request, 'basic.html')

# @login_required
def swagger_ui(request):
    return render(request, 'swagger.html')  



# @login_required
def student_dashboard(request):
    student_roll = request.session.get('student_roll')
    print(f"Frontend view, student roll: {student_roll}")
    # Define API endpoint URL
    api_url = f"{API_BASE_URL}/students/{student_roll}/courses/attendance"
    
    # Fetch data from the API
    try:
        response = requests.get(api_url)
        
        if response.status_code == 200:
            response_data = response.json()

            context = {
                'courses': response_data.get('courses', []),  # Use an empty list if 'courses' key does not exist
            }

            return render(request, 'student/dashboard.html', context)
        
        else:
            # If the response is not successful, handle the error
            error_message = response.json().get('error', 'Could not fetch data')
            return JsonResponse({'error': error_message}, status=response.status_code)
    
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions (e.g., network issues)
        return JsonResponse({'error': str(e)}, status=500)

# @login_required
def student_view_attendance(request):
    student_roll = request.session.get('student_roll')
    course_code = request.GET.get('course_code', 'CS 618')
    attendance_api_url = f"{API_BASE_URL}/students/{student_roll}/{course_code}/attendance"
    
    courses_api_url = f"{API_BASE_URL}/students/{student_roll}/courses"
    
    try:
        # Fetch attendance data from the API
        attendance_response = requests.get(attendance_api_url)
        attendance_data = attendance_response.json()

        # Fetch courses data from the API
        courses_response = requests.get(courses_api_url)
        courses_data = courses_response.json()

        if attendance_response.status_code == 200 and courses_response.status_code == 200:
            # Pass attendance and course data to the template
            attendance_records = attendance_data['attendance_records']
            courses = courses_data['courses']  # Assume the API returns a list of courses here
            
            context = {
                'student_info': {
                    'roll': attendance_data['student_roll'],
                    'course_code': attendance_data['course_code'],
                    'attendance_records': attendance_records,
                },
                'courses': courses  # List of courses for the dropdown
            }
            return render(request, 'student/view_attendance.html', context)
        
        else:
            # Handle error responses from API
            return JsonResponse({'error': 'Could not fetch data'}, status=attendance_response.status_code)
    
    except requests.RequestException as e:
        return JsonResponse({'error': 'Failed to connect to the API'}, status=500)

# @login_required
def student_take_attendance(request):
    today_date = date.today()
    student_roll = request.session.get('student_roll')
    course_code = request.GET.get('course_code', 'CS 612')
    selected_date = request.GET.get('date', '2024-11-08')

    courses_api_url = f"{API_BASE_URL}/ta/{student_roll}/courses"

    students_api_url = f"{API_BASE_URL}/course/{course_code}/students"
    
    try:
        courses_response = requests.get(courses_api_url)
        courses = courses_response.json()

        students_response = requests.get(students_api_url)
        students = students_response.json()

        if courses_response.status_code == 200 and students_response.status_code == 200:
            
            context = {
                'courses': courses,
                'course_code': course_code,
                'date': selected_date,
                'students': students,
                'today_date': today_date,
            }
            return render(request, 'student/take_attendance.html', context)
        
        else:
            # Handle error responses from API
            return JsonResponse({'error': 'Could not fetch data'}, status=courses_response.status_code)
    
    except requests.RequestException as e:
        return JsonResponse({'error': 'Failed to connect to the API'}, status=500)


def teacher_take_attendance(request):
    today_date = date.today()
    teacher_id = request.GET.get('teacher_id', 'I016')
    course_code = request.GET.get('course_code', 'CS 618')
    selected_date = request.GET.get('date', '2024-11-08')

    courses_api_url = f"{API_BASE_URL}/teacher/{teacher_id}/courses"

    students_api_url = f"{API_BASE_URL}/course/{course_code}/students"
    
    try:
        courses_response = requests.get(courses_api_url)
        courses = courses_response.json()

        students_response = requests.get(students_api_url)
        students = students_response.json()

        if courses_response.status_code == 200 and students_response.status_code == 200:
            
            context = {
                'teacher': {
                    'id': teacher_id,
                },
                'courses': courses,
                'course_code': course_code,
                'date': selected_date,
                'students': students,
                'today_date': today_date,
            }
            return render(request, 'teacher/take_attendance.html', context)
        
        else:
            # Handle error responses from API
            return JsonResponse({'error': 'Could not fetch data'}, status=courses_response.status_code)
    
    except requests.RequestException as e:
        return JsonResponse({'error': 'Failed to connect to the API'}, status=500)

# @login_required
def student_report(request):
    student = {'roll': 'CS24MT013'}
    return render(request, 'student/report.html', {'student': student})

# @login_required
def student_profile(request):
    student = {'roll': 'CS24MT013'}
    return render(request, 'student/profile.html', {'student': student})

# @login_required
def admin_profile(request):
    return render(request, 'admin/profile.html')

def admin_course_enrollment_slot(request):
    return render(request,'admin/Course_enrollment_slot.html')

def admin_course_enrollment(request):
    return render(request, 'admin/Course_enrollment.html')

def admin_enrollment_student(request):
    return render(request, 'admin/Enrollment_student.html')

def admin_enrollment_teacher(request):
    return render(request, 'admin/Enrollment_teacher.html')

def admin_enrollment(request):
    return render(request, 'admin/Enrollment.html')

def admin_manage_slot(request):
    return render(request, 'admin/Manage_slot.html')  

def admin_manage(request):
    return render(request, 'admin/Manage.html')      

def admin_student_add_subject(request):
    return render(request, 'admin/Student_add_student.html')    

def admin_student_enrollment(request):
    return render(request, 'admin/Student_Enrollment.html')  

def admin_student(request):
    return render(request, 'admin/Student.html')        

def admin_subject_add_subject(request):
    return render(request, 'admin/Subject_add_subject.html')        

def admin_subject(request):
    return render(request, 'admin/Subject.html')      

def admin_TA_enrollment_ta(request):
    return render(request, 'admin/TA_Enrollment_TA.html')       

def admin_TA_enrollment(request):
    return render(request, 'admin/TA_Enrollment.html')  

def admin_teacher_add_teacher(request):
    return render(request, 'admin/Teacher_add_teacher.html')     

def admin_teacher(request):
    return render(request, 'admin/Teacher.html') 

def admin_master(request):
    return render(request, 'admin/master.html')     
    # Check if the user is associated with the Admin model
    # if not Admin.objects.filter(user=request.user).exists():
        # return HttpResponseForbidden("You are not authorized to access this page.")
    
def logout_view(request):
    logout(request)  # Logs out the user and removes the session key
    return redirect('/')  # Redirect to the homepage or login page

