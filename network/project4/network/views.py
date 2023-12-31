from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow


def index(request):
    all_posts = Post.objects.all().order_by("id").reverse()

    # Pagination
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "all_posts": all_posts,
        "posts_of_the_page": posts_of_the_page
    })


def new_post(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse(index))
    

def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    all_posts = Post.objects.filter(user=user).order_by("id").reverse()

    following = Follow.objects.filter(user_following=user)
    followers = Follow.objects.filter(user_followed=user)

    try:
        check_follow = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(check_follow) == 0:
            is_following = False
        else:
            is_following = True
    except:
        is_following = False

    # Pagination
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "all_posts": all_posts,
        "posts_of_the_page": posts_of_the_page,
        "username": user.username,
        "following": following,
        "followers": followers,
        "is_following": is_following,
        "user_profile": user
    })


def follow(request):
    user_follow = request.POST['user_follow']
    current_user = User.objects.get(pk=request.user.id)
    user_follow_data = User.objects.get(username=user_follow)
    f = Follow(user_following=current_user, user_followed=user_follow_data)
    f.save()
    user_id = user_follow_data.id 
    return HttpResponseRedirect(reverse(profile, kwargs={"user_id": user_id}))


def unfollow(request):
    user_follow = request.POST['user_follow']
    current_user = User.objects.get(pk=request.user.id)
    user_follow_data = User.objects.get(username=user_follow)
    f = Follow.objects.get(user_following=current_user, user_followed=user_follow_data)
    f.delete()
    user_id = user_follow_data.id 
    return HttpResponseRedirect(reverse(profile, kwargs={"user_id": user_id}))



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
