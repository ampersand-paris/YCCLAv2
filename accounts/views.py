from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from accounts.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, RecipeCollectionCreate
from django.conf import settings

from accounts.models import CustomUser
from test_kitchen.models import TestKitchenPost
from .models import Recipe, RecipeCollection

# Create your views here.

def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")
    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect('home') #redirects to url with the name 'home' in backend/urls.py

        else: 
            context['registration_form'] = form

    return render(request, 'accounts/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')
    
    destination = get_redirect_if_exists(request)
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect('home')
        else:
            context['login_form'] = form
    return render(request, "accounts/login.html", context)

def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get('next'):
            redirect = str(request.GET.get('next'))
    return redirect

def account_view(request, *args, **kwargs):
        
    context = {}
    user_id =  kwargs.get('user_id')
    try: 
        account = CustomUser.objects.get(pk=user_id)
    except  CustomUser.DoesNotExist:
        return HttpResponse('That user does not exist.')
    if account: 
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['hide_email'] = account.username
        context['bio'] = account.bio
        context['fname'] = account.fname
        context['lname'] = account.lname
        context['posts'] = TestKitchenPost.objects.filter(user=account.id)
        context['postcards'] = RecipeCollection.objects.filter(user=account.id)

        is_self = True
        is_friend = False
        user = request.user

        if user.is_authenticated and user != account: 
            is_self = False
        elif not user.is_authenticated:
            is_self = False 

        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL
    
    if not user.is_authenticated:
        return redirect('login')
    else:        
        context['recipes'] = Recipe.objects.all()

        if request.POST:
            form = RecipeCollectionCreate(request.POST)
            print(form)
            if form.is_valid():
                form.save()
                print('success')
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
            return redirect('account:view', user_id=user.pk)

    return render(request, "accounts/account.html", context)

def edit_account_view(request, *args, **kwargs):

    if not request.user.is_authenticated:
        return redirect('login')
    user_id =  kwargs.get('user_id')
    # account = CustomUser.objects.get(pk=user_id)
    try: 
        account = CustomUser.objects.get(pk=user_id)
    except  CustomUser.DoesNotExist:
        return HttpResponse('Something went wrong.')
    if account.pk != request.user.pk:
        return HttpResponse('You cannot edit someone elses profile.')
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:view', user_id=account.pk)
        else: 
            form = AccountUpdateForm(request.POST, instance=request.user,
                initial = {
                    "id": account.pk,
                    "email": account.email,
                    "username": account.username,
                    "fname": account.fname,
                    "lname": account.lname,
                    "bio": account.bio,
                }
            )
            context['form'] = form
    else: 
        form = AccountUpdateForm(
                initial = {
                    "id": account.pk,
                    "email": account.email,
                    "username": account.username,
                    "fname": account.fname,
                    "lname": account.lname,
                    "bio": account.bio,
                })
        context['form'] = form

    return render(request, "accounts/edit_account.html", context)