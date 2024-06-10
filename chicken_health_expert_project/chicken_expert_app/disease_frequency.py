from collections import defaultdict
from .models import Interaction

def get_disease_frequency():
    try:
        # Fetch user queries and llm responses from the database
        interactions = Interaction.objects.all()
        print(f"Fetched {len(interactions)} interactions from the database.")
    except Exception as e:
        print("Database connection error:", e)
        return {}

    # Initialize a nested dictionary to store the frequency of each disease per location
    disease_location_counter = defaultdict(lambda: defaultdict(int))

    # List of keywords related to chicken diseases
    chicken_disease_keywords = [
        "newcastle",
        "coccidiosis",
        "marek's",
        "swollen crop",
        "avian influenza",
        "aspergillosis",
    ]
    print("Defined chicken disease keywords.")

    # Process each interaction
    for interaction in interactions:
        user_query = interaction.question.lower()
        llm_response = interaction.response.lower()
        location_key = (interaction.latitude, interaction.longitude)

        # print(f"Processing interaction: Question='{user_query}', Response='{llm_response}', Location={location_key}")

        if None in location_key:
            continue

        # Set to keep track of diseases encountered in this interaction
        disease_encountered = set()

        # Check for each keyword in the user query and LLM response
        for keyword in chicken_disease_keywords:
            if (keyword in user_query or keyword in llm_response) and keyword not in disease_encountered:
                disease_location_counter[keyword][location_key] += 1
                disease_encountered.add(keyword)
                # print(f"Keyword '{keyword}' found. Updated count for location {location_key}: {disease_location_counter[keyword][location_key]}")

    print("Final disease location counter:", dict(disease_location_counter))
    return disease_location_counter
