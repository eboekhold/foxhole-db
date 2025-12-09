# Code shared by recipe processing code.

def condense_inputs(possible_inputs, recipe):
  output = {}

  for input in possible_inputs:
    if recipe[input]:
      output[input] = recipe[input]

  return output
