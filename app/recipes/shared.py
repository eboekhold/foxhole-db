# Code shared by recipe processing code.

save = True

def condense_inputs(possible_inputs, recipe):
  output = {}

  for input in possible_inputs:
    if recipe[input]:
      output[input] = recipe[input]

  return output

def faction(internal_string):
  if internal_string is not None:
    return internal_string.replace('EFactionId::', '')
  else:
    return "Both"
