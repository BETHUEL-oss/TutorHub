from django.shortcuts import render
from django.views.generic import ListView, DetailView
from accounts.models import TutorProfile
from courses.models import Courses

# Create your views here.

class TutorListView(ListView):
    model =TutorProfile
    template_name = 'tutors/tutor_list.html'
    context_object_name = 'tutors'
    # queryset =
    # TutorProfile.objects.filter(user__is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_farmers'] = Courses.objects.values('tutor').distinct().count()
        return context

class TutorDetailView(DetailView):
    model = TutorProfile
    template_name = 'tutors/tutor_detail.html'
    context_object_name = 'tutor'

    def get_context_data(self, **kwargs):
        context = super(TutorDetailView, self).get_context_data(**kwargs)
        tutor = self.get_object()
        tutor_user = tutor.user

        context['courses'] = Courses.objects.filter(tutor=tutor_user, available=True).order_by('-created_at')
        return context

def tutor_dashboard(request):
    return render(request, 'tutors/tutor_dashboard.html')