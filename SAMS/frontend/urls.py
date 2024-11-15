from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='home'),  # Default route to the home (login) page
    path('save_data/', views.save_data, name='save_data'),  # Default route to the home (login) page
    path('swagger/', views.swagger_ui, name='swagger_docs'),  # Route for Swagger docs
    path('basic/', views.demo, name='basic'),
    path('teacher/courses/', views.courses, name='teacher/courses'),
    path('teacher/courses/courses_attendance/', views.teacher_course_attendance, name='teacher/courses/courses_attendance'),
    path('teacher/courses/courses_attendance/take_attendance', views.teacher_take_attendance, name='teacher/courses/courses_attendance/take_attendance'),
    path('teacher/manage_attendance/', views.teacher_manage_attendance, name='teacher/manage_attendance'),
    
    path('teacher/take_attendance', views.teacher_take_attendance, name='teacher/take_attendance'),

    path('teacher/manage_attendance/manage_courses_attendance', views.teacher_manage_courses_attendance, name='teacher/manage_attendance/manage_courses_attendance'),
    
    path('teacher/profile/', views.teacher_profile, name='teacher/profile'),
    path('login/forgot_password/', views.forgot_password_view, name='login/forgot_password'),
    
    path('student/', views.student_dashboard, name='student'),

    path('student/dashboard/', views.student_dashboard, name='student/dashboard'),
    path('student/view_attendance/', views.student_view_attendance, name='student/view_attendance'),
    path('student/take_attendance/', views.student_take_attendance, name='student/take_attendance'),
    path('student/profile/', views.student_profile, name='student/profile'),
    path('student/report/', views.student_report, name='student/report'),

    path('admin_custom/course_enrollment_slot', views.admin_course_enrollment_slot, name='admin_custom/course_enrollment_slot'),
    path('admin_custom/course_enrollment', views.admin_course_enrollment, name='admin_custom/course_enrollment'),
    path('admin_custom/enrollment_student', views.admin_enrollment_student, name='admin_custom/enrollment_student'),
    path('admin_custom/enrollment_teacher', views.admin_enrollment_teacher, name='admin_custom/enrollment_teacher'),
    path('admin_custom/enrollment', views.admin_enrollment, name='admin_custom/enrollment'),
    path('admin_custom/manage_slot', views.admin_manage_slot, name='admin_custom/manage_slot'),
    path('admin_custom/manage', views.admin_manage, name='admin_custom/manage'),
    path('admin_custom/student_add_subject', views.admin_student_add_subject, name='admin_custom/student_add_subject'),
    path('admin_custom/student_enrollment', views.admin_student_enrollment, name='admin_custom/student_enrollment'),
    path('admin_custom/student', views.admin_student, name='admin_custom/student'),
    path('admin_custom/subject_add_subject', views.admin_subject_add_subject, name='admin_custom/subject_add_subject'),
    path('admin_custom/subject', views.admin_subject, name='admin_custom/subject'),
    path('admin_custom/TA_enrollment_ta', views.admin_TA_enrollment_ta, name='admin_custom/TA_enrollment_ta'),
    path('admin_custom/TA_enrollment', views.admin_TA_enrollment, name='admin_custom/TA_enrollment'),
    path('admin_custom/teacher_add_teacher', views.admin_teacher_add_teacher, name='admin_custom/teacher_add_teacher'),
    path('admin_custom/teacher', views.admin_teacher, name='admin_custom/teacher'),
    path('admin_custom/profile', views.admin_profile, name='admin_custom/profile'),
    path('admin_custom/master', views.admin_master, name='admin_custom/master'),

    path('admin_custom/', views.admin_profile, name='admin_custom'),
    path('', views.logout_view, name='logout'),
]