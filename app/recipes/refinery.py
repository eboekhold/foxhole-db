import json

from .shared import save

async def read_refinery_recipes():
  output_data = {}

  # Try loading preprocessed data first
  try:
    with open('public/refinery.json') as fp:
      output_data = json.load(fp)

  # If not found, process from datamines
  except FileNotFoundError:
    print("Preprocessed Refinery recipes not found. Processing...")

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
    
    # and write result to be used again
    if save:
      with open('public/refinery.json', 'w') as file:
        json.dump(output_data, file, indent=2)

  return output_data
