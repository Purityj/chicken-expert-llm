from langchain.chains import LLMChain  # pip install langchain-community, pip install -U langchain
from langchain.prompts import PromptTemplate
from langchain_community.llms import GradientLLM
# from dotenv import load_dotenv
# load_dotenv()
import os
import json
import warnings
import sqlite3
from .models import Interaction

# suppress all(including depreciation) warnings
warnings.filterwarnings("ignore")

# Set the environment variables for gradient.ai
os.environ['GRADIENT_ACCESS_TOKEN'] = "XBBcWHO3xsE8y6Gkx9TVW6JOLr0VUfbN"
os.environ['GRADIENT_WORKSPACE_ID'] = "6b156994-76e0-4f26-9deb-dbbcc901670c_workspace"

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

    if location:
        location_data = json.loads(location)
        latitude = location_data.get('lat')
        longitude = location_data.get('lng')
        print(f'Parsed location data: Latitude={latitude}, Longitude={longitude}')

    # save interaction using Django ORM
    interaction = Interaction(
        question=user_query, 
        response=answer,
        latitude=latitude,
        longitude=longitude
    )
    interaction.save()

    return answer


