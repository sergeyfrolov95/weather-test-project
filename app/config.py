from pydantic import BaseSettings, Field, RedisDsn

__all__ = ['config']


class Settings(BaseSettings):

    CACHE_REDIS_URL: RedisDsn = Field('', env='REDIS_URL')
    REDIS_CACHE_ENABLED: bool = Field(False, env='REDIS_CACHE_ENABLED')
    REDIS_CACHED_CLIENT_EXPIRATION_TIMEOUT_MINUTES: int = Field(
        60, env='REDIS_CACHED_CLIENT_EXPIRATION_TIMEOUT_MINUTES'
    )
    WEATHER_API_KEY: str = Field('', env='WEATHER_API_KEY')

    class Config:
        env_file = '.env'


config = Settings()
