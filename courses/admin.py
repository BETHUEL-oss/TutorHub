from django.contrib import admin
from .models import Level, Courses, CoursesImage

# Register your models here.
class CoursesImageInline(admin.TabularInline):
    model = CoursesImage
    extra = 1
    max_num = 10

@admin.register(Level)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ['name', 'tutor', 'price', 'available']
    list_filter = ['available', 'level']
    inlines = [CoursesImageInline]

@admin.register(CoursesImage)
class CoursesImageAdmin(admin.ModelAdmin):
    list_display = ['courses', 'image']