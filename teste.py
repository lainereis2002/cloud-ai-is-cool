from google import genai
GEMINI_API_KEY="AIzaSyA5JmXW5V-3717n6oTocFMJllkIzcSQLHM"

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)