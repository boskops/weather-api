from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
from static import API_KEY

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def get_home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "data": None,
        "error": None
    })

@app.post("/", response_class=HTMLResponse)
def post_home(request: Request, city: str = Form(...)):
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=yes"
    response = requests.get(url)

    if response.status_code != 200:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "data": None,
            "error": "City not found or API error."
        })

    data = response.json()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "data": data,
        "error": None
    })

# @app.post("/weather")
# async def weather(city: str):
#     url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
    
#     response = requests.get(url)
    
#     if response.status_code != 200:
#         return {"error": "Failed to fetch weather data."}
    
#     data = response.json()
    
#     return {
#         "city": city,
#         "country": data["location"]["country"],
#         "temperature": data["current"]["temp_c"],
#         "feels_like": data["current"]["feelslike_c"],
#         "condition_text": data["current"]["condition"]["text"],
#         "local_time": data["location"]["localtime"],
#         "is_day": "Yes" if data["current"]["is_day"] == 1 else "No"
#     }
