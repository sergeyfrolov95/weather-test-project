import json

import requests
import logging
import redis

from config import config

logger = logging.getLogger(__name__)

__all__ = ['get_weather_client']


class WeatherAPIClient:

    WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'

    def __init__(self, api_token: str):
        self.appid = api_token

    def get_weather_for_city(self, city: str, lang: str, units: str):
        try:
            response = requests.get(
                url=self.WEATHER_URL,
                params={
                    'q': city,
                    'lang': lang or 'en',
                    'units': units or 'metric',
                    'appid': self.appid
                }
            )
            response.raise_for_status()
        except requests.HTTPError:
            logger.exception('HTTP error occurred on sending request')
            return
        except Exception:
            logger.exception('Exception occurred on sending request')
            return
        data = response.json()
        return {
            'city': data["name"],
            "cur_temp": data["main"]["temp"],
            'humidity': data["main"]["humidity"],
            'pressure': data["main"]["pressure"],
            "wind": data["wind"]["speed"]
        }


class RedisCachedWeatherAPIClient:

    def __init__(self, client: WeatherAPIClient):

        self.client = client
        self.redis_client = redis.Redis.from_url(config.CACHE_REDIS_URL)
        self.redis_expiration = int(config.REDIS_CACHED_CLIENT_EXPIRATION_TIMEOUT_MINUTES) * 60

    def __getattr__(self, attr):

        if hasattr(self.client, attr):
            def wrapper(*args, **kwargs):

                redis_key = ['weather-api', attr]
                redis_key.extend(args)
                redis_key.extend(kwargs.values())
                redis_key = ', '.join([str(r) for r in redis_key])
                cashed_value = self.redis_client.get(redis_key)

                if cashed_value:
                    logger.info(f'Got value for {attr} from cache')
                    return json.loads(cashed_value)
                else:
                    logger.info(f'No cached value for {attr}, updating...')
                    result = getattr(self.client, attr)(*args, **kwargs)
                    self.redis_client.set(redis_key, json.dumps(result))
                    self.redis_client.expire(redis_key, self.redis_expiration)

                    return result

            return wrapper
        raise AttributeError(attr)


def get_weather_client() -> WeatherAPIClient:
    weather_client = WeatherAPIClient(
        config.WEATHER_API_KEY
    )

    return RedisCachedWeatherAPIClient(weather_client) if config.REDIS_CACHE_ENABLED else weather_client
