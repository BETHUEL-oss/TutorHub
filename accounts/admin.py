from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import TutorProfile, StudentProfile

# Register your models here.

class TutorProfileInline(admin.StackedInline):
    model = TutorProfile
    can_delete = False
    verbose_name = "Tutor Profile"
    verbose_name_plural = "Tutor Profile"

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name = "Student Profile"
    verbose_name_plural = "Student Profile"

class UserAdmin(BaseUserAdmin):
    inlines = (TutorProfileInline, StudentProfileInline)

    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        return super().get_inlines(request, obj)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)