from django.urls import path
from . import views

urlpatterns = [
    # "/forum/"
    path('', views.index_view, name='forum-index'),

    # "/forum/category/<category_id>/"
    path('category/<int:category_id>/', views.category_detail, name='category-detail'),

    # "/forum/category/<category_id>/create-thread/"
    path('category/<int:category_id>/create-thread/', views.create_thread, name='create-thread'),

    # "/forum/thread/<thread_id>/"
    path('thread/<int:thread_id>/', views.thread_detail, name='thread-detail'),
    
    # "/forum/thread/<thread_id>/create-post/"
    path('thread/<int:thread_id>/create_post/', views.create_post, name='create-post'),
    
    # "/forum/create-category/" (ADMIN ONLY)
    path('create-category/', views.create_category, name='create-category'),

    # "/forum/category/<category_id>/delete/" (ADMIN ONLY)
    path('category/<int:category_id>/delete/', views.delete_category, name='delete-category'),

    # "/forum/thread/<thread_id>/delete/" (ADMIN ONLY)
    path('thread/<int:thread_id>/delete/', views.delete_thread, name='delete-thread'),

    # "/forum/post/<post_id>/delete/" (ADMIN ONLY)
    path('post/<int:post_id>/delete/', views.delete_post, name='delete-post'),
]
