from django.db import models
from django.contrib.auth.hashers import make_password

# 1. Student Model
class Student(models.Model):
    roll = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    last_login = models.DateTimeField(null=True, blank=True)  # Add this field
    password = models.CharField(max_length=128)  # For storing hashed passwords

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):  # Check if already hashed
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


# 2. Teacher Model
class Teacher(models.Model):
    id = models.CharField(max_length=10, primary_key=True)  # Format "T001"
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)  # Add this field

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


# 3. Admin Model
class Admin(models.Model):
    id = models.CharField(max_length=10, primary_key=True)  # Format "A001"
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)  # Add this field

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


# 4. Course Model
class Course(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.title}"


# 5. Slot Model
class Slot(models.Model):
    DAY_CHOICES = [
            (0, 'Monday'),
            (1, 'Tuesday'),
            (2, 'Wednesday'),
            (3, 'Thursday'),
            (4, 'Friday'),
            (5, 'Saturday'),
            (6, 'Sunday'),
    ]
    id = models.CharField(max_length=5, primary_key=True)  # Format "A1"
    day = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    duration = models.IntegerField()  # Duration in minutes

    def __str__(self):
        return f"{self.id}: {self.day} - {self.start_time} ({self.duration} mins)"


# 6. CourseSlot Model (Associates Course with Slots)
class CourseSlot(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'slot')

    def __str__(self):
        return f"{self.course} - {self.slot}"


# 7. CourseTeacher Model (Associates Teachers with Courses)
class CourseTeacher(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'teacher')

    def __str__(self):
        return f"{self.course} - {self.teacher}"


# 8. TA (Teaching Assistant) Model (Associates TAs with Courses and Teachers)
class TA(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'course', 'teacher')

    def __str__(self):
        return f"TA: {self.student} - Course: {self.course} - Under Teacher: {self.teacher}"


# 9. Attendance Model (Records Attendance of Students in Courses)
class Attendance(models.Model):
    STATUS_CHOICES = [
        (1, 'Present'),
        (0, 'Absent'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.IntegerField(choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'course', 'date')

    def __str__(self):
        return f"{self.student} - {self.course} - {self.date}: {self.status}"

# 10. StudentCourse Model (Associates Students with Courses)
class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'course')
    
    def __str__(self):
        return f"{self.student} enrolled in {self.course}"