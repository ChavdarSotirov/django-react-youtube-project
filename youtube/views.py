from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

from core.clean_up import clean_up_files
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
            return redirect('user videos')

        context = {
            'form': form,
            'pet': video,
        }

        return render(request, f'upload_video.html', context)


class MyVideosListView(ListView):
    template_name = 'user-videos.html'
    model = Video

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.all()
        return context


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
            return redirect('user videos')

        context = {
            'form': form,
            'video': video,
        }

        return render(request, f'edit_video.html', context)


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
        return redirect('user videos')


def check_or_comment_video(request, pk):
    video = Video.objects.get(pk=pk)
    if request.method == 'GET':
        context = {
            'video': video,
            'form': CommentForm(),
        }
        return render(request, 'check-or-comment-video.html', context)
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(text=form.cleaned_data['text'])
            comment.video = video
            comment.save()
            return redirect('check or comment video', pk)

        context = {
            'video': video,
            'form': form,
        }
        return render(request, 'check-or-comment-video.html', context)


def like_video(request, pk):
    video = Video.objects.get(pk=pk)
    like = Like(test=str(pk))
    like.video = video
    like.save()
    return redirect('check or comment video', pk)
