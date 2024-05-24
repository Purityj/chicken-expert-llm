from django.shortcuts import render, HttpResponse
from .expert_llm import get_chicken_expert_response
from .disease_frequency import get_disease_frequency
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import VetenaryOffice
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request, 'chicken_expert_app/home.html')

def expert_llm(request):
    if request.method == 'POST':
        user_query = request.POST.get('user_query')
        response = get_chicken_expert_response(user_query)
        context = {'response': response}
        return render(request, 'chicken_expert_app/expert_llm.html', context)
    return render(request, 'chicken_expert_app/expert_llm.html')

def show_disease_frequency(request):
    keyword_counter = get_disease_frequency()
    keyword_counter_dict = dict(keyword_counter)
    context = {'keyword_counter_dict': keyword_counter_dict}
    return render(request, 'chicken_expert_app/disease_frequency.html', context)

def find_vets(request):
    # get latitude and longitude from POST
    latitude = float(request.POST.get('latitude'))
    longitude = float(request.POST.get('longitude'))
    user_location = Point(longitude, latitude, srid=4326)

    # query for nearby vet offices within 10Km
    nearby_vets = VetenaryOffice.objects.annotate(
        distance=Distance('location', user_location)
        ).filter(distance__lt=10000).order_by('distance')[:10]
    
    results = {vet.name: vet.distance.m for vet in nearby_vets}
    return JsonResponse(results)




