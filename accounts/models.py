from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_profile')
    # farm_name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=11, blank=True)
    is_verified = models.BooleanField(default=False, help_text='Checked by admin to confirm farm identity')
    business_license = models.FileField(upload_to='vendor_docs/', blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='vendor_profiles/', null=True, blank=True)
    certification = models.TextField(blank=True)

    def _str_(self):
        return self.user

    def get_absolute_url(self):
        return reverse('tutor_profile', kwargs={'pk': self.pk})

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='consumer_profile')
    phone_number = models.CharField(max_length=11, blank=True)
    location = models.CharField(max_length=200, blank=True)

    def _str_(self):
        return f"{self.user.username}'s Profile"