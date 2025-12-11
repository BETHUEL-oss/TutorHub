from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.tutor_dashboard, name='tutor_dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.custom_login, name='login'),
    path('register/student/', views.register_student, name='register_student'),
    path("register/teacher/", views.register_teacher, name="register_teacher"),
]