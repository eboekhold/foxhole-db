import json

from .shared import condense_inputs, faction, CACHE_RESULTS, parse_internal_category

FACTORY_VEHICLE_INPUTS = [
  'BMat', 
  'RMat', 
  'Relic', 
  'PCMat'
]

FACILITY_VEHICLE_INPUTS = [
  '(Fac) CMat', 
  '(Fac) PCMat', 
  '(Fac) SCMat', 
  '(Fac) AssMat1', 
  '(Fac) AssMat2', 
  "(Fac) AssMat3", 
  "(Fac) AssMat4", 
  "(Fac) AssMat5", 
  "(Fac) Rare Alloys", 
  "(Fac) Hull Segments", 
  "(Fac) Shell Plating", 
  "(Fac) Turbine Components"
]

VEHICLE_INPUTS = FACTORY_VEHICLE_INPUTS + FACILITY_VEHICLE_INPUTS


# Esoteric process to determine which structure the vehicle comes from because:
# - Usually the VehicleBuildType will mention where you can build it but:
#   - There are VehicleBuildType:none that are built in the VehicleFactory
#   - There is a VehicleBuildType:BuildableAnywhere that is not buildable anywhere but is in fact built in a facility
#   - There is no VehicleBuildType:Facility, but you have to deduce it from its ingredients:
#     - If VehicleBuildType:none AND it has facility ingredients, it's a facility vehicle but:
#       - There are also Vehicles with facility costs that are not built in a facility
def structure(vehicle: dict):
  internal_string = vehicle['VehicleBuildType'] # ex. "EVehicleBuildType::VehicleFactory"

  # First check if the data mentions it being built in a VehicleFactory (Garage) or Shipyard.
  if internal_string:
    without_prefix = internal_string.replace('EVehicleBuildType::', '')
    if without_prefix == "VehicleFactory":
      return "Garage"
    elif without_prefix == "Shipyard":
      return "Shipyard"

  # Then check if it has costs associated with facilities
  if len(condense_inputs(FACILITY_VEHICLE_INPUTS, vehicle)) > 0:
    return 'Facility'
  # Catch the two vehicles that cost rmats and have BuildType::None but are in fact built in the Garage
  elif vehicle['RMat']:
    return "Garage"
  # Catch exceptions such as landing ships built at Large Ships, that one facility rail crane, and the motorboat built anywhere
  elif internal_string:
    return parse_internal_category('EVehicleBuildType::', internal_string)
  # Catch exceptions such as bicycles and inactive content.
  else:
    return internal_string


async def read_vehicle_recipes():
  output_data = {}

  # Try loading preprocessed data first
  try:
    with open('public/vehicles.json') as fp:
      output_data = json.load(fp)

  # If not, process from the datamines
  except FileNotFoundError:
    print("Preprocessed Vehicle recipes not found, Processing...")

    # == Load data from the vehicles datamine first ==
    with open('data/json2/vehicles.json') as fp:
      data = json.load(fp)

      output_data = {
        vehicle['Name']: {
          'Output Internal ID': internal_id,
          'Faction': faction(vehicle['Faction Variant']),
          'Structure': structure(vehicle),
          'Input Resources': condense_inputs(VEHICLE_INPUTS, vehicle),
          'Input Vehicle ID': None, # these will be overwritten later if they have an input vehicle
          'Input Vehicle': None,
        }
        for internal_id, vehicle in data.items()
      }

    # Delete entries that we know can't be built or are inactive content
    output_data.pop('Blumfield LK205', None) # bicycle
    output_data.pop('Centurion MV-2', None) # mech
    output_data.pop('Herne QMW 1a Scourge Hunter', None) # mech
    output_data.pop('Heavy Infantry Carrier', None) # -- relic content start
    output_data.pop('Armoured Fighting Tractor', None)
    output_data.pop('Storm Tank', None)
    output_data.pop('PL-1 "Phalanx"', None)
    output_data.pop('Staff Car', None)
    output_data.pop('Repurposed Truck', None) # -- relic content end
    output_data.pop('Player Imposter', None)
    output_data.pop('null', None)
    output_data.pop(None, None)

    # Remove unused input costs based on structure. Garage vehicles don't use facility resources & vice-versa.
    for _, vehicle in output_data.items():
      if vehicle['Structure'] == "Garage":
        for k in FACILITY_VEHICLE_INPUTS:
          vehicle['Input Resources'].pop(k, None)
      elif vehicle['Structure'] == 'Facility':
        for k in FACTORY_VEHICLE_INPUTS:
          vehicle['Input Resources'].pop(k, None)

    # Add crafting times to Non-facility vehicles. It's the amount of resources * 1100 (that's how long a hammer swing lasts in ms)
    # Non-facility vehicles never have more than 1 resource as input so we can just take the first one.
    non_facility_vehicles = {_: v for _, v in output_data.items() if v.get('Structure') != 'Facility'}

    for _, vehicle in non_facility_vehicles.items():
      vehicle['Time'] = next(iter(vehicle['Input Resources'].values())) * 1100


    # == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
    # == Go through all of the facility recipes for crafting times and base vehicles (those stats are not in the vehicles json) ==
    # == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==

    with open('data/json2/facilities_assembly.json') as fp:
      facility_datamine = json.load(fp)

    # Prepare info from datamine for processing
    facility_data = {
      (facility_recipe['Assembled Vehicle']).lower(): { # Force lowercase to avoid inconsistent capitalisation
        'Input Vehicle ID': facility_recipe['Required Vehicle'],
        'Time': 1000 * facility_recipe['Production Time']
      }
      for _, facility_recipe in facility_datamine.items()
    }

    # Go through all of the vehicles that are built in facility
    facility_vehicles = {_: v for _, v in output_data.items() if v['Structure'] == 'Facility'}
    for _, vehicle in facility_vehicles.items():

      matching_facility_data = facility_data[vehicle['Output Internal ID'].lower()] # Find the matching vehicle in the facility data

      if matching_facility_data['Input Vehicle ID'] != 'None': # if the vehicle has an upgrade, add that info to the output
        vehicle_data_key = matching_facility_data['Input Vehicle ID'].replace('Halftrack', 'HalfTrack') # avoid inconsistent naming

        vehicle['Input Vehicle ID'] = vehicle_data_key
        vehicle['Input Vehicle'] = data[vehicle_data_key]['Name']
      else:
        vehicle['Input Vehicle ID'] = None
        vehicle['Input Vehicle'] = None

      vehicle['Time'] = matching_facility_data['Time']
    

    if CACHE_RESULTS:
      with open('public/vehicles.json', 'w') as file:
        json.dump(output_data, file, indent=2)
    
  return output_data
