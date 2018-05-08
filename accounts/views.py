from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('uploadcsv')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required(login_url='login')

def manageaccount(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']

        try:
            User=get_user_model()
            obj = User.objects.get(username=request.user.username)
            obj.username = name
            obj.set_password(password)
            obj.save()
            messages.error(request, "Please re-login.")
            return redirect('login')

        except:
            messages.error(request, "Username is taken. Please choose another username.")

    return render(request, 'accounts/manageaccount.html')