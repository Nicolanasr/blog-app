from django.urls import path
from . import views

app_name = 'index'

urlpatterns = [
    path('', views.index, name="index"),
    path('post/<int:post_id>', views.post_details, name="post_details"),
    path('new_post/', views.new_post, name="new_post"),
    path('like/<int:post_id>', views.post_like, name="post_like"),
    path('user_profile/<str:profile>', views.user_profile, name="user_profile"),
    path('share_post/<int:post_id>', views.share_post, name="share_post"),
]
