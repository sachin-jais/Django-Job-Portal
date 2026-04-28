
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    is_jobseeker = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

class Company(models.Model):
    employer = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to='company_logos/')
    location = models.CharField(max_length=100)

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return sum(r.rating for r in reviews) / reviews.count()
        return 0

class Job(models.Model):
    JOB_TYPES = (('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Remote', 'Remote'))
    EXP_LEVELS = (('Entry', 'Entry'), ('Mid', 'Mid'), ('Senior', 'Senior'))
    
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.PositiveIntegerField(null=True, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    experience_level = models.CharField(max_length=20, choices=EXP_LEVELS)
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    resume = models.FileField(upload_to='resumes/')
    skills = models.CharField(max_length=500)
    saved_jobs = models.ManyToManyField(Job, blank=True, related_name='saved_by')

class Application(models.Model):
    STATUS = (('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected'))
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    jobseeker = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='applications/')
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    applied_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')
    jobseeker = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
