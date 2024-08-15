from django.shortcuts import render, redirect
import requests
from googleapiclient.discovery import build 
from .forms import BookSearchForm
from decouple import config

# Generate your own API key: https://console.cloud.google.com/apis/credentials
api_key = config("api_key")

# Create your views here.
def return_books_data(query):
    service = build("books", "v1", developerKey=api_key)
    request = service.volumes().list(q=query, maxResults=40)
    response = request.execute()
    # books_list = [response["items"][item]["volumeInfo"]for item in range(len(response["items"]))]
    # return books_list
    books_list = []
    for item in response.get("items", []):
        volume_info = item.get("volumeInfo", {})
        # only getting books with non null ISBN
        if any((identifier.get('type') == 'ISBN_13' or identifier.get('type') == 'ISBN_10') and identifier.get('identifier') for identifier in volume_info.get("industryIdentifiers", [])):
            books_list.append(volume_info)

    return books_list


def search_books(request):
    if request.method == "POST":
        form = BookSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            books = return_books_data(query)

            context = {
                "form": form,
                "books": books  # Add the books to the context
            }
            return render(request, "searchBooks_form.html", context)
    else:
        form = BookSearchForm()
        context = {
            "form": form,
            "books": []  # Empty list of books for initial rendering
        }
    return render(request, "searchBooks_form.html", context)
