from typing import Union

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import json

app = FastAPI()


# Open access to raw data sources
app.mount("/public/", StaticFiles(directory="public"), name="public")
app.mount("/raw_data/", StaticFiles(directory="data/json2"), name="raw_data")

# Health
@app.get("/")
def read_root():
  return {"Hello": "World"}

# ============================
# == Processed Data Sources ==
# ============================

# Refinables
@app.get("/refinables")
def read_refinables():
  with open('data/json2/items_refinable.json') as fp:
    data = json.load(fp)

    output_data = {
      recipe['Refined Item Name']: {
        'Input Resource': recipe['Source Item Name'],
        'Input Amount': 1 / recipe['YieldModifier'],
        'Output Resource': recipe['Refined Item Name'],
        'Output Amount': 1,
        'Time': ((60.0 / recipe['YieldModifier']) / recipe['SpeedModifier']) * 1000,
        'Max Refined Item Count': recipe['MaxRefinedItemCount']
      }
      for _, recipe in data.items()
    }

    return output_data

