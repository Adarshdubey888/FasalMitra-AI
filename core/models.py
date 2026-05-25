from django.db import models


class SoilImage(models.Model):

    image = models.ImageField(upload_to='soil_images/')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.image.name
    

from django.db import models

class PredictionReport(models.Model):

    farmer_phone = models.CharField(max_length=15)

    crop = models.CharField(max_length=100)

    soil = models.CharField(max_length=100)

    season = models.CharField(max_length=100)

    prediction = models.CharField(max_length=100)

    irrigation = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.crop