# Chicken Health Expert LLM
Welcome to the Chicken Health Expert System! This web application leverages the power of large language models (LLM) to provide expert advice on chicken health issues, locate nearby veterinary offices, and analyze disease frequencies. Built using Django and styled with Tailwind CSS, this project aims to support poultry farmers and enthusiasts by offering a comprehensive tool for managing chicken health.

## Features

- **Expert LLM Responses**: Ask any question related to chicken health and get responses powered by an LLM.
- **Find Veterinary Offices**: Locate nearby veterinary offices using geospatial data.
- **Disease Frequency Analysis**: Visualize the frequency of various chicken diseases based on gathered data.

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, Tailwind CSS
- **Geospatial Data**: Django GIS
- **LLM Integration**: use Gradientai to fine-tune **Nous-Hermes-Llama2-13b** model with chicken related data 

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/purityj/chicken-health-expert.git
   cd chicken-health-expert

