from django.shortcuts import render
from django.http import JsonResponse
from .expert_llm import get_chicken_expert_response
from .disease_frequency import get_disease_frequency
import json

# Create your views here.
def home(request):
    return render(request, 'chicken_expert_app/home.html')

def expert_llm(request):
    if request.method == 'POST':
        user_query = request.POST.get('user_query')
        location_data = request.POST.get('location-data')

        print(f"Received form data: question={user_query}, location_data={location_data}")

        response = get_chicken_expert_response(user_query, location_data)
        context = {'response': response}
        # return JsonResponse('status':'Success', 'response': response)
        return render(request, 'chicken_expert_app/expert_llm.html', context)
    return render(request, 'chicken_expert_app/expert_llm.html')

import json

def show_disease_frequency(request):
    # Get disease frequency data
    disease_location_counter = get_disease_frequency()
    
    # Convert the dictionary keys from tuples to strings for JSON serialization
    disease_location_counter_str_keys = {
        disease: {f"({location[0]}, {location[1]})": frequency for location, frequency in locations.items()}
        for disease, locations in disease_location_counter.items()
    }
    
    context = {
        'keyword_counter_dict_str': json.dumps(disease_location_counter_str_keys, indent=4),
        'keyword_counter_dict': disease_location_counter_str_keys
    }
    
    print("Context data prepared for rendering:", context['keyword_counter_dict'])
    
    return render(request, 'chicken_expert_app/disease_frequency.html', context)

def find_vet(request):
    return render(request, 'chicken_expert_app/find_vet.html')
