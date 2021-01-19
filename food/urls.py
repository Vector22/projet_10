from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


from . import views


urlpatterns = [

    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.login,
         {'template_name': 'food/registration/login.html'}, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('result/<str:searchedFood>', views.result, name='result'),
    path('saveFood/', views.saveFood, name='saveFood'),
    path('myFoods/', login_required(views.myFoods), name='myFoods'),
    path('user/<int:pk>/', login_required(views.UserDetail.as_view()),
         name='user_detail'),
    path('food/<int:pk>/', views.FoodDetail.as_view(),
         name='food_detail'),
    path('food_not_found/', views.foodNotFound, name='food_not_found'),
    path('legale_notice/', views.legaleNotice, name='legale_notice'),
    ]
