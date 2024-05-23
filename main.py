from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.routes import router 
from config.database import engine
import models.models as models
from routes.auth import auth_router
from dotenv import load_dotenv

app = FastAPI(title="AlToqueAPI")
models.Base.metadata.create_all(bind=engine)

@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs", status_code=300)

load_dotenv()
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(router)