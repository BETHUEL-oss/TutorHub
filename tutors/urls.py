from django.urls import path
from .views import TutorListView, TutorDetailView
from . import views

urlpatterns = [
    path('tutors/', TutorListView.as_view(), name='tutor_list'),
    path('tutors/<int:pk>/', TutorDetailView.as_view(), name='tutor_detail'),
    path("dashboard/", views.tutor_dashboard, name='tutor_dashboard'),
]