from django.contrib import admin
from .models import User, Company, Job, Application, Review, Profile

admin.site.register(User)
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Review)
admin.site.register(Profile)