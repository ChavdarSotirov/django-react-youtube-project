from django import forms

from auth_youtube.models import UserProfile


class ProfileFormUploadImage(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture',)