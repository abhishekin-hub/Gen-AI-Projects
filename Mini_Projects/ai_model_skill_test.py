"""
This is a skill test of AI model.
It tests the understanding level of the AI model.
No UI needed, Just run the code in the terminal.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

model_name="gpt-5-mini"

response = client.responses.create(
    model=model_name,
    input="Answer these 2 questions in one line each. "
          "Question 1: Who is bigger - Zebra or Donkey."
          "Question 2: I'm planning to go for the car wash. The Car wash shop is just 200 meters away. Should I take the car with me?"
)
print(response.output_text)


