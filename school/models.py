from django.db import models
from django.utils import timezone

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Show on the website")

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title


class GalleryCategory(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Gallery Categories"

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} - {self.caption or 'Image'}"


class AdmissionApplication(models.Model):
    PROGRAM_CHOICES = [
        ('1', 'Early Years (Age 2-3)'),
        ('2', 'Nursery (Age 3-4)'),
        ('3', 'Kindergarten (Age 4-6)'),
        ('4', 'Day Care (Age 2-6)'),
    ]
    child_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    parent_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    program = models.CharField(max_length=1, choices=PROGRAM_CHOICES)
    message = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.child_name} - {self.get_program_display()}"


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    image = models.ImageField(upload_to='events/', null=True, blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title
        
    @property
    def is_past(self):
        from datetime import date
        return self.date < date.today()


class Enquiry(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"Enquiry from {self.name}"


class ActivityUpdate(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='activities/')
    date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "Daily Activity Update"
        verbose_name_plural = "Daily Activity Updates"
        ordering = ['-date']

    def __str__(self):
        return self.title


class VideoEmbed(models.Model):
    title = models.CharField(max_length=200)
    youtube_url = models.URLField(help_text="Full YouTube URL")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
        
    def get_embed_url(self):
        import re
        match = re.search(r'(?:v=|youtu\.be/|embed/|shorts/)([^&?]+)', self.youtube_url)
        if match:
            video_id = match.group(1).replace('/', '')
            return f"https://www.youtube.com/embed/{video_id}"
        return self.youtube_url


class Student(models.Model):
    name = models.CharField(max_length=150)
    age = models.IntegerField()
    program_enrolled = models.CharField(max_length=200)
    parent_name = models.CharField(max_length=150)
    parent_email = models.EmailField(blank=True)
    parent_phone = models.CharField(max_length=20)
    enrolled_date = models.DateField(default=timezone.now)
    photo = models.ImageField(upload_to='students/', blank=True, null=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='teachers/')

    def __str__(self):
        return self.name
