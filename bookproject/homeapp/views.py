from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UserCreationWithEmailForm
from django.views.generic import CreateView, View
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import logout
# Create your views here.
def home(request):
    context = {}
    return render(request, 'homeapp/home.html', context)

class RegisterUser(CreateView):
    model = User
    form_class = UserCreationWithEmailForm
    template_name = 'homeapp/register.html'
    
    success_url = reverse_lazy('login')
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        # Redirect to a success page
        return HttpResponseRedirect(reverse('home'))  # Assuming 'home' is the name of your home page URL
    else:
        # Handle invalid request methods gracefully
        return HttpResponseRedirect(reverse('home'))  # Redirect to home or any other appropriate page