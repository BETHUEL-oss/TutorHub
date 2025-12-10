from django.db import models

# Create your models here.

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=120, default="TutorHub")
    is_maintenance_mode = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def save(self, *args, **kwargs):
        if self.pk is None and SiteSetting.objects.exists():
            raise Exception("Only one SiteSetting instance can be created.")
        return super(SiteSetting, self).save(*args, **kwargs)

    def _str_(self):
        return 'Global Site Settings'

class ContactInfo(models.Model):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, blank=True)
    support_hours = models.CharField(max_length=50, blank=True, default='Monday-Sunday: 6:00AM - 6:00PM')

    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"

    def _str_(self):
        return f"Contact Info: {self.email}"