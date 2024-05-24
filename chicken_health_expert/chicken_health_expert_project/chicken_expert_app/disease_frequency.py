import sqlite3
from collections import Counter
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from chicken_expert_app.expert_llm import initialize_database

def get_disease_frequency():
    initialize_database()
    try:
        # connect to sqlite3 db
        conn = sqlite3.connect('interactions.db')
        cursor = conn.cursor()
        print('Database connection successful!')

        # fetch user queries and llm_responses from the interactions table interactions
        cursor.execute("SELECT question, response FROM chicken_expert_app_interaction")
        rows = cursor.fetchall()
        conn.close()

    except sqlite3.Error as e:
        print("Database connection error:", e)

    # convert fetched data into tuple format
    user_queries_and_response = [(row[0], row[1]) for row in rows]

    # initialize a set to keep track of diseases encountered in each pair
    diseases_encountered = set()

    # define a list of keywords related to chicken diseases
    chicken_disease_keywords = [
        "Newcastle",
        "coccidiosis",
        "Marek's",
        "swollen crop",
        "avian influenza"
    ]

    # initialize a counter to store the frequency of each chicken disease
    keyword_counter = Counter()

    # process each user query and llm response pair 
    for user_query, llm_response in user_queries_and_response:
        # preprocess the query and response by lowercasing 
        user_query = user_query.lower()
        llm_response = llm_response.lower()

        # initialize a flag to check if the disease has already been encountered in this pair
        diseases_encountered_in_pair = False

        # check if any keyword exists in the query or response
        for keyword in chicken_disease_keywords:
            if keyword.lower() in user_query:
                # if the keyword is found in the user query and it's not encountered before in this pair
                if keyword not in diseases_encountered:
                    # update the counter
                    keyword_counter[keyword] += 1
                    # add the keyword to the set of diseases encountered in this pair
                    diseases_encountered.add(keyword)
                    # set the flag to True to indicate the disease has been encountered before in this pair 
                    diseases_encountered_in_pair = True
            elif keyword.lower() in llm_response:
                # if keyword is found in llm_response and it's not encountered before in this pair 
                if keyword not in diseases_encountered:
                    # update the counter 
                    keyword_counter[keyword] += 1
                    # add the keyword to the set of diseases encountered in this pair 
                    diseases_encountered.add(keyword)
                    # set the flag to true to indicate the disease has been encountered in this pair 
                    diseases_encountered_in_pair = True
        
        # if a disease was encountered in this pair, clear the set for the next pair
        if diseases_encountered_in_pair:
            diseases_encountered.clear()

    return keyword_counter
