from django.db import models
from django.contrib.gis.db import models

# # Create your models here.
class Interaction(models.Model):
    question = models.TextField()
    response = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chicken_expert_app_interaction'

    def __str__(self):
        return (f'self.question, self.response')

class Vet(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
