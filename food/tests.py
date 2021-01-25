from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
# For selenium
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager

from .models import Category, Food, MyFood
from .forms import SignUpForm, ResearchForm

# Test the app models


class CategoryTest(TestCase):
    def setUp(self):
        self.name = "Boissons"
        self.url = "https://www.off.com/category/boissons"
        self.category = Category.objects.create(name=self.name, url=self.url)

    def test_initialize_category(self):
        """ Test if a category has been properly
        initialized """
        self.assertEqual(self.category.name, 'Boissons')
        self.assertTrue((self.category.name is not None
                         and self.category.url is not None))
        self.assertEqual(str(self.category), "Boissons")


class FoodTest(TestCase):
    def setUp(self):
        self.catName = "Boissons"
        self.catUrl = "https://www.off.com/category/boissons"
        self.foodCategory = Category.objects.create(name=self.catName,
                                                    url=self.catUrl)

        self.url = "https://www.off.com/aliments/boissons/orangina"
        self.nameFr = "Orangina"
        self.nutritionGrade = 'C'
        self.countries = "France"
        self.ingredientsText = "Eau, sucre, orange naturel"
        self.food = Food.objects.create(nameFr=self.nameFr,
                                        url=self.url,
                                        nutritionGrade=self.nutritionGrade,
                                        countries=self.countries,
                                        ingredientsText=self.ingredientsText,
                                        category=self.foodCategory)

    def test_initialize_Food(self):
        """ Test if a food has been properly
        initialized """
        self.assertEqual(self.food.category.name, "Boissons")
        self.assertEqual(self.countries, "France")
        self.assertEqual(str(self.food), "Orangina")


class MyFoodTest(TestCase):
    def setUp(self):
        self.catName = "Boissons"
        self.catUrl = "https://www.off.com/category/boissons"
        self.foodCategory = Category.objects.create(name=self.catName,
                                                    url=self.catUrl)

        self.url = "https://www.off.com/aliments/boissons/orangina"
        self.nameFr = "Orangina"
        self.nutritionGrade = 'C'
        self.countries = "France"
        self.ingredientsText = "Eau, sucre, orange naturel"
        self.food = Food.objects.create(nameFr=self.nameFr,
                                        url=self.url,
                                        nutritionGrade=self.nutritionGrade,
                                        countries=self.countries,
                                        ingredientsText=self.ingredientsText,
                                        category=self.foodCategory)

        self.userId = 1
        self.MyFood = MyFood.objects.create(userId=self.userId, food=self.food)

    def test_initialize_MyFood(self):
        self.assertEqual(self.MyFood.food.nutritionGrade, 'C')
        self.assertTrue('Eau' in self.MyFood.food.ingredientsText)
        self.assertEqual(str(self.MyFood), "Orangina")


# Test the app's form


class SignUpFormTest(TestCase):
    def setUp(self):
        self.username = "Stephane"
        self.password = "St3ph4n3"
        self.password1 = self.password
        self.password2 = self.password
        self.email = "user@mp.com"
        self.first_name = "Nedelec"

    def test_signupForm_valid(self):
        form = SignUpForm(
            data={
                'username': self.username,
                'first_name': self.first_name,
                'email': self.email,
                'password1': self.password1,
                'password2': self.password2
            })

        self.assertTrue(form.is_valid())

    def test_signupForm_invalid(self):
        """ We invalidate the signUpForm by set the email
        field to blank """
        form = SignUpForm(
            data={
                'username': self.username,
                'first_name': self.first_name,
                'email': "",
                'password1': self.password1,
                'password2': self.password2
            })

        self.assertFalse(form.is_valid())


class ResearchFormTest(TestCase):
    def setUp(self):
        self.searchText = "Chocolat"

    def test_researchForm_valid(self):
        form = ResearchForm(data={'search': self.searchText})
        self.assertTrue(form.is_valid())

    def test_researchForm_invalid(self):
        """ We invalidate the ResearchForm by lefting the
        search field to blank """
        form = ResearchForm(data={'search': ""})
        self.assertFalse(form.is_valid())


