
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import TutorProfile, PupilProfile

# Register your models here.

class TutorProfileInline(admin.StackedInline):
    model = TutorProfile
    can_delete = False
    verbose_name = "Tutor Profile"
    verbose_name_plural = "Tutor Profile"

class PupilProfileInline(admin.StackedInline):
    model = PupilProfile
    can_delete = False
    verbose_name = "Pupil Profile"
    verbose_name_plural = "Pupil Profile"

class UserAdmin(BaseUserAdmin):
    inlines = (TutorProfileInline, PupilProfileInline)

    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        return super().get_inlines(request, obj)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
