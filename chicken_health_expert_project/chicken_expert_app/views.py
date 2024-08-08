from django.shortcuts import render
from .expert_llm import get_chicken_expert_response, correct_spelling
from .disease_frequency import get_disease_frequency
from .models import Interaction
from django.views.decorators.csrf import csrf_exempt
import json, logging

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request, 'chicken_expert_app/home.html')

def about(request):
    return render(request, 'chicken_expert_app/about.html')

@csrf_exempt
def expert_llm(request):
    if request.method == 'POST':
        user_query = request.POST.get('user_query')
        location_data = request.POST.get('location-data')
        confirmation_action = request.POST.get('confirmation_action')
        
        if 'interactions' not in request.session:
            request.session['interactions'] = []
        
        logger.debug(f"Session before modification: {request.session['interactions']}")
        
        if confirmation_action:
            if confirmation_action == 'use_corrected':
                user_query = request.POST.get('user_query')
            elif confirmation_action == 'use_original':
                user_query = request.POST.get('original_query')
            
            if user_query:
                response = get_chicken_expert_response(user_query, location_data)
                request.session['interactions'].insert(0, {
                    'question': user_query,
                    'response': response
                })
                request.session.modified = True
                logger.debug(f"Session after modification: {request.session['interactions']}")
                context = {
                    'response': response,
                    'current_question': user_query,
                    'interactions': request.session['interactions']
                }
                return render(request, 'chicken_expert_app/expert_llm.html', context)
            else:
                error_message = "Query cannot be empty."
                return render(request, 'chicken_expert_app/expert_llm.html', {'error_message': error_message})
        
        corrected_query = correct_spelling(user_query)
        
        if corrected_query != user_query:
            context = {
                'original_query': user_query,
                'corrected_query': corrected_query,
                'location_data': location_data,
                'confirmation_needed': True
            }
            return render(request, 'chicken_expert_app/expert_llm.html', context)
        
        if user_query:
            response = get_chicken_expert_response(user_query, location_data)
            request.session['interactions'].insert(0, {
                'question': user_query,
                'response': response
            })
            request.session.modified = True
            logger.debug(f"Session after modification: {request.session['interactions']}")
            context = {
                'response': response,
                'current_question': user_query,
                'interactions': request.session['interactions']
            }
            return render(request, 'chicken_expert_app/expert_llm.html', context)
        else:
            error_message = "Please enter a valid query."
            return render(request, 'chicken_expert_app/expert_llm.html', {'error_message': error_message})

    context = {
        'interactions': request.session.get('interactions', [])
    }
    return render(request, 'chicken_expert_app/expert_llm.html', context)

def show_disease_frequency(request):
    # Get disease frequency data
    disease_location_counter, disease_total_counter, location_name_dict = get_disease_frequency()
    
    # Convert the dictionary keys from tuples to strings for JSON serialization
    disease_location_counter_str_keys = {
        disease: {f"({location[0]}, {location[1]})": frequency for location, frequency in locations.items()
                  if location_name_dict.get(str(location)) is not None}  # Filter locations with valid names}
        for disease, locations in disease_location_counter.items()
    }

    # Filter out diseases with no valid locations
    disease_location_counter_str_keys = {
        disease: locations for disease, locations in disease_location_counter_str_keys.items() if locations
    }

    # prepare the context to be sent to the template
    context = {
        'keyword_counter_dict_str': json.dumps(disease_location_counter_str_keys, indent=4),
        'keyword_counter_dict': disease_location_counter_str_keys,
        'disease_total_counter': disease_total_counter,
        'location_name_dict': location_name_dict
    }
    # Debugging print
    print("Context data prepared for rendering:", context['keyword_counter_dict'])
    
    return render(request, 'chicken_expert_app/disease_frequency.html', context)


def find_vet(request):
    return render(request, 'chicken_expert_app/find_vet.html')
