import base64 
import os
import json
import requests
import azure.functions as func
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# Get the environment variables
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_ENDPOINT = os.environ['OPENAI_ENDPOINT']
OPENAI_DEPLOYMENT_NAME = os.environ['OPENAI_DEPLOYMENT_NAME']
SEARCH_API_KEY = os.environ['SEARCH_API_KEY']
SEARCH_ENDPOINT = os.environ['SEARCH_ENDPOINT']
SEARCH_INDEX_NAME = os.environ['SEARCH_INDEX_NAME']

# Initialize the Azure OpenAI headers
openai_headers = {
    'Authorization': 'Bearer {}'.format(OPENAI_API_KEY),
    'Content-Type': 'application/json'
}

# Initialize the Azure Search client
search_credentials = AzureKeyCredential(SEARCH_API_KEY)
search_client = SearchClient(SEARCH_ENDPOINT, SEARCH_INDEX_NAME, search_credentials)

app = func.FunctionApp()

@app.route(route="stylist", methods=["post"], auth_level=func.AuthLevel.FUNCTION)
def stylist(req: func.HttpRequest) -> func.HttpResponse:
    # get image from request and convert to a base64 string
    image = req.files["image"]
    image_bytes = image.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # Generate a text description from the image using Azure OpenAI
    base_url = f"{OPENAI_ENDPOINT}openai/deployments/{OPENAI_DEPLOYMENT_NAME}"
    endpoint = f"{base_url}/chat/completions?api-version=2023-12-01-preview"
    data = {
        "messages": [
            { "role": "system", "content": "You are a helpful assistant." },
            { "role": "user", "content": [
                {
                    "type": "text",
                    "text": "Describe the main fashion item in this picture. Make sure you include the type of item (e.g. Shirt, T-Shirt, Shorts, Pants, Dress, Purse, Clutch), the color of the item, and 'Men' or 'Women' if the fashion item appears to be specific to either of those genders."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_base64
                    }
                }
            ] }
        ],
        "max_tokens": 2000
    }

    response = requests.post(endpoint, headers=openai_headers, data=json.dumps(data))
    result = response.json()
    image_description = result['text']

    # Find the closest match from the search index using Azure OpenAI
    search_result = search_client.search(
        search_text=image_description,
        select=["id", "productDisplayName"],
        top=1
    )
    match_id = search_result["id"]
    match_name = search_result["productDisplayName"]

    # Generate a natural language recommendation based on the match result using Azure OpenAI
    data = {
        "messages": [
            { "role": "system", "content": "You are a helpful assistant." },
            { "role": "user", "content": [
                {
                    "type": "text",
                    "text": f"Please generate a natural language recommendation based on the matching item: {match_id}, {match_name}. For example: The best match for your clothing item is: Peter England Men Party Blue Jeans. This is a pair of jeans for men in blue color, suitable for casual occasions. You can pair it with a shirt or a t-shirt of your choice."
                }
            ] }
        ],
        "max_tokens": 2000
    }
    response = requests.post(endpoint, headers=openai_headers, data=json.dumps(data))
    result = response.json()
    recommendation = result['text']

    # Return the recommendation as a JSON response
    return func.HttpResponse(json.dumps({
        'image_id': match_id,
        'recommendation': recommendation
    }))