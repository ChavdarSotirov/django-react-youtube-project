from django.urls import path

from youtube.views import IndexTemplateView, ItemListView, upload_video, edit_video_view, \
    delete_video, like_video, check_or_comment_video, admin_page, SearchResultsView

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index page'),
    path('videos/', ItemListView.as_view(), name='list videos page'),


    # CRUD
    path('upload_video/', upload_video, name='video upload'),
    path('edit_video/<int:pk>/', edit_video_view, name='edit video'),
    path('delete_video/<int:pk>/', delete_video, name='delete video'),


    path('like/<int:pk>/', like_video, name='like video'),
    path('video/<int:pk>/', check_or_comment_video, name='check or comment video'),
    path('admin_panel/', admin_page, name='admin page'),

    path('seach/', SearchResultsView.as_view(), name='search_results'),

]
