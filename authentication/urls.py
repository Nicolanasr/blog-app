from django.urls import path
from . import views

app_name = "authentication"

urlpatterns = [
    path('', views.account, name="account"),
    path('register/', views.registration, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('change_password/', views.change_password, name="change_password"),
]
