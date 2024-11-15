from django.contrib import admin
from .models import Student, Teacher, Admin, Course, Slot, CourseSlot, CourseTeacher, TA, Attendance, StudentCourse

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Admin)
admin.site.register(Course)
admin.site.register(Slot)
admin.site.register(CourseSlot)
admin.site.register(CourseTeacher)
admin.site.register(TA)
admin.site.register(Attendance)
admin.site.register(StudentCourse)
