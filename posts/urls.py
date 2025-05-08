from django.urls import path
from .views import LikePostView

urlpatterns = [
    path('likes/<int:post_id>/', LikePostView.as_view(), name='like-post'),
]