from langchain.chains import LLMChain  # pip install langchain-community, pip install -U langchain
from langchain.prompts import PromptTemplate
from langchain_community.llms import GradientLLM
from dotenv import load_dotenv
import warnings, os, json, requests, re
import sqlite3
from .models import Interaction
from spellchecker import SpellChecker


# suppress all(including depreciation) warnings
warnings.filterwarnings("ignore")

load_dotenv()

# retrieve credentials from environment variables 
GRADIENT_ACCESS_TOKEN = os.getenv('GRADIENT_ACCESS_TOKEN')
GRADIENT_WORKSPACE_ID = os.getenv('GRADIENT_WORKSPACE_ID')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# Set environment variables for gradient.ai
os.environ['GRADIENT_ACCESS_TOKEN'] = GRADIENT_ACCESS_TOKEN
os.environ['GRADIENT_WORKSPACE_ID'] = GRADIENT_WORKSPACE_ID

# resolve longitude and latitude to location name
def get_place_name(latitude, longitude, api_key):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'latlng': f'{latitude}, {longitude}',
        'key': api_key
    }
    headers = {
        'User-Agent': 'chicken_expert_llm (info@chickenexpert.com)'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  #raise a HTTP error if the HTTP request returned unsuccessful status code
        data = response.json()
        if data['results']:
            # Filter out addresses that are only plus codes
            for result in data['results']:
                formatted_address = result.get('formatted_address', '')
                if not formatted_address.startswith("MQHF+") and not formatted_address.startswith("MQJC+"):
                    return formatted_address
            
            # If no valid address found, return the first formatted address
            return data['results'][0]['formatted_address']
        else:
            return 'Unknown Location'
    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON response: {response.text}")
    return 'Unknown Location'

# check and correct spelling of user query
def correct_spelling(user_query):
    spell = SpellChecker()

    # Use regular expressions to split text into words and punctuation marks
    tokens = re.findall(r'\b\w+\b|[^\w\s]', user_query, re.UNICODE)
    
    corrected_query = []
    for token in tokens:
        if re.match(r'\b\w+\b', token):  # Check if the token is a word
            corrected_word = spell.correction(token)
            if corrected_word is None:
                corrected_word = token  # Leave the word unchanged if no correction is found
            corrected_query.append(corrected_word)
        else:
            corrected_query.append(token)  # Append punctuation marks unchanged

    return ' '.join(corrected_query)

# Use the fine-tuned model to get 
def get_chicken_expert_response(user_query, location=None):
    model_adapter_id = "fdfac42e-938e-4e52-8975-4a641261578e_model_adapter"
    
    llm = GradientLLM(
        model=model_adapter_id, 
        model_kwargs=dict(max_generated_token_count=128),
    ) 

    template = (
        f"### Instruction: {user_query} \n\n##Response:"
    )
    print(f"{template}")

    prompt = PromptTemplate(template=template, input_variables=["Instruction"])

    llm_chain = LLMChain(prompt=prompt, llm=llm)
    answer = llm_chain.run(Instruction=user_query)

    latitude = None
    longitude = None
    location_name = 'Unknown Location'

    if location:
        location_data = json.loads(location)
        latitude = location_data.get('lat')
        longitude = location_data.get('lng')
        location_name = get_place_name(latitude, longitude, GOOGLE_MAPS_API_KEY)
        print(f'Parsed location data: Latitude={latitude}, Longitude={longitude}, Location Name={location_name}')

    # save interaction using Django ORM
    interaction = Interaction(
        question=user_query, 
        response=answer,
        latitude=latitude,
        longitude=longitude,
        location_name = location_name 
    )
    interaction.save()

    # print saved interaction details for debugging
    print(f"Saved interaction: Question='{interaction.question}', Response='{interaction.response}', Latitude={interaction.latitude}, Longitude={interaction.longitude}, Location Name={location_name}")

    return answer


