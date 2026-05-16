from google import genai

# Hardcoded API key
client = genai.Client(api_key="AIzaSyDhTxDXHjTryG78frt309J223lX2GIBhWY")

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Who is albert einstein"
)

print(response.text)