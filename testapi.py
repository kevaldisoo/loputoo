from openrouter import OpenRouter
from dotenv import load_dotenv
load_dotenv()
import os

with OpenRouter(
    api_key=os.getenv("OPENROUTER_API_KEY")
) as client:
    print(os.getenv("OPENROUTER_API_KEY"))
    response = client.chat.send(
        model="minimax/minimax-m2.5:free",
        messages=[
            {"role": "user", "content": "Explain quantum computing"}
        ]
    )

    print(response.choices[0].message.content)
