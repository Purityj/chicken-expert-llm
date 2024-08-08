from django.db import models
from django.contrib.gis.db import models

# # Create your models here.
class Interaction(models.Model):
    question = models.TextField()
    response = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chicken_expert_app_interaction'
    
    def short_summary(self):
        # customize the displayed summary as needed
        summary_length = 50
        if len(self.question) > summary_length:
            question_summary = self.question[:summary_length] + '...'
        else:
            question_summary = self.question
        return f'{question_summary} - {self.location_name} - {self.created_at.strftime("%Y-%m-%d")}'
    short_summary.short_description = 'Interaction Summary' #customize column header

    def __str__(self):
        return self.short_summary()

class Vet(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
