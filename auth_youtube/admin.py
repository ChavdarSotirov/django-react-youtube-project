from django.contrib import admin

# Register your models here.
from auth_youtube.models import UserProfile

admin.site.register(UserProfile)