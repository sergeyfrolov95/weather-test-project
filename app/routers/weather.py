from fastapi import APIRouter, HTTPException

from common.weather_client import get_weather_client
from schemas import CurrentWeatherModel

weather_router = APIRouter(prefix='/api/v1/weather')


@weather_router.get("/get_weather/{city}", status_code=200, response_model=CurrentWeatherModel)
def get_weather(*, city: str, lang: str = None, units: str = None) -> dict:

    weather_client = get_weather_client()
    resp = weather_client.get_weather_for_city(
        city=city,
        lang=lang,
        units=units
    )
    if not resp:
        raise HTTPException(404, 'City not found.')

    return resp
