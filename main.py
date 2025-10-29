import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from instabot import Bot
from config.config import settings
from core import router as core_router
from db.session import reboot_database

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title = str(settings.PROJECT_NAME),
    version = str(settings.PROJECT_VERSION),
    swagger_ui_parameters = {"docExpansion": "none"}
    )

app.include_router(core_router)

@app.get("/")
def read_root():
    return JSONResponse(content={"message": "Bienvenido, Gracias por usar la API de Test"})

@app.get("/reboot_database", summary="Reboot database", description="Roboot database")
async def create_tables():
    await reboot_database()
    return JSONResponse(content={"message": "Reboot database successfully !!!"})
FastAPI()
