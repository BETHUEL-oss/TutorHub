from django import forms
from .models import Course, CourseImage
from django.utils.text import slugify

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "subject", "name", "description", "price", "unit",
            "stock_quantity", "available", "in_stock",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Auto-generate slug:
        if not instance.slug:
            instance.slug = slugify(instance.name)

        if commit:
            instance.save()
        return instance


class CourseImageForm(forms.ModelForm):
    class Meta:
        model = CourseImage
        fields = ["image", "caption", "is_primary"]