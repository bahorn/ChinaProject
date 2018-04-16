import json

try:
    foods = json.load(open('./data.json'))
except:
    exit()

for food in foods:
    print food['generic_name'], food['product_name'], food['countries_en']
