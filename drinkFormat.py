import json
from enum import Enum

class Category(Enum):
    ALCOHOL = 0
    MIXER = 1
    OTHER = 2


with open('base-ingredients.json') as data_file:
    data = json.load(data_file)

with open('all-drinks.json') as drink_data:
    drinks = json.load(drink_data)


def lookup_by_name(ingredient_name):
    return [ing for ing in data if ingredient_name.lower() == ing['Name'].lower()][0]


def get_category(ingredient_name):
    return lookup_by_name(ingredient_name)['Category']


def ml_to_oz(ml):
    return float(ml) * .033814


def shot_to_oz(shots):
    return float(shots) * 1.5


def convert_to_oz(ingredient):
    if (ingredient['Measurement'] == 'ml'):
        ingredient['Measurement'] = 'oz'
        ingredient['Amount'] = ml_to_oz(convert_mixed_number(ingredient['Amount']))
        return ingredient
    elif (ingredient['Measurement'] == 'shot'):
        ingredient['Measurement'] = 'oz'
        ingredient['Amount'] = shot_to_oz(convert_mixed_number(ingredient['Amount']))
        return ingredient
    else:
        if (ingredient['Amount'] != '' and get_category(ingredient['Name']) != Category.OTHER):
            ingredient['Amount'] = convert_mixed_number(ingredient['Amount'])
        return ingredient


def parse_frac(fraction):
    numer = float(str.split(fraction, '/')[0])
    denom = float(str.split(fraction, '/')[1])
    return numer/denom


def convert_mixed_number(num):
    vals = str.split(num, ' ')
    if (len(vals) > 1):
        return float(vals[0]) + float(parse_frac(vals[1]))
    elif (len(str.split(vals[0], '/')) > 1):
        return parse_frac(vals[0])
    else:
        return float(vals[0])


def convert_drink(drink):
    drink['Ingredients'] = [convert_to_oz(ing) for ing in drink['Ingredients']]
    return drink

converted_drinks = [convert_drink(drink) for drink in drinks]

for drink in converted_drinks:
    for ingredient in drink['Ingredients']:
        ingredient.update({'ID' : lookup_by_name(ingredient['Name'])['ID']})

formatted_drinks = [{'Name' : drink['Name'], 'Ingredients' : [{'ID' : ing['ID'], 'Name' : ing['Name'], 'Quantity' : ing['Amount'], 'Units' : ing['Measurement']} for ing in drink['Ingredients']]} for drink in converted_drinks]

with open('formatted-drinks.json', 'w') as outfile:
    json.dump(formatted_drinks, outfile)
