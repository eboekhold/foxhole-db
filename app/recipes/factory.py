import json
import re

def factory_without_empty_inputs(recipe):
  output = {}
  possible_input_resources = ['BMat', 'EMat', 'RMat', 'HEMat']

  for resource in possible_input_resources:
    if recipe[resource]:
      output[resource] = recipe[resource]
  
  return output


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
          'Faction': "Colonial" if recipe['Faction Variant'] == "EFactionId::Colonials" else "Warden" if recipe['Faction Variant'] == "EFactionId::Wardens" else "Both",
          'Category': re.sub(r"(\w)([A-Z])", r"\1 \2", recipe['Type'].replace('EFactoryQueueType::', '')),
          'Input Resources': factory_without_empty_inputs(recipe),
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
    with open('public/factory.json', 'w') as file:
      json.dump(output_data, file, indent=2)

  return output_data
