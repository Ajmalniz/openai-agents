import os
import openai
from dotenv import load_dotenv

load_dotenv()

def main():
    client = openai.Client(
        api_key=os.getenv("GOOGLE_API_KEY"),  # Explicitly passing API key
        base_url="https://generativelanguage.googleapis.com/v1beta"  # Google Gemini API base
    )

    response = client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[{"role": "user", "content": "Explain AI in simple terms."}]
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
