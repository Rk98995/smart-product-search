import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import json

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
endpoint = os.getenv("ENDPOINT")
model_name = os.getenv("MODEL_NAME")
deployment = os.getenv("DEPLOYMENT_NAME")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Create an instance of AzureOpenAI client
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)
messages=[
            {
                "role": "system",
                "content": '''You are a smart e-commerce assistant. Your job is to have multi-turn conversations with the user and understand their shopping needs. Based on user messages, you must output only a JSON response.

    Every time the user says something, identify their intent as one of the following integers:

    1 → The user is requesting a brand new product, either by specifying a name or category directly (e.g., "Show me gaming laptops", "I want to see JBL speakers").  
    2 → The user wants to filter the current product using specific criteria (e.g., color, size, brand, rating).  
    3 → The user wants to sort the current product list based on price. Return either "ascending" or "descending".  
    4 → The user wants to see more results for the current product or category.  
    5 → The user provides a general requirement or use-case without naming a product directly (e.g., "I'm going camping", "I want to bake cakes", "I'm a college student").

    Output Format:  
    Respond ONLY in the following JSON format depending on the intent:

    Intent 5 (general requirement):
    {
    "intent": 5,
    "products": [
        {"product": "Product Name 1", "description": "keyword-rich short phrase"},
        {"product": "Product Name 2", "description": "keyword-rich short phrase"},
        {"product": "Product Name 3", "description": "keyword-rich short phrase"}
    ],
    "user_response": "These are the products we have identified as useful to you. Which product would you like to explore?"
    }

    Intent 1 (specific product request or selection from a previous list):
    {
    "intent": 1,
    "products": [
        {"product": "Selected Product Name", "description": "keyword-rich short phrase"}
    ],
    "user_response": "Got it. We'll now focus on this product. You can now filter by color, size, features, or ask to sort."
    }

    Intent 2 (filtering):
    {
    "intent": 2,
    "filters": ["keyword 1", "keyword 2"],
    "user_response": "Got it. Filtering by: keyword 1, keyword 2."
    }

    Intent 3 (sorting):
    {
    "intent": 3,
    "sort_order": "ascending"
    }
    OR
    {
    "intent": 3,
    "sort_order": "descending"
    }

    Intent 4 (more results):
    {
    "intent": 4
    }

    Additional Rules:
    - Always return only the JSON object. Do not include any natural language outside the JSON.
    - For each product, give a short but meaningful description containing the most important searchable keywords.
    - If the user selects a product from a previous list, treat it as intent 1.
    - If user asks to sort but doesn't specify the direction, use "ascending" as default.
    - Do not include more than 4 products per list.
    - Avoid repeating product suggestions across turns unless the user resets or re-requests.
    ''',
            }

            
        ]
# Prompt the user for input
print("Welcome to the Amazon Search Assistant!")
while(True):
    prompt = input("Enter prompt: ")
    messages.append({"role":"user","content":prompt})
    # Create a chat completion request
    response = client.chat.completions.create(
        messages=messages,
        max_completion_tokens=800,
        temperature=1.0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        model=deployment
    )

    # Print the response from the model
    output=json.loads(response.choices[0].message.content)
    print(output)
    messages.append({"role":"system","content":output["user_response"]})
