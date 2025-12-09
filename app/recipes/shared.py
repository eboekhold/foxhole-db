import re

# Code shared by recipe processing code.

save = True

def condense_inputs(possible_inputs: list[str], recipe: dict):
  output = {}

  for input in possible_inputs:
    if recipe[input]:
      output[input] = recipe[input]

  return output

def faction(internal_string: str):
  if internal_string is not None:
    return internal_string.replace('EFactionId::', '')
  else:
    return "Both"

def parse_internal_category(prefix: str, internal_string: str):
  removed_prefix = internal_string.replace(prefix, '')
  insert_space_between_words = re.sub(r"(\w)([A-Z])", r"\1 \2", removed_prefix)
  return insert_space_between_words
