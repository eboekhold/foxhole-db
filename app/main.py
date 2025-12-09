from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import recipes

app = FastAPI()


# Open access to raw data sources
app.mount("/public/", StaticFiles(directory="public"), name="public")
app.mount("/raw_data/", StaticFiles(directory="data/json2"), name="raw_data")

# Health
@app.get("/")
def read_health():
  return {"Hello": "World"}

# Recipes
app.include_router(recipes.router)
