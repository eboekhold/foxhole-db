from typing import Union

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import re
import json

app = FastAPI()


# Open access to raw data sources
app.mount("/public/", StaticFiles(directory="public"), name="public")
app.mount("/raw_data/", StaticFiles(directory="data/json2"), name="raw_data")

# Health
@app.get("/")
def read_health():
  return {"Hello": "World"}

# ============================
# == Processed Data Sources ==
# ============================

# Refinery
@app.get("/refinery")
def read_refinery_recipes():
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

# Factory
def without_empty_inputs(recipe):
  output = {}
  possible_input_resources = ['BMat', 'EMat', 'RMat', 'HEMat']

  for resource in possible_input_resources:
    if recipe[resource]:
      output[resource] = recipe[resource]
  
  return output


@app.get("/factory")
def read_factory_recipes():
  with open('data/json2/items_factory.json') as fp:
    data = json.load(fp)

    output_data = {
      recipe['Name']: {
        'Faction': "Colonial" if recipe['Faction Variant'] == "EFactionId::Colonials" else "Warden" if recipe['Faction Variant'] == "EFactionId::Wardens" else "Both",
        'Category': re.sub(r"(\w)([A-Z])", r"\1 \2", recipe['Type'].replace('EFactoryQueueType::', '')),
        'Input Resources': without_empty_inputs(recipe),
        'Quantity Per Crate': recipe['QuantityPerCrate'],
        'Crate Production Time': recipe['CrateProductionTime'] * 1000,
        'Time Per Item': 1000 * recipe['CrateProductionTime'] / recipe['QuantityPerCrate']
      }
      for _, recipe in data.items()
    }

    # This one is missing in the datamines
    output_data['A3 Harpa Fragmentation Grenade'] = {
      'Faction': "Warden",
      'Category': "Small Arms",
      'Input Resources': { "BMat": 100, "EMat": 40 },
      'Quantity Per Crate': 20,
      'Crate Production Time': 100 * 1000,
      'Time Per Item': 1000 * 100 / 20
    }

    return output_data