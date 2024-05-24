from langchain.chains import LLMChain  # pip install langchain-community, pip install -U langchain
from langchain.prompts import PromptTemplate
from langchain_community.llms import GradientLLM
# from dotenv import load_dotenv
# load_dotenv()
import os
import warnings
import sqlite3

# suppress all(including depreciation) warnings
warnings.filterwarnings("ignore")

def initialize_database():
    # connect to the SQLite db
    conn = sqlite3.connect('interactions.db')
    # call the connection
    cursor = conn.cursor()

    # create a table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS chicken_expert_app_interaction 
                   (id INTEGER PRIMARY KEY, 
                   question TEXT, 
                   response TEXT)''')
    conn.commit()
    conn.close()

# Set the environment variables for gradient.ai
os.environ['GRADIENT_ACCESS_TOKEN'] = "XBBcWHO3xsE8y6Gkx9TVW6JOLr0VUfbN"
os.environ['GRADIENT_WORKSPACE_ID'] = "6b156994-76e0-4f26-9deb-dbbcc901670c_workspace"

# Use the fine-tuned model to get 
def get_chicken_expert_response(user_query):
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

    initialize_database()

    # connect to SQLite db
    conn = sqlite3.connect('interactions.db')
    cursor = conn.cursor()

    # Insert user interactions into the db
    cursor.execute('''INSERT INTO chicken_expert_app_interaction
                   (question, response) VALUES (?, ?)''', (user_query, answer))
    conn.commit()
    conn.close()

    return answer


