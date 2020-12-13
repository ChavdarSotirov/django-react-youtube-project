from django.contrib.auth.models import User
from django.db import models

from auth_youtube.models import UserProfile


class Video(models.Model):
    title = models.CharField(blank=False, max_length=50)
    description = models.TextField(blank=False, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(blank=False, upload_to='videos/')
    image = models.ImageField(upload_to='images/', blank=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, {self.created_at}'



class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

