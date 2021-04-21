from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from .models import Tags, Post, Comments, LikesUsers, User
from authentication.models import Profile, FollowModel
from django.contrib import messages


def index(request):
    posts = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    follow_model = FollowModel.objects.get(follower=profile)

    following = []
    for fl in follow_model.following.all():
        following.append(fl)
    
    posts_of_following = []
    # append all the posts from profiles that the user follow 
    for post in posts:
        if post.author in following and post.shared == False: # To not add the shared posts from profiles that the user does not follow but he follow the original author
            posts_of_following.append(post)
        elif post.shared == True and post.shared_by in following:  # To also add shared posts by profiles he follows
            posts_of_following.append(post)

    ctx = {'posts': posts_of_following}
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

    comments = Comments.objects.filter(post=post)

    # Get all the profiles the user is following
    follower = FollowModel.objects.get(follower=profile)
    following = follower.following.all()
    follower = follower.follower

    # Check if the user is following the author of the original post
    if post.author in following and post.author != follower: # Making sure the user can't unfollow himself
        is_following = True
        is_same = False
    elif post.author == follower:
        is_following = False
        is_same = True
    else:
        is_following = False
        is_same = False


    ctx = {'post': post, 'user_like': user_like, 'has_liked': has_liked, 'comment': comments, 'is_following': is_following, 'is_same': is_same}
    return render(request, 'index/post_details.html', ctx)


def new_post(request):
    tags = Tags.objects.all()
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        # Get submitted title, content and tags
        title = request.POST.get('title')
        content = request.POST.get('content')
        thumbnail = request.POST.get('image')
        post_tags = request.POST.getlist('tags')  # Get all submitted tags as a list

        post = Post(title=title, content=content, author=profile, thumbnail=thumbnail)
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
def user_profile(request, profile):
    try:
        user = User.objects.get(username=profile)
        profile = Profile.objects.get(user=user)
    except User.DoesNotExist:
        messages.error(request, "This user does not exits")
        return redirect("index:index")

    users_posts = profile.post_set.filter(shared=False)
    try:
        shared_posts = Post.objects.filter(shared=True, shared_by=profile)
    except:
        shared_posts = ""

    # Get all the profiles the user is following
    following_user = User.objects.get(username=request.user)
    following_user_profile = Profile.objects.get(user=following_user)
    follower = FollowModel.objects.get(follower=following_user_profile)
    following = follower.following.all()
    follower = follower.follower

    # Check if the user is following the author of the original post
    if profile in following and profile != follower: # Making sure the user can't unfollow himself
        is_following = True
        is_same = False
    elif profile == follower:
        is_following = False
        is_same = True
    else:
        is_following = False
        is_same = False

    ctx = {'users_posts': users_posts, 'shared_posts': shared_posts, 'profile': profile, 'is_following': is_following, 'is_same': is_same}
    return render(request, 'index/user_profile.html', ctx)


def share_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        messages.error(request, "this post does not exist")
        return redirect('index:index')

    profile = Profile.objects.get(user=request.user)
    title = post.title
    content = post.content
    thumbnail = post.thumbnail
    post_tags = post.tags

    post = Post(title=title, content=content, author=post.author, thumbnail=thumbnail, shared=True, shared_by=profile,
                shared_post_id=post.id)
    post.save()
    # # Getting the tag by its id and adding it to the 'post'
    for tag in post_tags.all():
        post.tags.add(tag)

    return redirect('index:index')


def post_comment(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            messages.error(request, 'post does not exist')
            return redirect('index:index')

        try:
            user = User.objects.get(username=request.user)
            profile = Profile.objects.get(user=user)
        except:
            messages.error(request, 'Oops, something went wrong!')
            return redirect('index:index')
        
        content = request.POST.get('content')

        comment = Comments(author=profile, content=content, post=post)
        comment.save()
        return redirect('index:post_details', post_id)

    else:
        messages.error(request, 'Oops, something went wrong!')
        return redirect('index:index')