from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    def __str__(self):

        return self.name


class Food(models.Model):
    name = models.CharField(max_length=200)
    nameFr = models.CharField(max_length=200)
    genericNameFr = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    nutritionGrade = models.CharField(max_length=3)
    countries = models.CharField(max_length=200)
    purchasePlaces = models.CharField(max_length=200)
    manufacturingPlaces = models.TextField()
    ingredientsText = models.TextField()
    image_link = models.URLField(max_length=250, null=True)
    #image = models.ImageField(upload_to='image_bd/')
    #imageSmall = models.ImageField(upload_to='image_bd/')

    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):

        return self.nameFr


class MyFood(models.Model):
    """ A class who store the users favorites foods """

    userId = models.IntegerField()  # the user's id

    food = models.ForeignKey('Food', on_delete=models.CASCADE)

    def __str__(self):
        return self.food.nameFr
