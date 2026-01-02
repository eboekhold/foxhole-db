from fastapi import APIRouter

from ..recipes.refinery import read_refinery_recipes
from ..recipes.factory import read_factory_recipes
from ..recipes.vehicles import read_vehicle_recipes

router = APIRouter()

@router.get("/recipes/", tags=["recipes"])
async def read_recipes():
  return {"Sorry": "Not Implemented Yet"}

@router.get("/recipes/refinery", tags=["recipes"])
async def read_recipes_refinery():
  return await read_refinery_recipes()

@router.get("/recipes/factory", tags=["recipes"])
async def read_recipes_factory():
  return await read_factory_recipes()

@router.get("/recipes/vehicles", tags=["recipes"])
async def read_recipes_vehicles():
  return await read_vehicle_recipes()
