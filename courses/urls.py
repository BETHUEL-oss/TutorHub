from django.urls import path
from . import views
from .views import HomePageView, CoursesListView, CoursesDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('courses/', CoursesListView.as_view(), name='courses_list'),
    path('courses/<slug:slug>/', CoursesDetailView.as_view(), name='courses_detail'),
    path('cart/add/<int:courses_id>/', views.add_to_cart, name='add_to_cart'),
    path("tutor/dashboard/", views.tutor_dashboard, name="tutor_dashboard"),
    path("add/", views.add_courses, name="add_courses"),
    path("edit/<int:pk>/", views.edit_courses, name="edit_courses"),
    path("delete/<int:pk>/", views.delete_courses, name="delete_courses"),
    path("mpesa_pay/", views.mpesa_pay, name="mpesa_pay"),
]