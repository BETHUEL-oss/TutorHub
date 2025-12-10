from courses.models import Courses
def global_stats(request):
    total_courses = Courses.objects.count()
    total_tutors = Courses.objects.values('tutor').distinct().count()
    return {'total_courses': total_courses, 'total_tutors': total_tutors}