"""
This is an application that responses the calaory intake of a meal using OpenAI chat model and API calls. 
The user will share the meal or dish name and the application should return the calories of the meal.
The application should be able to handle the following:
- The user will share the dish name. 
- The application should analyse the ingredients used in the dish.
- The application should then return the calories of the meal.
"""

import os
import dotenv
from openai import OpenAI
from openai import AsyncOpenAI
from openai import ChatCompletion
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import uvicorn 

dotenv.load_dotenv()

#model = "gpt-5-mini"
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

gemini_model = "gemini-3.5-flash-lite"

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

gemini_client = AsyncOpenAI(
    base_url=GEMINI_BASE_URL,
    api_key=GEMINI_API_KEY
)

class MealRequest(BaseModel):
    dish_name: str | None = None
    meal_list: list[str] | None = None

class Nutrition(BaseModel):
    Calories: int
    Protein: int
    Carbohydrates: int
    Fat: int
    Fiber: int

class ItemNutrition(Nutrition):
    item: str

class ListNutrition(BaseModel):
    Nutritions: list[ItemNutrition]
    Total: Nutrition

app = FastAPI(
    title="A calorie tracker",
    description="Calculate the estimated calories and macronutrients of a meal."
)

@app.post("/calorie", response_model=Nutrition | ListNutrition)
async def calculate_calories(request: MealRequest):
    """Calculate the calories of a dish"""

    dish_name = request.dish_name
    meal_list = request.meal_list
    
    try:
        if meal_list:
            messages = [
                {"role": "system", "content": "You are a helpful assistant that responses the calaory intake of a meal using OpenAI chat model and API calls."},
                {"role": "user", "content": f"What is the calories of the {meal_list}"}
            ]
            response = await gemini_client.chat.completions.parse(
                model=gemini_model,
                messages=messages,
                temperature=0.0,
                response_format=ListNutrition
            )
            return response.choices[0].message.parsed

        if dish_name:
            messages = [
                {"role": "system", "content": "You are a helpful assistant that responses the calaory intake of a meal using OpenAI chat model and API calls."},
                {"role": "user", "content": f"What is the calories of the {dish_name}"}
            ]
            response = await gemini_client.chat.completions.parse(
                model=gemini_model,
                messages=messages,
                temperature=0.0,
                response_format=Nutrition
            )
            return response.choices[0].message.parsed
            
    except Exception as e:
        print(f"Error calculating calories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")