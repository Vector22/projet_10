from django.contrib.auth import login, authenticate, logout
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import SignUpForm, ResearchForm
from .models import Food, MyFood

from random import randrange


def home(request):
    """ show the home page """

    if request.method == 'POST':
        form = ResearchForm(request.POST or None)
        if form.is_valid():
            searchedFood = form.cleaned_data['search']
            return redirect('result', searchedFood=searchedFood)
    else:
        form = ResearchForm()
    return render(request, 'food/index.html', {'form': form})


def result(request, searchedFood):
    """ The search result page """

    if request.method == 'POST':
        form = ResearchForm(request.POST or None)
        if form.is_valid():
            searchedFood = form.cleaned_data['search']
            return redirect('result', searchedFood=searchedFood)
    else:
        form = ResearchForm()

    result = Food.objects.filter(name__contains=str(searchedFood)).exists()
    if not result:
        return redirect('food_not_found')
    first_food = Food.objects.filter(name__icontains=str(searchedFood))[0]
    temp = first_food.category.food_set.all()
    foodSubtituts = temp.exclude(id=first_food.id).order_by('nutritionGrade')

    return render(request, 'food/result.html', locals())


def saveFood(request):
    """ This function perform the task what permit
    to save a food in favorite by the user
    """

    # recover the data transmitted by the client
    foodId = int(request.POST.get('foodId', None))
    userId = int(request.POST.get('userId', None))

    if foodId and userId:
        food = Food.objects.get(id=foodId)  # the concerned food
        # verfy if the food has been already saved by the user
        foodSaved = MyFood.objects.filter(food=food).exists()
        # if never saved, save it
        if not foodSaved:
            # save the food in the db
            favoriteFood = MyFood.objects.create(userId=userId, food=food)
            favoriteFood.save()
            messages.add_message(request, messages.SUCCESS,
                                 'The food has been saved...')
            return redirect('result', searchedFood=food.name)
        else:
            messages.add_message(request, messages.WARNING,
                                 'This food is already in your favorites...')
            return redirect('result', searchedFood=food.name)

    else:
        messages.add_message(request, messages.WARNING,
                             'An error has occured when saving the food !')
        return redirect('result', searchedFood=food.name)


def myFoods(request):
    """ This function show the user's favorites foods """
    if request.method == 'POST':
        form = ResearchForm(request.POST or None)
        if form.is_valid():
            searchedFood = form.cleaned_data['search']
            return redirect('result', searchedFood=searchedFood)
    else:
        form = ResearchForm()

    favoritesFoods = MyFood.objects.filter(userId=request.user.id)
    if favoritesFoods.count() > 0:
        # choose a food to display at the top of the page randomly
        headerFood = favoritesFoods[randrange(favoritesFoods.count())]
    return render(request, 'food/my_foods.html', locals())


def foodNotFound(request):
    if request.method == 'POST':
        form = ResearchForm(request.POST or None)
        if form.is_valid():
            searchedFood = form.cleaned_data['search']
            return redirect('result', searchedFood=searchedFood)
    else:
        form = ResearchForm()
    return render(request, 'food/food_not_found.html', locals())


class FoodDetail(DetailView):
    model = Food
    template_name = 'food/food_details.html'
    context_object_name = 'food'


class UserDetail(DetailView):
    model = User
    template_name = 'food/user_details.html'
    context_object_name = 'user'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'food/registration/signup.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect(reverse(home))


def legaleNotice(request):
    return render(request, 'food/mentions_legales.html', locals())


# Test centry integration
def trigger_error(request):
    division_by_zero = 1 / 0
