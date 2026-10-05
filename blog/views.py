from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Profile, Comment, Reaction
from django.core.paginator import Paginator
from django.db.models import Q



def home(request):

    search_query = request.GET.get('q', '').strip()

    posts_list = Post.objects.filter(
        is_deleted=False,
        is_published=True
    )

    if search_query:
        posts_list = posts_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    posts_list = posts_list.order_by('-created_at')

    paginator = Paginator(posts_list, 6)

    page_number = request.GET.get('page')

    posts = paginator.get_page(page_number)

    return render(
        request,
        'home.html',
        {
            'posts': posts,
            'search_query': search_query,
        }
    )

@csrf_exempt
def login_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')
        
        return render(request, 'login.html', {
            'msg': 'Invalid username or password!'
        })

    return render(request, 'login.html')

@csrf_exempt
def signup(request):
    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        profile_pic = request.FILES.get('profile_pic')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                'msg': 'Username already exists.'
            })

        if password != confirm_password:
            return render(request, 'signup.html', {
                'msg': 'Passwords do not match.'
            })

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )

        Profile.objects.create(
            user=user,
            profile_pic=profile_pic
        )

        return redirect('login')

    return render(request, 'signup.html')


@login_required(login_url='login')
def logout_(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    return render(request, 'profile.html', {
        'profile': profile
    })

@login_required(login_url='login_')
def reset_password(request):
    if request.method=='POST':
        if 'old' in request.POST:
            uname=request.POST['username']
            old=request.POST['old']
            u=authenticate(username=uname,password=old)
            print(u)
            if u:
                return render(request,'reset_password.html',{'new_pass':True})
            else:
                return render(request,'reset_password.html',{'msg':"Invalid old password!"})
        elif 'new' in request.POST:
            new=request.POST['new']
            print(new)
            u=request.user
            u.set_password(new)
            u.save()
            return redirect('logout')
    return render(request,'reset_password.html')

def forgot(request):
    if request.method=='POST':
        uname=request.POST['username']
        try:
            u=User.objects.get(username=uname)
            request.session['fp_user'] = u.username
            return redirect('new_password')
        except:
            return render(request,'forgot.html',{'msg':"Username doesn't exits!"})
    return render(request,'forgot.html')

def new_password(request):
    username = request.session.get('fp_user')
    if not username:
        return redirect('forgot')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('forgot')
    if request.method == 'POST':
        new_pass = request.POST['new']
        if user.check_password(new_pass):
            return render(request,'new.html',{'msg':"New password can't be same as old password!"})
        else:
            user.set_password(new_pass)
            user.save()
            del request.session['fp_user']
            return redirect('login')
    return render(request, 'new.html')

@login_required(login_url='login')
def update_profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        user = request.user

        user.first_name = request.POST.get("fname")
        user.last_name = request.POST.get("lname")
        user.email = request.POST.get("email")

        user.save()

        profile_pic = request.FILES.get("profile_pic")

        if profile_pic:
            profile.profile_pic = profile_pic
            profile.save()

        return redirect("profile")

    return render(request, "update_profile.html", {
        "profile": profile
    })

# blog views

@login_required(login_url='login')
def posts(request):

    search_query = request.GET.get('q', '').strip()

    posts_list = Post.objects.filter(
        is_deleted=False,
        is_published=True
    )

    if search_query:
        posts_list = posts_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    posts_list = posts_list.order_by('-created_at')

    paginator = Paginator(posts_list, 6)

    page_number = request.GET.get('page')

    posts = paginator.get_page(page_number)

    return render(
        request,
        'posts.html',
        {
            'posts': posts,
            'search_query': search_query,
        }
    )

@login_required(login_url='login')
def post_detail(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        is_deleted=False
    )

    comments = post.comments.select_related(
        'user'
    ).order_by('-created_at')

    like_count = post.reactions.filter(
        reaction=Reaction.LIKE
    ).count()

    dislike_count = post.reactions.filter(
        reaction=Reaction.DISLIKE
    ).count()

    user_reaction = post.reactions.filter(
        user=request.user
    ).first()

    return render(
        request,
        'post_detail.html',
        {
            'post': post,
            'comments': comments,
            'like_count': like_count,
            'dislike_count': dislike_count,
            'user_reaction': user_reaction,
        }
    )

@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        is_published = request.POST.get('is_published') == 'on'

        post = Post.objects.create(
            title=title,
            content=content,
            image=image,
            author=request.user,
            is_published=is_published
        )

        return redirect('post-detail', post_id=post.id)

    return render(request, 'new_blog.html')

@login_required(login_url='login_')
def delete_post(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user,
        is_deleted=False
    )
    post.is_deleted = True
    post.save()
    return redirect('home')

@login_required(login_url='login_')
def update_post(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user,
        is_deleted=False
    )

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.is_published = request.POST.get('is_published') == 'on'
        post.save()
        return redirect('post-detail', post_id=post.id)

    return render(request, 'update_post.html', {'post': post})

@login_required(login_url='login')
def my_posts(request):
    posts = Post.objects.filter(
        author=request.user,
        is_deleted=False
    ).order_by('-created_at')

    return render(request, 'my_posts.html', {'posts': posts})

@login_required(login_url='login')
def add_comment(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        is_deleted=False
    )

    if request.method == 'POST':

        content = request.POST.get('content', '').strip()

        if content:
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )

    return redirect('post-detail', post_id=post.id)

@login_required(login_url='login')
def react_to_post(request, post_id, reaction_type):

    post = get_object_or_404(
        Post,
        id=post_id,
        is_deleted=False
    )

    if reaction_type not in ['like', 'dislike']:
        return redirect('post-detail', post_id=post.id)

    reaction = Reaction.objects.filter(
        post=post,
        user=request.user
    ).first()

    if reaction:

        if reaction.reaction == reaction_type:
            # Clicking the same reaction again removes it
            reaction.delete()

        else:
            # Change like ↔ dislike
            reaction.reaction = reaction_type
            reaction.save()

    else:

        Reaction.objects.create(
            post=post,
            user=request.user,
            reaction=reaction_type
        )

    return redirect('post-detail', post_id=post.id)

@login_required(login_url='login')
def edit_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id,
        user=request.user
    )

    if request.method == 'POST':

        content = request.POST.get('content', '').strip()

        if content:
            comment.content = content
            comment.save()

        return redirect(
            'post-detail',
            post_id=comment.post.id
        )

    return render(
        request,
        'edit_comment.html',
        {
            'comment': comment
        }
    )

@login_required(login_url='login')
def delete_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id,
        user=request.user
    )

    post_id = comment.post.id

    if request.method == 'POST':
        comment.delete()

    return redirect(
        'post-detail',
        post_id=post_id
    )