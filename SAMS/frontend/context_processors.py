def student_roll(request):
    return {
        'student_roll': request.session.get('student_roll', None)
    }

def student_name(request):
    return {
        'student_name': request.session.get('student_name', None)
    }


def teacher_id(request):
    return {
        'teacher_id': request.session.get('teacher_id', None)
    }

def teacher_name(request):
    return {
        'teacher_name': request.session.get('teacher_name', None)
    }


def admin_id(request):
    return {
        'admin_id': request.session.get('admin_id', None)
    }

def admin_name(request):
    return {
        'admin_name': request.session.get('admin_name', None)
    }