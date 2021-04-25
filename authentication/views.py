from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from .forms import CreateUserForm, ChangeUserForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import FollowModel, User, Profile


def account(request):
    errors = []
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    if request.method == "POST":
        form = ChangeUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            err = form.errors.values()
            errors = list(err)
            print(errors)
            messages.error(request, errors[0])
            return redirect('authentication:account')
    form = ChangeUserForm(instance=request.user)
    ctx = {'form': form}
    return render(request, 'authentication/account.html', ctx)


# user registration views
def registration(request):
    if request.user.is_authenticated:
        messages.warning(request, "User already logged in!")
        return redirect('authentication:account')
    form = CreateUserForm()
    ctx = {'form': form}
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password1')
            form.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('index:index')
        else:
            err = form.errors.values()
            errors = list(err)
            ctx = {'form': form, 'errors': errors}
    return render(request, 'authentication/registration.html', ctx)


# user login views
def login_page(request):
    if request.user.is_authenticated:
        messages.warning(request, "User already logged in!")
        return redirect('authentication:account')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('index:index')
        else:
            messages.warning(request, 'Username or Password are incorrect')

    return render(request, 'authentication/login.html')


def logout_page(request):
    logout(request)
    return redirect('authentication:login')


def change_password(request):
    form = PasswordChangeForm(request.user)
    ctx = {'form': form}
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
        else:
            err = form.errors.values()
            errors = list(err)
            ctx = {'form': form, 'errors': errors}
            messages.error(request, errors[0])

    return render(request, 'authentication/change_password.html', ctx)


def follow(request, user_to_follow):
    #TODO transform to ajax
    try:
        user = User.objects.get(username=user_to_follow)
        profile_to_follow = Profile.objects.get(user=user)
    except User.DoesNotExist:
        messages.error(request, "Error! User with username " + str(user_to_follow) + " does not exist")
        return redirect('index:index')

    profile = Profile.objects.get(user=request.user)
    follower, created = FollowModel.objects.get_or_create(follower=profile)

    # making sure the user can't follow himself
    
    if profile == profile_to_follow:
        messages.error(request, 'You cannot follow yourself')
        return redirect('index:index')

    follower.following.add(profile_to_follow)

    profile_to_follow_follow_model, created = FollowModel.objects.get_or_create(follower=profile_to_follow)
    profile_to_follow_follow_model.followers.add(profile)
    try:
        return redirect(request.META.get('HTTP_REFERER'))
    except:
        return redirect('index:index')


def unfollow(request, user_to_unfollow):
    #TODO transform to ajax
    try:
        user = User.objects.get(username=user_to_unfollow)
        profile_to_follow = Profile.objects.get(user=user)
    except User.DoesNotExist:
        messages.error(request, "Error! User with username " + str(user_to_unfollow) + " does not exist")
        return redirect('index:index')

    profile = Profile.objects.get(user=request.user)
    follower, created = FollowModel.objects.get_or_create(follower=profile)

    # making sure the user can't unfollow himself
    if profile == profile_to_follow:
        messages.error(request, 'You cannot unfollow yourself')
        return redirect('index:index')
        
    follower.following.remove(profile_to_follow)

    profile_to_follow_follow_model, created = FollowModel.objects.get_or_create(follower=profile_to_follow)
    profile_to_follow_follow_model.followers.remove(profile)
    try:
        return redirect(request.META.get('HTTP_REFERER'))
    except:
        return redirect('index:index')
