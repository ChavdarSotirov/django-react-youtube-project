from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

from core.clean_up import clean_up_files
from core.decorators import allowed_users
from youtube.forms import VideoCreationForm, CommentForm
from youtube.models import Video, Like, Comment


class IndexTemplateView(TemplateView):
    template_name = 'index.html'


class ItemListView(ListView):
    template_name = 'video-page.html'
    model = Video
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.all()
        return context


@login_required(login_url='register user')
def upload_video(request):
    video = Video()
    if request.method == 'GET':
        form = VideoCreationForm()
        context = {
            'form': form,
            'video': video,
        }

        return render(request, f'upload_video.html', context)
    else:
        form = VideoCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('current user profile')

        context = {
            'form': form,
            'video': video,
        }

        return render(request, f'upload_video.html', context)


@login_required(login_url='register user')
def edit_video_view(request, pk):
    video = Video.objects.get(pk=pk)
    if request.method == 'GET':
        form = VideoCreationForm(instance=video)
        context = {
            'form': form,
            'video': video,
        }

        return render(request, f'edit_video.html', context)
    else:
        form = VideoCreationForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('current user profile')

        context = {
            'form': form,
            'video': video,
        }

        return render(request, f'edit_video.html', context)


@login_required(login_url='register user')
def delete_video(request, pk):
    video = Video.objects.get(pk=pk)
    if request.method == 'GET':
        context = {
            'video': video,
        }

        return render(request, 'video-delete.html', context)
    else:
        clean_up_files(video.image.path)
        clean_up_files(video.video_file.path)
        video.delete()
        return redirect('current user profile')


@login_required(login_url='register user')
def check_or_comment_video(request, pk):
    video = Video.objects.get(pk=pk)
    if request.method == 'GET':
        context = {
            'user': request.user,
            'video': video,
            'form': CommentForm(),
            'can_delete': request.user == video.user.user,
            'can_edit': request.user == video.user.user,
            'can_like': request.user != video.user.user,
            'has_liked': video.like_set.filter(user_id=request.user.userprofile.id).exists(),
            'can_comment': request.user != video.user.user,
        }
        return render(request, 'check-or-comment-video.html', context)
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(text=form.cleaned_data['text'])
            comment.video = video
            comment.user = request.user.userprofile
            comment.save()
            return redirect('check or comment video', pk)

        context = {
            'video': video,
            'form': form,
        }
        return render(request, 'check-or-comment-video.html', context)


@login_required(login_url='register user')
def like_video(request, pk):
    like = Like.objects.filter(user_id=request.user.userprofile.id, video_id=pk).first()
    if like:
        like.delete()
    else:
        video = Video.objects.get(pk=pk)
        like = Like(user=request.user.userprofile)
        like.video = video
        like.save()
    return redirect('check or comment video', pk)

@login_required(login_url='register user')
@allowed_users(allowed_roles=['admin'])
def admin_page(request):
    if request.method == 'GET':
        context = {
            'videos': Video.objects.all()
        }
        return render(request, 'admin-page.html', context)


class SearchResultsView(ListView):
    template_name = 'video-page.html'
    model = Video

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Video.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        return object_list
