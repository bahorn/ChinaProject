import csv
from fuzzywuzzy import fuzz, process
import json

def cleanName(name):
    cleaned = ""
    for i in name.lower():
        if ord(i) < 128: cleaned += i
        else: pass
    return cleaned

# stolen from stack overflow.
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

# Include the FooDB food database.
def loadAllFoods(file='./data/foods.csv'):
    ingredientIds = {}
    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            name = cleanName(line[1])
            ingredientIds[name] = {
                'id': line[0],
                'name': line[1].lower(),
                'desc': line[3].lower()
            }
    return ingredientIds

def loadAllFlavors(file='./data/flavors.csv'):
    flavorIds = {}
    inverseFlavorIds = {}
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            flavorIds[line['id']] = line['name']
            inverseFlavorIds[line['name']] = line['id']
    return flavorIds, inverseFlavorIds

def loadAllCompoundFlavors(flavors, file='./data/compounds_flavors.csv'):
    compoundFlavorIds = {}
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            if line['compound_id'] in compoundFlavorIds:
                compoundFlavorIds[line['compound_id']].append(
                    flavors[line['flavor_id']])
            else:
                compoundFlavorIds[line['compound_id']] = [
                    flavors[line['flavor_id']]]
    return compoundFlavorIds

# Only get WesternEuropean or EastAsian foods.
def loadAllDishes(file='./data/cusinefoods.csv'):
    dishes = []
    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            if line[0] in ['EastAsian', 'WesternEuropean']:
                dishes.append(
                    {
                        'name':"_",
                        'type':line[0],
                        'items':line[1::]
                    })
    return dishes

def matchIngredient(ingredient, foods):
    result = process.extractOne(ingredient.replace('-', ' '), foods.keys(),
                       scorer=fuzz.token_sort_ratio)
    if result[1] < 65:
        return {}
    else:
        return {
            'id': foods[result[0]]['id'],
            'name': foods[result[0]]['name'],
        }

# Returns compound Ids for all of these ingredients.
# SLOOOOOW FUNCTION. RUN ONCE AT STARTUP.
def lookupIngredientCompounds(ingredients, flavors, file='./data/contents.csv'):
    ingredientCompounds = {}
    ids = [i['id'] for i in ingredients]
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            # only care about compounds, not nutrients
            if line['source_type'] != 'Compound':
                continue
            if line['food_id'] in ids:
                newData = {
                    'source_id':line['source_id'],
                    'content_avg':line['orig_content'],
                    'content_min':line['orig_min'],
                    'content_max':line['orig_max'],
                    'content_unit':line['orig_unit'],
                }
                # sometimes they don't have a recorded flavor
                try:
                    newData['flavors'] = flavors[line['source_id']]
                except KeyError:
                    pass

                if line['food_id'] in ingredientCompounds:
                    ingredientCompounds[line['food_id']].append(newData)
                else:
                    ingredientCompounds[line['food_id']] = [newData]

    return ingredientCompounds

# Could do something based on concentration, would have to deal with units then
# though
def computeCompoundScore(compound):
    return 1

# Generate scores for a dish.
def scoreDish(dish, cachedIngredients, ingredientLookup):
    flavors = {}
    highest = 0
    for item in dish['items']:
        this = {}
        try:
            this = cachedIngredients[ingredientLookup[item]['id']]
        except KeyError:
            continue
        for compound in this:
            # only track ones with flavors
            if 'flavors' not in compound:
                continue
            compoundScore = computeCompoundScore(compound)
            for flavor in compound['flavors']:
                if flavor not in flavors:
                    flavors[flavor] = compoundScore
                else:
                    flavors[flavor] += compoundScore
                if flavors[flavor] > highest: highest = flavors[flavor]
    for flavor in flavors:
        flavors[flavor] = translate(flavors[flavor], 0, highest, 0, 1)
    return flavors

# Get the score in a suitable form for machine learning.
def vectoriseScore(score, inverseFlavors):
    vector = [0 for _ in inverseFlavors]
    for flavor in score.keys():
        vector[int(inverseFlavors[flavor])-1] = score[flavor]
    return vector

# Setup
def main():
    # Initialize our lists/dicts
    ingredientLookup = {}
    ingredients = []
    uniqueIngredients = []
    # load in a few datasets.
    foods = loadAllFoods()
    flavors, inverseFlavors = loadAllFlavors()
    compoundFlavors = loadAllCompoundFlavors(flavors)
    dishes = loadAllDishes()
    # Get a list of ingredients to look up.
    for dish in dishes:
        for item in dish['items']:
            if item not in ingredients:
                ingredients.append(item)
                t = matchIngredient(item, foods)
                if t != {}:
                    uniqueIngredients.append(t)
                    # more of a hack.
                    ingredientLookup[item] = t

    # Find out what flavor each ingredient has.
    cachedIngredients = lookupIngredientCompounds(uniqueIngredients,
                            compoundFlavors)
    allScores = []
    thisId = 0
    # generate the vector for each dish
    for dish in dishes:
        score = scoreDish(dish, cachedIngredients, ingredientLookup)
        allScores.append({
            'id':thisId,
            'name':dish['name'],
            'type':dish['type'],
            'scores':vectoriseScore(score, inverseFlavors)
        })
        thisId += 1

    f = open('./data/flavorValues.json', 'w')
    f.write(json.dumps(allScores))
    f.close()

if __name__ == "__main__":
    main()
