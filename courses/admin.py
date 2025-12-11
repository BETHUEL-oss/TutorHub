from django.contrib import admin
from .models import Subject, Course, CourseImage

# Register your models here.
class CourseImageInline(admin.TabularInline):
    model = CourseImage
    extra = 1
    max_num = 10

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'price', 'available']
    list_filter = ['available', 'subject']
    inlines = [CourseImageInline]

@admin.register(CourseImage)
class CourseImageAdmin(admin.ModelAdmin):
    list_display = ['course', 'image']