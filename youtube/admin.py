from django.contrib import admin

# Register your models here.
from youtube.models import Video, Like

admin.site.register(Video)
admin.site.register(Like)