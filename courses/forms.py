from django import forms
from .models import Courses, CoursesImage
from django.utils.text import slugify

class CoursesForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = [
            "level", "name", "description", "price", "subjects",
             "available",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Auto-generate slug:
        if not instance.slug:
            instance.slug = slugify(instance.name)

        if commit:
            instance.save()
        return instance


class CoursesImageForm(forms.ModelForm):
    class Meta:
        model = CoursesImage
        fields = ["image", "caption", "is_primary"]