# Test the app's views


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="Stephane",
                                        email="user@mp.com",
                                        first_name="Stephane")
        self.user.set_password('St3ph4n3')
        self.user.save()

        self.homeUrl = reverse('home')
        self.myFoodsUrl = reverse('myFoods')
        # Usefull to test the FoodDeatil(DetailView) view
        self.catName = "Boissons"
        self.catUrl = "https://www.off.com/category/boissons"
        self.foodCategory = Category.objects.create(name=self.catName,
                                                    url=self.catUrl)

        self.url = "https://www.off.com/aliments/boissons/orangina"
        self.nameFr = "Orangina"
        self.nutritionGrade = 'C'
        self.countries = "France"
        self.ingredientsText = "Eau, sucre, orange naturel"
        # self.image = File(open('media/image/caro.jpg', 'rb'))
        # self.imageSmall = File(open('media/image/caro-sm.jpg', 'rb'))
        self.food = Food.objects.create(nameFr=self.nameFr,
                                        url=self.url,
                                        nutritionGrade=self.nutritionGrade,
                                        countries=self.countries,
                                        ingredientsText=self.ingredientsText,
                                        category=self.foodCategory)
        self.food.save()

    def test_home_view(self):
        """ Verify that everyone can se the home page"""
        response = self.client.get(self.homeUrl)
        # status http 200 query ok
        self.assertEqual(response.status_code, 200)

    def test_redirect_anonymous_user(self):
        """ Redirect a anonymous user who attempt to
        access to the user favorites foods page """
        response = self.client.get(self.myFoodsUrl)
        # status 302 http redirect
        self.assertEqual(response.status_code, 302)
        # Check that the view don't use myFoods template
        self.assertTemplateNotUsed(response, 'food/my_foods.html')
        # Check that the next redirection page is correct
        self.assertRedirects(response, '/accounts/login/?next=/myFoods/')

    def test_signup_view(self):
        """ Verify if a user can logged in """

        # attempt to log the client
        user_login = self.client.login(username="Stephane",
                                       password="St3ph4n3")
        response = self.client.get(self.homeUrl)

        self.assertTrue(user_login)
        # Verify the password
        self.assertTrue(self.user.check_password("St3ph4n3"))
        # Check if the correct template is used to render the response
        self.assertTemplateUsed(response, 'food/index.html')

    """def test_saveFood_view(self):
        self.client.login(username="Stephane", password="St3ph4n3")
        response = self.client.post(reverse('saveFood',
                                            kwargs={'searchedFood':
                                                    self.food.nameFr}),
                                    data={'foodId': self.food.id,
                                          'userId': self.user.id, })
        self.assertEqual(response.status_code, 302)"""

    def test_searchFood_view(self):
        response = self.client.post(
            reverse('result', kwargs={'searchedFood': self.food.nameFr}))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'food/result.html')

    def test_myFoods_view(self):
        self.client.login(username="Stephane", password="St3ph4n3")
        response = self.client.get(self.myFoodsUrl)
        self.assertTemplateUsed(response, 'food/my_foods.html')

    def test_food_not_found_view(self):
        response = self.client.get(reverse('food_not_found'))
        self.assertTemplateUsed(response, 'food/food_not_found.html')

    def test_foodDetail_view(self):
        foodDetailUrl = reverse('food_detail', args=(self.food.id, ))
        response = self.client.get(foodDetailUrl)
        # Status http 200 ok
        self.assertEqual(response.status_code, 200)
        # The response contain a food object
        self.assertEqual(response.context['object'], self.food)

    def test_userDetail_view(self):
        self.client.login(username="Stephane", password="St3ph4n3")
        userDetailUrl = reverse('user_detail', args=(self.user.id, ))
        response = self.client.get(userDetailUrl)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)

    def test_legaleNotice_view(self):
        response = self.client.get(reverse('legale_notice'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/mentions_legales.html')


# Test with selenium
# class AccountTestCase(LiveServerTestCase):
#     def setUp(self):
#         self.selenium = webdriver.Firefox(
#             executable_path=GeckoDriverManager().install())
#         super(AccountTestCase, self).setUp()

#     def tearDown(self):
#         self.selenium.quit()
#         super(AccountTestCase, self).tearDown()

#     def test_register(self):
#         selenium = self.selenium
#         # Opening the link we want to test
#         selenium.get('http://127.0.0.1:8000/signup/')
#         # Find the form element
#         username = selenium.find_element_by_id('id_username')
#         first_name = selenium.find_element_by_id('id_first_name')
#         last_name = selenium.find_element_by_id('id_last_name')
#         email = selenium.find_element_by_id('id_email')
#         password1 = selenium.find_element_by_id('id_password1')
#         password2 = selenium.find_element_by_id('id_password2')

#         submit = selenium.find_element_by_name('submit')

#         print(submit)

#         # Fill the form with data
#         first_name.send_keys('ulrich')
#         last_name.send_keys('ulrich')
#         username.send_keys('vector22')
#         email.send_keys('ulrich@gmail.com')
#         password1.send_keys('R3k1nV3ct0r**')
#         password2.send_keys('R3k1nV3ct0r**')

#         # Submitting the form
#         submit.send_keys(Keys.RETURN)

#         # Check the returned result
#         textTab = [
#             'Nom d\'utilisateur', 'First name', 'Last name', 'Email',
#             'Mot de passe', 'Confirmation du mot de passe'
#         ]

#         # assert the presence of some wignets label
#         for text in textTab:
#             assert text in selenium.page_source

#     def test_result(self):
#         # <h4 class="food-box__name">Zero cookie chocolate brownie flavour</h4>
#         selenium = self.selenium
#         # Opening the link we want to test
#         selenium.get('http://127.0.0.1:8000/result/chocolat')

#         # Assert the presence of some chocolat in the food list displayed
#         foodName = [
#             'Krispees quinoa amaranth', 'NESQUIK Barres de Céréales',
#             'Zero cookie chocolate brownie flavour'
#         ]

#         for name in foodName:
#             assert name in selenium.page_source
