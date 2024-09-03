from collections import defaultdict
from .models import Interaction
from django.conf import settings
import json, os

def get_disease_frequency():
    try:
        # Fetch user queries and llm responses from the database
        interactions = Interaction.objects.all()
        print(f"Fetched {len(interactions)} interactions from the database.")
    except Exception as e:
        print("Database connection error:", e)
        return {}

    # Initialize a nested dictionary to store the frequency of each disease per location and total frequency
    disease_location_counter = defaultdict(lambda: defaultdict(int))
    disease_total_counter = defaultdict(int)
    location_name_dict = {}

    # determine the file path dynamically
    json_file_path = os.path.join(settings.BASE_DIR, 'chicken_expert_app', 'chicken_diseases.json')
    print(json_file_path)

    # load chicken diseases from the JSON file
    try:
        with open(json_file_path, 'r') as f:
            disease_data = json.load(f)
    except FileNotFoundError:
        print(f"JSON file not found at path: {json_file_path}")
        return {}
        
    chicken_disease_keywords = [keyword.lower() for keyword in disease_data['chicken_diseases']]
    print("Loaded and converted chicken disease keywords to lower case from JSON ")
    # print(f"Loaded and converted chicken disease keywords to lower case from JSON = {chicken_disease_keywords}")

    # Process each interaction
    for interaction in interactions:
        user_query = interaction.question.lower()
        llm_response = interaction.response.lower()
        location_key = (interaction.latitude, interaction.longitude)

        # print(f"Processing interaction: Question='{user_query}', Response='{llm_response}', Location={location_key}")

        if None in location_key:
            print(f"Skipping interactions due to no location: {interaction}")
            continue

        # Set to keep track of diseases encountered in this interaction
        disease_encountered = set()

        # Check for each keyword in the user query and LLM response
        for keyword in chicken_disease_keywords:
            if (keyword in user_query or keyword in llm_response) and keyword not in disease_encountered:
                disease_location_counter[keyword][location_key] += 1
                disease_total_counter[keyword] += 1
                disease_encountered.add(keyword)
                # Debugging print 
                # print(f"Keyword '{keyword}' found. Updated count for location {location_key}: {disease_location_counter[keyword][location_key]}")
        
        # store location names
        if location_key not in location_name_dict:
            location_name_dict[str(location_key)] = interaction.location_name

    print("Final disease location counter:", dict(disease_location_counter))
    print("Final disease total counter:", dict(disease_total_counter))
    return disease_location_counter, disease_total_counter, location_name_dict
