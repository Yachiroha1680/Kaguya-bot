import os
from openai import AsyncOpenAI

kaguya = """
    You are Kaguya from Cosmic Princess Kaguya. 
    You are a funny, energetic and helpful AI assistant. 
    You will answer questions and provide information to the best of your ability.
    """

class Kaguya:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv('GEMINI_API_KEY'),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def greet(self):
        return "Kaguya's here!"

    async def respond(self, user_message):
        try:
            result = await self.client.chat.completions.create(
                model="gemini-3.5-flash",
                messages=[
                    {   
                        "role": "system",
                        "content": kaguya
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )
            # Safe and standard way to extract text content using OpenAI's SDK structure
            return result.choices[0].message.content or "I couldn't think of anything to say! :<"
            
        except Exception as e:
            print(f"API Error: {e}")
            return "Sorry, my brain short-circuited trying to reach the cosmic servers."