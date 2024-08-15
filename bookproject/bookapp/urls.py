from django.urls import path
from . import views
from profileapp.views import send_notes

urlpatterns = [
        
    path("search_books/", views.search_books, name="search_books"),
    path('send-notes/', send_notes, name='send_notes'),
   
]