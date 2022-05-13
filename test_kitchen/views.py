from django.shortcuts import render, redirect
from django.http import HttpResponse
from test_kitchen.forms import TestKitchenPostCreate
# Create your views here.
def test_kitchen_list(request):
	return render(request, "TestKitchenList.html")

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
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect('account:view', user_id=user.pk)

    return render(request, "TestKitchenCreate.html", context)
