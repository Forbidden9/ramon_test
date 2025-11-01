import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from config.config import settings
from core import router as core_router

_logger = logging.getLogger(__name__)

app = FastAPI(
    title = str(settings.PROJECT_NAME),
    version = str(settings.PROJECT_VERSION),
    swagger_ui_parameters = {"docExpansion": "none"}
    )

app.include_router(core_router)

@app.get("/")
def read_root():
    try:
        return JSONResponse(content={"message": "Bienvenido, Gracias por usar la API de Test"})
    except Exception as e:
        _logger.error("ERROR: %s", str(e), exc_info=True)
        return JSONResponse(content={"error": str(e)}, status_code=500)
