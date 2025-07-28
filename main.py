import os
from dotenv import load_dotenv
from openai import AzureOpenAI

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

# Prompt the user for input
print("Welcome to the Amazon Search Assistant!")
prompt = input("Enter prompt: ")

# Create a chat completion request
response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You're job is to give JSON data of products (with description attribute which mentions keywords for that) you might need to buy based on the users prompt. If the prompt is unrelated say 'I am an AI Search Assistant, nothing more than that'",
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    max_completion_tokens=800,
    temperature=1.0,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    model=deployment
)

# Print the response from the model
print(response.choices[0].message.content)