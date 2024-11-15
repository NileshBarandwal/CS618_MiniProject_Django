from rest_framework import serializers
from .models import *

# 1. Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['roll', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only
        }

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

# 2. Teacher Serializer
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'email', 'password']  # Include only the necessary fields

    # Custom create method to handle password hashing
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

# 3. Admin Serializer
class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Admin
        fields = ['id', 'name', 'email', 'password']

# 4. Course Serializer
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['code', 'title', 'venue']  # Include the fields you want to expose in the API


# 5. Slot Serializer
class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['id', 'day', 'start_time', 'duration']


class CourseSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSlot
        fields = ['course', 'slot']  # Fields to include in the serialized output

# 6. CourseSlot Serializer (for associating courses and slots)
class AddSlotToCourseSerializer(serializers.Serializer):
    course_code = serializers.CharField(max_length=20)
    slot_id = serializers.CharField(max_length=5)

    def validate_course_code(self, value):
        """
        Check if the course exists in the database.
        """
        if not Course.objects.filter(code=value).exists():
            raise serializers.ValidationError(f"Course with code {value} does not exist.")
        return value

    def validate_slot_id(self, value):
        """
        Check if the slot exists in the database.
        """
        if not Slot.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Slot with ID {value} does not exist.")
        return value

    def create(self, validated_data):
        """
        Create the CourseSlot association.
        """
        course = Course.objects.get(code=validated_data['course_code'])
        slot = Slot.objects.get(id=validated_data['slot_id'])

        # Check if the slot is already associated with the course
        if CourseSlot.objects.filter(course=course, slot=slot).exists():
            raise serializers.ValidationError("This slot is already associated with the course.")

        # Create the association
        course_slot = CourseSlot.objects.create(course=course, slot=slot)
        return course_slot

# 7. CourseTeacher Serializer (for associating courses and teachers)
class CourseTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTeacher
        fields = ['course', 'teacher']

# 8. TA Serializer (for associating TAs with courses and teachers)
class TAEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TA
        fields = ['student', 'course', 'teacher']

# 9. Attendance Serializer (for recording attendance of students in courses)
class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ['student', 'course', 'date', 'status']

# 10. Student Course Serializer
class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = ['student', 'course']