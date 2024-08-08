from django.contrib import admin
from .models import Interaction

# Register your models here.
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('short_summary', 'latitude', 'longitude', 'location_name', 'created_at')
    search_fields = ('question', 'response', 'location_name')

admin.site.register(Interaction, InteractionAdmin)

