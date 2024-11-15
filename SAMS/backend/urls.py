from django.urls import path
from .views import *

urlpatterns = [
    path('login', login_api, name='login'),

    path('students/<str:roll>/courses/attendance', get_student_courses_attendance, name='get_student_courses_attendance'),
    path('students/<str:roll>/courses', get_student_courses, name='get_student_courses_attendance'),
    path('students/<str:roll>/<str:course_code>/attendance/', get_student_course_attendance, name='get_student_course_attendance'),
    path('students/<str:roll>/profile/', get_student_profile, name='get_student_profile'),
    
    path('students/profile/update/', update_student, name='update_student'),
    
    path('teachers/profile/update/', update_teacher, name='update_teacher'),
    path('admins/profile/update/', update_admin, name='update_admin'),

    path('ta/<str:roll_no>/courses/', TACourseListView.as_view(), name='ta-course-list'),
    path('teacher/<str:teacher_id>/courses/', TeacherCourseListView.as_view(), name='teacher-course-list'),
    path('course/<str:course_code>/students/', CourseStudentListView.as_view(), name='course-student-list'),


    path('teacher/dashboard/<str:id>/courses/', teacher_dashboard_courses, name='teacher-dashboard-courses'),


    # path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    # path('teachers/', TeacherListCreateView.as_view(), name='teacher-list-create'),
    # path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    # path('attendance/', AttendanceListCreateView.as_view(), name='attendance-list-create'),
    # path('slots/', SlotListCreateView.as_view(), name='slot-list-create'),
    # path('course-slots/', CourseSlotListCreateView.as_view(), name='course-slot-list-create'),
    # path('course-teachers/', CourseTeacherListCreateView.as_view(), name='course-teacher-list-create'),
    # path('ta/', TAListCreateView.as_view(), name='ta-list-create'),

        # Swagger and Redoc
#    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('mark_attendances/', mark_attendances, name='mark_attendances'),




    path('teacher/', create_teacher, name='create_teacher'),
    path('create-student/', create_student, name='create_student'),
    path('create-course/', create_course, name='create_course'),
    path('slots/create/', create_slot, name='slot-create'),
    path('enroll_teacher/', enroll_teacher, name='enroll_teacher'),
    path('add-slot-to-course/',add_slot_to_course, name='add_slot_to_course'),
    path('enroll_ta/', enroll_ta, name='enroll_ta'),
    path('enroll_student/', enroll_student_in_course, name='enroll_student_in_course'),





    path('student/admin/<str:roll>/delete/', delete_student, name='admin-delete-student'),
    path('teacher/admin/<str:id>/delete/', delete_teacher, name='admin-delete-teacher'),
    path('admin/<str:id>/delete/', delete_admin, name='admin-delete-admin'),
    path('course/admin/<str:code>/delete/', delete_course, name='admin-delete-course'),
    path('slot/admin/<str:id>/delete/', delete_slot, name='admin-delete-slot'),
    path('course-slot/admin/<str:course_code>/<str:slot_id>/delete/', delete_course_slot, name='admin-delete-course-slot'),
    path('course-teacher/admin/<str:course_code>/<str:teacher_id>/delete/', delete_course_teacher, name='admin-delete-course-teacher'),
    path('ta/admin/<str:student_roll>/<str:course_code>/<str:teacher_id>/delete/', delete_ta, name='admin-delete-ta'),
    # path('attendance/admin/<str:student_roll>/<str:course_code>/<str:date>/delete/', delete_attendance, name='admin-delete-attendance'),
    path('student-course/admin/<str:student_roll>/<str:course_code>/delete/', delete_student_course, name='admin-delete-student-course'),



    path('student/admin/get-all/', get_all_students, name='admin-get-all-students'),
    path('teacher/admin/get-all/', get_all_teachers, name='admin-get-all-teachers'),
    path('admin/admin/get-all/', get_all_admins, name='admin-get-all-admins'),
    path('course/admin/get-all/', get_all_courses, name='admin-get-all-courses'),
    path('slot/admin/get-all/', get_all_slots, name='admin-get-all-slots'),
    path('course-slot/admin/get-all/', get_all_course_slots, name='admin-get-all-course-slots'),
    path('course-teacher/admin/get-all/', get_all_course_teachers, name='admin-get-all-course-teachers'),
    path('ta/admin/get-all/', get_all_tas, name='admin-get-all-tas'),
    path('attendance/admin/get-all/', get_all_attendances, name='admin-get-all-attendances'),
    path('student-course/admin/get-all/', get_all_student_courses, name='admin-get-all-student-courses'),

]
