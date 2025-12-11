from django.urls import path
from . import views
from .views import HomePageView, CourseListView, CourseDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('course/<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('cart/add/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path("teacher/dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("add/", views.add_course, name="add_course"),
    path("edit/<int:pk>/", views.edit_course, name="edit_course"),
    path("delete/<int:pk>/", views.delete_course, name="delete_course"),
    path("mpesa_pay/", views.mpesa_pay, name="mpesa_pay"),
]