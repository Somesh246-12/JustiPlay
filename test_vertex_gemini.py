import vertexai
from vertexai.preview.generative_models import GenerativeModel

PROJECT_ID = "legalease-ai-471416"   # <-- replace
LOCATION = "asia-south1"         # recommended

vertexai.init(project=PROJECT_ID, location=LOCATION)

model = GenerativeModel("gemini-2.5-flash")

response = model.generate_content("Say hello as a legal client.")
print(response.text)
