import csv
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date, parse_time
from backend.models import (
    Student, Teacher, Admin, Course, Slot, CourseSlot,
    CourseTeacher, TA, Attendance, StudentCourse
)  # Replace 'your_app' with the name of your Django app

class Command(BaseCommand):
    help = 'Load data into specified table from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('table', type=str, help='The name of the table to populate')
        parser.add_argument('csv_file', type=str, help='Path to the CSV file to import data from')

    def handle(self, *args, **kwargs):
        table = kwargs['table'].lower()
        csv_file_path = kwargs['csv_file']

        # Open the CSV file and read it
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)

            # Check table name and process accordingly
            if table == 'student':
                self.load_student(reader)
            elif table == 'teacher':
                self.load_teacher(reader)
            elif table == 'admin':
                self.load_admin(reader)
            elif table == 'course':
                self.load_course(reader)
            elif table == 'slot':
                self.load_slot(reader)
            elif table == 'courseslot':
                self.load_courseslot(reader)
            elif table == 'courseteacher':
                self.load_courseteacher(reader)
            elif table == 'ta':
                self.load_ta(reader)
            elif table == 'attendance':
                self.load_attendance(reader)
            elif table == 'studentcourse':
                self.load_studentcourse(reader)
            else:
                self.stdout.write(self.style.ERROR(f'Unknown table name: {table}'))
                return

            self.stdout.write(self.style.SUCCESS(f'Successfully loaded data into {table}'))

    # Table-specific loading functions
    def load_student(self, reader):
        students = [Student(roll=row['roll'], name=row['name'], email=row['email']) for row in reader]
        Student.objects.bulk_create(students, ignore_conflicts=True)

    def load_teacher(self, reader):
        teachers = [Teacher(id=row['id'], name=row['name'], email=row['email']) for row in reader]
        Teacher.objects.bulk_create(teachers, ignore_conflicts=True)

    def load_admin(self, reader):
        admins = [Admin(id=row['id'], name=row['name'], email=row['email']) for row in reader]
        Admin.objects.bulk_create(admins, ignore_conflicts=True)

    def load_course(self, reader):
        courses = [Course(code=row['code'], title=row['title'], venue=row['venue']) for row in reader]
        Course.objects.bulk_create(courses, ignore_conflicts=True)

    def load_slot(self, reader):
        slots = [
            Slot(
                id=row['slot_id'],
                day=int(row['day']),
                start_time=parse_time(row['start_time']),
                duration=int(row['duration'])
            ) for row in reader
        ]
        Slot.objects.bulk_create(slots, ignore_conflicts=True)

    def load_courseslot(self, reader):
        courseslots = [
            CourseSlot(
                course_id=row['course_code'],
                slot_id=row['slot_id']
            ) for row in reader
        ]
        CourseSlot.objects.bulk_create(courseslots, ignore_conflicts=True)

    def load_courseteacher(self, reader):
        courseteachers = [
            CourseTeacher(
                course_id=row['course_code'],
                teacher_id=row['teacher_id']
            ) for row in reader
        ]
        CourseTeacher.objects.bulk_create(courseteachers, ignore_conflicts=True)

    def load_ta(self, reader):
        tas = [
            TA(
                student_id=row['student_id'],
                course_id=row['course_code'],
                teacher_id=row['teacher_id']
            ) for row in reader
        ]
        TA.objects.bulk_create(tas, ignore_conflicts=True)

    def load_attendance(self, reader):
        attendance_records = [
            Attendance(
                student_id=row['student_id'],
                course_id=row['course_code'],
                date=parse_date(row['date']),
                status=int(row['status'])
            ) for row in reader
        ]
        Attendance.objects.bulk_create(attendance_records, ignore_conflicts=True)

    def load_studentcourse(self, reader):
        studentcourses = [
            StudentCourse(
                student_id=row['student_id'],
                course_id=row['course_code']
            ) for row in reader
        ]
        StudentCourse.objects.bulk_create(studentcourses, ignore_conflicts=True)
