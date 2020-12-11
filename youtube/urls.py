from django.urls import path

from youtube.views import IndexTemplateView, ItemListView, upload_video, MyVideosListView, edit_video_view, \
    delete_video, like_video, check_or_comment_video

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index page'),
    path('videos/', ItemListView.as_view(), name='list videos page'),
    path('my_videos/', MyVideosListView.as_view(), name='user videos'),


    # CRUD
    path('upload_video/', upload_video, name='video upload'),
    path('edit_video/<int:pk>/', edit_video_view, name='edit video'),
    path('delete_video/<int:pk>/', delete_video, name='delete video'),


    path('like/<int:pk>/', like_video, name='like video'),
    path('video/<int:pk>/', check_or_comment_video, name='check or comment video'),
]
