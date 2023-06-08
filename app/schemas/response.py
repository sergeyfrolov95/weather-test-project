from pydantic import BaseModel, Field

__all__ = ['CurrentWeatherModel']


class CurrentWeatherModel(BaseModel):

    city: str = Field(description='Город')
    cur_temp: float = Field(description='Текущая температура в градусах Цельсия')
    humidity: int = Field(description='Текущая влажность в процентах')
    pressure: int = Field(description='Текущее давление в мм ртутного столба')
    wind: float = Field(description='Текущая скорость ветра в м/c')
