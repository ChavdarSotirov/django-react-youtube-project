from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from auth_youtube.forms.ProfileFormUploadImage import ProfileFormUploadImage
from auth_youtube.forms.SignUpForm import SignUpForm
from auth_youtube.models import UserProfile
from core.decorators import unauthenticated_user, allowed_users


def user_profile(request, pk=None):
    user = request.user if pk is None else User.objects.get(pk=pk)
    if request.method == 'GET':
        context = {
            'profile_user': user,
            'videos': user.userprofile.video_set.all(),
            'profile': user.userprofile,
            'form': ProfileFormUploadImage(),
            'can_crud': request.user != user
        }
        return render(request, 'registration/user_profile.html', context)
    else:
        form = ProfileFormUploadImage(request.POST, request.FILES, instance=user.userprofile)

        if form.is_valid():
            form.save()
            return redirect('current user profile')
        return redirect('current user profile')


@unauthenticated_user
def register_user(request):
    if request.method == 'GET':
        context = {
            'form': SignUpForm()
        }
        return render(request, 'register/register.html', context)
    else:
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            profile = UserProfile(user=user)
            profile.save()
            return redirect('index page')
        context = {
            'form': form,
        }
        return render(request, 'register/register.html', context)


def sighout_user(request):
    logout(request)
    return redirect('index page')



