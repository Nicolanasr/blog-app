from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from .models import Tags, Post, Comments, LikesUsers, User, ViewedPost
from authentication.models import Profile, FollowModel
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
import datetime


# ~ To add test data to  database
# for i in range(0, 100):
#         profiles = Profile.objects.all()
#         random_profile = random.choice(profiles)

#         title = "title demo" + str(i)
#         views = random.randint(0, 500)
#         views_for_algo = random.randint(1,views+1)
#         likes = random.randint(0, views_for_algo)

#         post = Post(title=title,
#             author=random_profile,
#             content="Just content",
#             likes=likes,
#             views=views,
#             views_for_algo=views_for_algo,
#             thumbnail="https://www.cameraegg.org/wp-content/uploads/2016/01/Nikon-D500-Sample-Images-2.jpg"
#             )
#         post.save()

# for i in range(0, profiles.count()):
#     profile_to_follow = random.choice(profiles)

#     profile = random.choice(profiles)
#     follower, created = FollowModel.objects.get_or_create(follower=profile)

#     # making sure the user can't follow himself
    
#     if profile == profile_to_follow:
#         continue

#     follower.following.add(profile_to_follow)

#     profile_to_follow_follow_model, created = FollowModel.objects.get_or_create(follower=profile_to_follow)
#     profile_to_follow_follow_model.followers.add(profile)

def index(request):
    if request.user.is_authenticated:
        for post in Post.objects.all():
            try:
                if post.views_for_algo >= (post.views * 15) / 100:
                    rank = (post.likes * 100) / post.views_for_algo
                else:
                    rank = 0.0
            except:
                rank = 0.0
            Post.objects.select_for_update().filter(id=post.id).update(rank=rank)

        date_before_week = datetime.date.today()-datetime.timedelta(days=7)
        
        popular_posts = Post.objects.filter(created_at__gte=date_before_week).order_by('-rank')[:4]
        expected_views = Profile.objects.count() * 10 / 100
        
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


        ctx = {'posts': posts_of_following, 'popular_posts': popular_posts, 'expected_views': expected_views}
        return render(request, 'index/index.html', ctx)
    else:
        return redirect('authentication:login')


def discover(request):
    tags = Tags.objects.all()
    return render(request, 'index/discover.html', {'tags': tags})


# To display the most popular posts based on posts views / likes algorithm
def popular(request):
    if request.user.is_authenticated:
        date_before_week = datetime.date.today()-datetime.timedelta(days=7)
        for post in Post.objects.all():
            try:
                if post.views_for_algo >= (post.views * 15) / 100:
                    rank = (post.likes * 100) / post.views_for_algo
                else:
                    rank = 0.0
            except:
                rank = 0.0
            Post.objects.select_for_update().filter(id=post.id).update(rank=rank)
        
        
        posts = Post.objects.filter(created_at__gte=date_before_week).order_by('-rank')[:20]
        expected_views = Profile.objects.count() * 10 / 100

        ctx = {'posts': posts, 'expected_views': expected_views}
        return render(request, 'index/popular.html', ctx)
    else:
        messages.error(request, 'please sign in to view this page')
        return redirect('index:index')


def discover_tags(request, tag):
    try:
        tag = Tags.objects.get(tag_name__iexact=tag)
    except Tags.DoesNotExist:
        messages.error(request, "Tag couldn't be found")
        return redirect('index:discover')
    
    posts = Post.objects.filter(tags=tag)

    ctx = {'tag': tag, 'posts': posts}
    return render(request, 'index/discover_tags.html', ctx)


# Get the latest posted posts
def newly_posted(request):
    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'index/newly_posted.html', {'posts': posts})


def most_liked(request):
    date_before_week = datetime.date.today()-datetime.timedelta(days=7)

    posts = Post.objects.filter(created_at__gte=date_before_week).order_by('-likes')[:50]

    return render(request, 'index/most_liked.html', {'posts': posts})


def random_profile(request):
    current_profile = Profile.objects.get(user=request.user)
    random_profile = current_profile

    profiles = Profile.objects.all()
    while random_profile is current_profile:
        random_profile = random.choice(profiles)
    
    return redirect('index:user_profile', random_profile)


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


    viewd_post, created = ViewedPost.objects.get_or_create(post=post, Profile=profile)
    print(viewd_post, created)

    post_views = post.views
    post_views = post_views + 1
    post_views_for_algo = post.views_for_algo
    if created:
        post_views_for_algo = post_views_for_algo + 1
    
    Post.objects.select_for_update().filter(id=post_id).update(views=post_views, views_for_algo=post_views_for_algo)

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
    follow_model = FollowModel.objects.get(follower=following_user_profile)
    following = follow_model.following.all()
    follower = follow_model.follower

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

    visited_user = FollowModel.objects.get(follower=profile)
    following = visited_user.following.all()
    followers = visited_user.followers.all()

    ctx = {'users_posts': users_posts, 'shared_posts': shared_posts, 'profile': profile, 'is_following': is_following, 'is_same': is_same, 'following': following, 'followers': followers}
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


def search_form(request):
    query = request.GET.get('query')
    return redirect('index:search', query)


def search(request, query):
    found = []
    results_dic = {'profiles': [], "post_title": [], "post_content": []}

    try:
        user = User.objects.filter(username__icontains=query)
        for u in user:
            profile = Profile.objects.filter(user=u)
            found.append(profile[0])
            results_dic['profiles'].append(profile[0])
    except User.DoesNotExist:
        profile = ""

    try:
        post = Post.objects.filter(title__icontains=query)
    except:
        post = ""
    
    for p in post:
        found.append(p)
        results_dic['post_title'].append(p)

    try:
        post_content = Post.objects.filter(content__icontains=query)
    except:
        post = ""
    
    for p in post_content:
        results_dic['post_content'].append(p)

    ctx =  {'found': found, 'results_dic': results_dic, 'query': query}
    return render(request, 'index/search_res.html', ctx)