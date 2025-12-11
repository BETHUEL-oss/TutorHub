from courses.models import Course
def global_stats(request):
    total_courses = Course.objects.count()
    total_teachers = Course.objects.values('teacher').distinct().count()
    return {'total_courses': total_courses, 'total_teachers': total_teachers}