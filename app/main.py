from fastapi import FastAPI
from pydantic import BaseModel
import requests
from static import API_KEY

class InputData(BaseModel):
    city: str

app = FastAPI()


@app.post("/weather")
# async def weather(data: InputData):
async def weather(city: str):
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch weather data."}
    
    data = response.json()
    
    return {
        "city": city,
        "country": data["location"]["country"],
        "temperature": data["current"]["temp_c"],
        "feels_like": data["current"]["feelslike_c"],
        "condition_text": data["current"]["condition"]["text"],
        "local_time": data["location"]["localtime"],
        "is_day": "Yes" if data["current"]["is_day"] == 1 else "No"
    }
