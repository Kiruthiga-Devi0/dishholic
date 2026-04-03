from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [

    # ---------- BASIC ----------
    path('', views.home, name="home"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup_view, name="signup"),
    path('dashboard/', views.dashboard, name='dashboard'),

    # ---------- FORGOT PASSWORD ----------
    path(
        'forgot-password/',
        auth_views.PasswordResetView.as_view(
            template_name='forgot_password.html'
        ),
        name='forgot_password'
    ),

    path(
        'forgot-password/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='forgot_password_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset-password/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='reset_password_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset-password/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='reset_password_complete.html'
        ),
        name='password_reset_complete'
    ),

    # ---------- RECIPES ----------
    path('recipes/', views.recipes_page, name="recipes"),
    path('add-recipe/', views.add_recipe, name="add_recipe"),

    # ⭐ NEW DETAIL PAGE
    path('recipe/<int:recipe_id>/', views.recipe_detail, name="recipe_detail"),

    path('simulate/<int:recipe_id>/', views.recipe_simulation, name="simulate"),

    # ---------- FAVORITES ----------
    path('favorites/', views.favorites, name="favorites"),
    path('toggle-favorite/<int:recipe_id>/', views.toggle_favorite, name="toggle_favorite"),

    # ---------- PROFILE ----------
    path('profile/', views.profile, name="profile"),

    # ---------- API ----------
    path('api/recipes/', views.recipe_list, name="recipe_api"),
]