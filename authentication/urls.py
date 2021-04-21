from django.urls import path
from . import views

app_name = "authentication"

urlpatterns = [
    path('', views.account, name="account"),
    path('register/', views.registration, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('change_password/', views.change_password, name="change_password"),
    path('follow/<str:user_to_follow>', views.follow, name="follow"),
    path('unfollow/<str:user_to_unfollow>', views.unfollow, name="unfollow"),
]
