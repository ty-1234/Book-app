from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Category, Thread, Post
from .forms import CategoryForm, ThreadForm, PostForm
import pusher
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect    
import json

def index_view(request):
    categories = Category.objects.all()
    categories_with_threads = [
        {'category': category, 'threads': Thread.objects.filter(category=category).order_by('-created_at')[:5]}
        for category in categories
    ]
    return render(request, 'forum_index.html', {'categories_with_threads': categories_with_threads})

@login_required
def create_thread(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.posted_by = request.user  # Set the user here
            thread.category = category      # Ensure the category is also set correctly
            thread.save()
            return redirect('category-detail', category_id=category.id)
    else:
        form = ThreadForm(initial={'posted_by': request.user, 'category': category})  # Set initial values

    return render(request, 'create_thread.html', {'form': form, 'category': category})

@staff_member_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum-index')
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})

@staff_member_required
def delete_category(request, category_id):
    Category.objects.get(id=category_id).delete()
    return redirect('forum-index')

@staff_member_required
def delete_thread(request, thread_id):
    Thread.objects.get(id=thread_id).delete()
    return redirect('forum-index')

@staff_member_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('thread-detail', thread_id=post.thread.id)

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    threads = category.threads.all().order_by('-created_at')
    return render(request, 'category_detail.html', {'category': category, 'threads': threads})

@csrf_protect
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = thread.posts.all().order_by('created_at')
    context = {
        'thread': thread,
        'posts': posts,
        'PUSHER_KEY': settings.PUSHER_KEY,
        'PUSHER_CLUSTER': settings.PUSHER_CLUSTER,
    }
    return render(request, 'thread_detail.html', context)

pusher_client = pusher.Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
    ssl=settings.PUSHER_SSL
)
@login_required
@csrf_protect
def create_post(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            if message:
                post = Post.objects.create(
                    thread=thread,
                    message=message,
                    created_by=request.user
                )

                # Trigger Pusher event
                pusher_client.trigger('thread-' + str(thread.id), 'new-post', {
                    'username': post.created_by.username,
                    'message': post.message,
                    'created_at': post.created_at.isoformat()
                })

                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'error': 'Message is empty.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})
