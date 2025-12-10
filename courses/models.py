from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class Level(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)  # lucide icon name
    slug = models.SlugField(unique=True)

    def _str_(self):
        return self.name


class Courses(models.Model):
    UNIT_CHOICES = [
        ('English', 'per lesson'),
        ('Kiswahili', 'per lesson'),
        ('Religious Education', 'per lesson'),
        ('Science & Technology', 'per lesson'),
        ('Agriculture & Nutrition', 'per lesson'),
        ('Social Studies', 'per lesson'),
        ('Creative Arts & Sports', 'per lesson'),
    ]

    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subjects = models.CharField(max_length=50, choices=UNIT_CHOICES)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_primary_image(self):
        primary = self.images.filter(is_primary=True).first()
        return primary if primary else self.images.first()

    def _str_(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class CoursesImage(models.Model):
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='courses/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_primary', 'id']