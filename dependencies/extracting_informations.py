import requests
from bs4 import BeautifulSoup
import spacy

# Load the SpaCy English model
nlp = spacy.load("en_core_web_sm")

def extract_organization_info(url):
    # Send a GET request to the organization's URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Extract text content from the HTML response
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        
        # Process the text using SpaCy
        doc = nlp(text)
        
        # Extract relevant organization information (e.g., name, key personnel)
        organization_info = {
            'text': text,
            # You can extract more specific information based on your requirements
        }
        
        return organization_info
    else:
        print("Failed to fetch content from the URL.")
        return None

def verify_user_identity(user_data, organization_info):
    # Extract relevant user data (e.g., name, email) from the user's information
    user_name = user_data.get('name', '').lower()
    user_email = user_data.get('email', '').lower()
    
    # Extract relevant organization information (e.g., name, key personnel) from the website content
    org_text = organization_info.get('text', '').lower()
    
    # Perform identity verification based on extracted information
    if user_name in org_text and user_email in org_text:
        return True  # Identity verified
    else:
        return False  # Identity not verified

# Example user data and organization URL
user_data = {'name': 'John Smith', 'email': 'john@example.com'}
organization_url = 'https://www.knust.edu.gh/'

# Extract organization information from the provided URL
organization_info = extract_organization_info(organization_url)

if organization_info:
    # Verify user identity based on extracted information
    if verify_user_identity(user_data, organization_info):
        print("User identity verified.")
    else:
        print("User identity not verified.")
