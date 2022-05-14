from django.shortcuts import render, redirect
from django.http import HttpResponse
from test_kitchen.forms import TestKitchenPostCreate, TestKitchenPostUpdateForm
from test_kitchen.models import TestKitchenPost
from accounts.models import CustomUser
from django.views.generic.detail import DetailView

# Create your views here.
def test_kitchen_list(request, *args):
    context = {}
    user_id =  request.user.pk
    try: 
        account = CustomUser.objects.get(pk=user_id)
    except  CustomUser.DoesNotExist:
        return HttpResponse('That user does not exist.')
    if account:
        context['posts'] = TestKitchenPost.objects.all()
    return render(request, "TestKitchenList.html", context)

class TestKitchenDetail(DetailView):
    model = TestKitchenPost
    template_name = "TestKitchenDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get('next'):
            redirect = str(request.GET.get('next'))
    return redirect

def test_kitchen_create(request, *args, **kwargs):
    user = request.user

    if not user.is_recipe_tester:
        return HttpResponse(f"You are not currently a recipe test. Please reach out to Ampersand and Lexi about becoming one at youcancookliterallyangything@gmail.com")
    context = {}

    if request.POST:
        form = TestKitchenPostCreate(request.POST)
        if form.is_valid():
            form.save()
            print('success')
            print(form)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect('account:view', user_id=user.pk)

    return render(request, "TestKitchenCreate.html", context)

def edit_test_kitchen_view(request, pk):

    if not request.user.is_authenticated:
        return redirect('login')
    user_id =  request.user.id
    post_id = pk
    post = TestKitchenPost.objects.get(pk=post_id)
    form = TestKitchenPostUpdateForm(request.POST, instance=post)
    try: 
        account = CustomUser.objects.get(id=user_id)
    except  CustomUser.DoesNotExist:
        return HttpResponse('Something went wrong.')
    if account.id != post.user.id:
        return HttpResponse('You cannot edit someone elses post.')
    context = {}
    if request.POST:
        print(form)
        if form.is_valid():
            print('view save')
            form.save()
            return redirect('test-kitchen:list')
        else: 
            form = TestKitchenPostUpdateForm(request.POST, instance=request.user,
                initial = {
                    "id": post.pk,
                    "title": post.title,
                    "post": post.post,
                }
            )
            context['form'] = form
    else: 
        form = TestKitchenPostUpdateForm(
                initial = {
                    "id": post.pk,
                    "title": post.title,
                    "post": post.post,
                })
        context['form'] = form

    return render(request, "TestKitchenUpdate.html", context)

def test_kitchen_delete(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id =  request.user.id
    post_id = pk
    post = TestKitchenPost.objects.get(pk=post_id)
    try: 
        account = CustomUser.objects.get(id=user_id)
    except  CustomUser.DoesNotExist:
        return HttpResponse('Something went wrong.')
    if account.id != post.user.id:
        return HttpResponse('You cannot delete someone elses post.')
    else:
        post.delete()
        
        return redirect('account:view', user_id=user_id)
    