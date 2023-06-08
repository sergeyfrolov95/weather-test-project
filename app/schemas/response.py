from pydantic import BaseModel, Field

__all__ = ['CurrentWeatherModel']


class CurrentWeatherModel(BaseModel):

    city: str = Field(description='City')
    cur_temp: float = Field(description='Current temperature in degrees Celsius')
    humidity: int = Field(description='Current humidity percentage')
    pressure: int = Field(description='Current pressure in mmHg')
    wind: float = Field(description='Current wind speed in m/s')
