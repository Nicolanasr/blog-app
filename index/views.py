from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from .models import Tags, Post, Comments, LikesUsers, User
from authentication.models import Profile
from django.contrib import messages


def index(request):
    posts = Post.objects.all()
    ctx = {'posts': posts}
    return render(request, 'index/index.html', ctx)


def post_details(request, post_id):
    has_liked = False
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        messages.error(request, "The post you are looking for is not available!")
        return redirect('index:index')
    profile = Profile.objects.get(user=request.user)
    try:
        user_like = LikesUsers.objects.get(user=profile, post=post)
        has_liked = True
    except:
        user_like = ""
        has_liked = False

    print(user_like)
    ctx = {'post': post, 'user_like': user_like, 'has_liked': has_liked}
    return render(request, 'index/post_details.html', ctx)


def new_post(request):
    tags = Tags.objects.all()
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        # Get submitted title, content and tags
        title = request.POST.get('title')
        content = request.POST.get('content')
        post_tags = request.POST.getlist('tags')  # Get all submitted tags as a list

        post = Post(title=title, content=content, author=profile)
        post.save()
        # Getting the tag by its id and adding it to the 'post'
        for tag in post_tags:
            post.tags.add(Tags.objects.get(id=tag))

    ctx = {'tags': tags}
    return render(request, 'index/new_post.html', ctx)


def post_like(request, post_id):
    # Take ajax request and add/remove like to add post
    if request.is_ajax():
        # Check the post requested is available
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return redirect("index:index")

        prof = Profile.objects.get(user=request.user)
        # Check if the user has already liked/disliked the post
        try:
            liked = LikesUsers.objects.get(user=prof, post=post)
            is_liked = True
            is_liked_value = liked.value
        except LikesUsers.DoesNotExist:
            is_liked = False

        like_value = request.POST.get('like_value')
        curr_likes = post.likes

        # Raise 404 if user already liked
        if like_value == 'like' and not is_liked:
            print('liking')
            new_likes = curr_likes + 1
            Post.objects.select_for_update().filter(id=post_id).update(likes=new_likes)
            LikesUsers(user=prof, post=post, value=+1).save()
        elif like_value == 'dislike' and not is_liked:
            new_likes = curr_likes - 1
            Post.objects.select_for_update().filter(id=post_id).update(likes=new_likes)
            LikesUsers(user=prof, post=post, value=-1).save()
        # Checking if the user has already disliked the post and want to like it (and vice versa)
        elif is_liked and is_liked_value == -1 and like_value == "like":
            new_likes = curr_likes + 1
            Post.objects.select_for_update().filter(id=post_id).update(likes=new_likes)
            LikesUsers.objects.filter(user=prof, post=post, value=-1).delete()
        elif is_liked and is_liked_value == +1 and like_value == "dislike":
            new_likes = curr_likes - 1
            Post.objects.select_for_update().filter(id=post_id).update(likes=new_likes)
            LikesUsers.objects.filter(user=prof, post=post, value=+1).delete()
        else:
            raise Http404('404')

        data = {'': like_value}
        return JsonResponse(data)


# User profile (to see all posted posts)
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    users_posts = profile.post_set.all()

    ctx = {'users_posts': users_posts}
    return render(request, 'index/user_profile.html', ctx)

