import google.generativeai as genai
import os

from dotenv import load_dotenv
load_dotenv()

# Configure your API key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Create a GenerativeModel instance
model = genai.GenerativeModel('gemini-1.5-flash')

# Generate content
prompt = "The meaning of life?"
response = model.generate_content(prompt)

# Print the response
print(response.text)
