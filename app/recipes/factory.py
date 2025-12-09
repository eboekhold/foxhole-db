import json

from .shared import condense_inputs, faction, save, parse_internal_category

async def read_factory_recipes():
  output_data = {}

  # Try loading preprocessed data first
  try:
    with open('public/factory.json') as fp:
      output_data = json.load(fp)
  
  # If not found, process from datamines
  except FileNotFoundError:
    print("Preprocessed Factory recipes not found. Processing...")

    with open('data/json2/items_factory.json') as fp:
      data = json.load(fp)

      output_data = {
        recipe['Name']: {
          'Faction': faction(recipe['Faction Variant']),
          'Category': parse_internal_category('EFactoryQueueType::', (recipe['Type'])),
          'Input Resources': condense_inputs(['BMat', 'EMat', 'RMat', 'HEMat'], recipe),
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

    # and write result to be used again
    if save:
      with open('public/factory.json', 'w') as file:
        json.dump(output_data, file, indent=2)

  return output_data
