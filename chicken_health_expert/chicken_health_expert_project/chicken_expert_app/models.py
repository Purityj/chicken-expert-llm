from django.db import models
from django.contrib.gis.db import models

# # Create your models here.
# class Interaction(models.Model):
#     question = models.TextField()
#     response = models.TextField()

#     def __str__(self):
#         return (f'self.question, self.response')

class VetenaryOffice(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField(help_text="Represents longitude and latitude")

    def __str__(self):
        return self.name
