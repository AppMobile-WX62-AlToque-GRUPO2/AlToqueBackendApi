from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.routes import router 
from config.database import engine
import models.models as models

app = FastAPI(title="AlToqueAPI")
models.Base.metadata.create_all(bind=engine)

@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs", status_code=300)

app.include_router(router)