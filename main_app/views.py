from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from main_app.models import Recipe
from django.views.generic.detail import DetailView

# Create your views here.

DEBUG = False

def home_screen_view(request):
	context = {}
	context['debug_mode'] = settings.DEBUG
	context['debug'] = DEBUG
	context['room_id'] = "1"
	return render(request, "home.html", context)

def recipe_search(request,  *args):
    if request.method == "POST":
        searched = request.POST['searched']
        context = {}
        context['recipes'] = Recipe.objects.filter(title__icontains=searched)
        context['searched'] = searched
        return render(request, "RecipesList.html", context)
    else: 
        context = {}
        context['recipes'] = Recipe.objects.all()
        return render(request, "RecipesList.html", context)

class RecipeDetail(DetailView):
    model = Recipe
    template_name = "RecipeDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def summer_2022_view(request):
    
	return render(request, "Summer2022.html")