import json
import requests   
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Recipe


def get_recipe_image(query):
    url = "https://api.unsplash.com/search/photos"

    params = {
        "query": f"{query} food",
        "client_id": "ZhM2HD0fj-7gn4S_0z-BjHTuvibD0CAnLUcVnR80Aj0",  
        "per_page": 1
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("results"):
            return data["results"][0]["urls"]["regular"]
    except:
        pass

    return "https://via.placeholder.com/400x300?text=No+Image"


def home(request):
    return render(request, "index.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("signup")

        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "signup.html")

@login_required(login_url='login')
def dashboard(request):
    return render(request, "dashboard.html")


@login_required(login_url='login')
def add_recipe(request):

    if request.method == "POST":
        name = request.POST.get("name")
        ingredients = request.POST.get("ingredients")
        steps_text = request.POST.get("steps")
        duration = request.POST.get("duration")
        difficulty = request.POST.get("difficulty")

        if steps_text:
            steps_list = [s.strip() for s in steps_text.split("||") if s.strip()]
        else:
            steps_list = []

        image_url = get_recipe_image(name)

        Recipe.objects.create(
            name=name,
            ingredients=ingredients,
            steps=steps_list,
            duration=int(duration) if duration else 0,
            difficulty=difficulty,
            image_url=image_url
        )

        messages.success(request, "Recipe added successfully!")
        return redirect("recipes")

    return render(request, "add_recipe.html")


@login_required(login_url='login')
def recipes_page(request):
    recipes = Recipe.objects.all()
    return render(request, "recipes.html", {"recipes": recipes})

@login_required(login_url='login')
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, "recipe_detail.html", {"recipe": recipe})

@login_required(login_url='login')
def recipe_simulation(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, "simulate.html", {"recipe": recipe})

@login_required(login_url='login')
def favorites(request):
    favorite_recipes = request.user.favorite_recipes.all()
    return render(request, "favorites.html", {"recipes": favorite_recipes})

@login_required(login_url='login')
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if recipe.favorites.filter(id=request.user.id).exists():
        recipe.favorites.remove(request.user)
    else:
        recipe.favorites.add(request.user)

    return redirect("recipes")

@login_required(login_url='login')
def profile(request):
    return render(request, "profile.html", {"user": request.user})

def recipe_list(request):
    recipes = Recipe.objects.all()
    data = []

    for r in recipes:
        data.append({
            "name": r.name,
            "ingredients": r.ingredients,
            "steps": r.steps,
            "duration": r.duration,
            "difficulty": r.difficulty,
            "image": r.image_url
        })

    return JsonResponse(data, safe=False)