from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from accounts.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, RecipeCollectionCreate, RecipeCollectionUpdateForm
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
            return redirect('home:recipes') #redirects to url with the name 'home' in backend/urls.py

        else: 
            context['registration_form'] = form

    return render(request, 'accounts/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('home:about')

def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('account:view', user_id=user.pk)
    
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
                return redirect('account:view', user_id=user.pk)
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
    
    # CREATE RECIPE COLLECTION
    # if not user.is_authenticated:
    #     return redirect('login')
    # else:        
    #     context['recipes'] = Recipe.objects.all()

    #     if request.POST:
    #         form = RecipeCollectionCreate(request.POST)
    #         print(form)
    #         if form.is_valid():
    #             form.save()
    #             print('success')
    #             destination = get_redirect_if_exists(request)
    #             if destination:
    #                 return redirect(destination)
    #         return redirect('account:view', user_id=user.pk)

    # # CREATE RECIPE COLLECTION
    if not user.is_authenticated:
        return redirect('login')
    else:        
        context['recipes'] = Recipe.objects.all()
        form = RecipeCollectionCreate(request.POST)

        if request.POST and not form.is_valid():
            print('update')
            # collection_id = pk
            collection = RecipeCollection.objects.filter(user=account.id)
            update_form = RecipeCollectionUpdateForm(request.POST)
            if request.POST:
                print('update', update_form)
                if update_form.is_valid():
                    print('view update')
                    update_form.save()
                    return redirect('account:view', user_id=user.pk)
                # else: 
                #     update_form = RecipeCollectionUpdateForm(request.POST, instance=request.user,
                #         initial = {
                #             "id": collection.pk,
                #             "sent": collection.sent,
                #             "sent_to": collection.sent_to,
                #             "received": collection.received,
                #             "received_from": collection.received_from,
                #         }
                #     )
                    # context['form'] = form
            # else: 
            #     update_form = RecipeCollectionUpdateForm(
            #             initial = {
            #                 "id": collection.pk,
            #                 "sent": collection.sent,
            #                 "sent_to": collection.sent_to,
            #                 "received": collection.received,
            #                 "received_from": collection.received_from,
            #             })
            #     context['form'] = update_form
        elif request.POST:
            print('create')
            print(form)
            if form.is_valid():
                form.save()
                print('success')
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
            return redirect('account:view', user_id=user.pk)
            # else:
            #     form = RecipeCollectionCreate(prefix="create")
        
        
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

def edit_recipe_collection_view(request, pk):
    user = request.user
    user_id =  request.user.id
    context = {}
    postcard_id = pk
    postcard = RecipeCollection.objects.get(pk=postcard_id)
    form = RecipeCollectionUpdateForm(request.POST, instance=postcard)

    if not user.is_authenticated:
        return redirect('login')
    if request.POST:
        print('update', form)
        if form.is_valid():
            print('view update')
            form.save()
            return redirect('account:view', user_id=user.pk)
        else: 
            form = RecipeCollectionUpdateForm(request.POST, instance=request.user,
                initial = {
                    "id": postcard.pk,
                    "recipe": postcard.recipe,
                    "sent": postcard.sent,
                    "sent_to": postcard.sent_to,
                    "received": postcard.received,
                    "received_from": postcard.received_from,
                    }
                )
            context['form'] = form
    else: 
        form = RecipeCollectionUpdateForm(
            initial = {
                "id": postcard.pk,
                "recipe": postcard.recipe,
                "sent": postcard.sent,
                "sent_to": postcard.sent_to,
                "received": postcard.received,
                "received_from": postcard.received_from,
            })
        context['form'] = form
    
    return render(request, "accounts/postcard_update.html", context)