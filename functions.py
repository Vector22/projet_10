from food.models import Category, Food, MyFood
from django.utils.text import slugify
from django.core.files import File

import requests
import urllib.request


def present(cle, table):
    """function that checks if elements belong to
    the keys of a dictionary"""
    resultat = True
    for i in cle:
        if i in table.keys():
            pass
        else:
            resultat = False
            break  # sort de la boucle
    return resultat


def fill_table(maxFoodCat, maxFoodPage):
    """
    This function download food and inserting it into
    the local database
    Parameter: maxFoodCat = maximum food categories wished
               maxFoodPage = maximum categories food page wished

    Not all foods are looking for relevant information.
    So we used a table containing the keys searched for
    verification before extraction.
    """

    requiredIndex = ("url", "nutrition_grade_fr",
                     "purchase_places", "manufacturing_places", "countries",
                     "ingredients_text", "product_name", "generic_name_fr",
                     "image_url", "image_small_url",
                     )

    # geting categories objects from openfoodfact
    categoriesUrl = "https://fr.openfoodfacts.org/categories.json"
    r = requests.get(categoriesUrl)
    categories = r.json()

    # insert the categories in the DB
    for i in range(maxFoodCat):
        cat = Category()
        cat.name = categories['tags'][i]['name']
        cat.url = categories['tags'][i]['url']
        cat.save()

        # insert foods for each category
        """
        A category may contain many page of foods, paginate by 20.
        Then we save the differents url in a list tab to loop other
        it and extract any foods that respect the constraint.
        """

        foodPageUrlTab = list()  # the different page url of aliments
        foodPageUrlTab = [cat.url + '/' + str(ind) + '.json'
                          for ind in range(1, maxFoodPage + 1)]

        # request each url of the table to find out the contains foods
        for j in range(len(foodPageUrlTab)):
            foodsUrl = foodPageUrlTab[j]
            r2 = requests.get(foodsUrl)
            foods = r2.json()
            foodsName = list()

            # each page contain 20 foods
            for k in range(len(foods)):
                # verify if the food object keys contain the
                # required index
                if present(requiredIndex, foods['products'][k]):
                    # then add them to the DB
                    food = Food()
                    fObject = foods['products'][k]  # json food object

                    # fill in all the texts fields
                    food.category = cat
                    food.name = fObject['product_name']
                    food.nameFr = fObject['product_name_fr']
                    food.genericNameFr = fObject['generic_name_fr']
                    food.url = fObject['url']
                    food.nutritionGrade = fObject['nutrition_grade_fr']
                    food.manufacturingPlaces = fObject['manufacturing_places']
                    food.purchasePlaces = fObject['purchase_places']
                    food.countries = fObject['countries'].replace("en:", "")
                    food.ingredientsText = fObject['ingredients_text']
                    food.image_link = fObject['image_front_url']

                    # this section deals with uploading images and inserting
                    # them into the DB

                    # we save two kinds of images; small and normal size

                    # variables what store the the saved images directory path
                    #imageDirectory = 'media/image/'  # for the normal size
                    #imageSmallDirectory = 'media/imageSmall/'  # small
                    """imageDirectory = 'media/image/'

                    # variables who rename the downloaded images
                    imageName = "{}.jpg".format(slugify(food.name))
                    imageSmallName = "{}-sm.jpg".format(slugify(food.name))

                    # download the two images with urllib librairy
                    # urllib.request.urlretrieve(imageUrl, localImagePath)
                    imagePath = imageDirectory + str(imageName)
                    imageSmallPath = imageDirectory + str(imageSmallName)

                    urllib.request.urlretrieve(fObject['image_url'],
                                               imagePath)
                    urllib.request.urlretrieve(fObject['image_small_url'],
                                               imageSmallPath)

                    # now we can fill the two imageFields
                    # with the downloaded images
                    food.image = File(open(imagePath, 'rb'))
                    food.imageSmall = File(open(imageSmallPath, 'rb'))"""

                    if food.name in foodsName:
                        pass
                    else:
                        foodsName.append(food.name)
                        food.save()


def clear_table():
    """
    This function clears all entries in the tables of the database
    """

    # delete the users favorites foods
    MyFood.objects.all().delete()

    # delete the the foods
    Food.objects.all().delete()

    # delete the categories
    Category.objects.all().delete()


def init_db():

    maxFoodCat = 20
    maxFoodPage = 5

    fill_table(maxFoodCat, maxFoodPage)
