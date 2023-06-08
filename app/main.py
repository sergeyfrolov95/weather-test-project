from fastapi import FastAPI

from app.routers import weather_router


app = FastAPI(title="Weather API")
app.include_router(weather_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, log_level="debug")
