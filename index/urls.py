from django.urls import path
from . import views

app_name = 'index'

urlpatterns = [
    path('', views.index, name="index"),
    path('discover', views.discover, name="discover"),
    path('discover/popular', views.popular, name="popular"),
    path('discover/tags/<str:tag>', views.discover_tags, name="discover_tags"),
    path('discover/newly_posted', views.newly_posted, name="newly_posted"),
    path('discover/most_liked', views.most_liked, name="most_liked"),
    path('discover/random_profile', views.random_profile, name="random_profile"),
    path('post/<int:post_id>', views.post_details, name="post_details"),
    path('new_post/', views.new_post, name="new_post"),
    path('like/<int:post_id>', views.post_like, name="post_like"),
    path('user_profile/<str:profile>', views.user_profile, name="user_profile"),
    path('share_post/<int:post_id>', views.share_post, name="share_post"),
    path('post_comment/<int:post_id>', views.post_comment, name="post_comment"),
    path('search/', views.search_form, name="search_form"),
    path('search/<str:query>', views.search, name="search"),

]
