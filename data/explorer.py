import json

#English Name, Chinese Name, Image, price?, flvours?

#GET EXPLORER WORKING, RENDER JSON

uk_name = 'United Kingdom'
cn_name = 'China'

def get_data(filename):
    with open(filename) as json_file:
        foods = json.load(json_file)
    return foods

foods = get_data('bearsdata.json')

#print(foods[0])


'''
Code for exploring old dataset
with open('data.json') as json_file:
    foods = json.load(json_file)

national_origins = {}

for food in foods:
    for country in food['countries_en'].split(','):
        if country not in national_origins:
            national_origins[country] = 1
        else:
            national_origins[country] += 1

print(len(foods), 'foods in json file.')

chinese_meals = national_origins['China'] + national_origins['Hong Kong'] + national_origins['Singapore']
british_meals = national_origins['United Kingdom']

#can take a string or list of strings
def foods_from(origin_countries):
    national_foods = []
    for food in foods:
        for country in food['countries_en'].split(','):
            if country in origin_countries:
                national_foods.append(food)
    return national_foods

chinese_foods = foods_from(['China','Hong Kong','Singapore'])
british_foods = foods_from('United Kingdom')

print(len(chinese_foods), 'of Chinese origin.')
print(len(british_foods), 'of British origin.')

##for food in foods:
##    for country in food['countries_en'].split(','):
##        if country in ['China','Hong Kong','Singapore']:
##            chinese_foods.append(food)

#Will show all non ingredient keys

#print all tags
##def get_tags():
##    for key in foods[0]:
##        if '100g' not in key:
##            print(key)
#print(national_origins)

for i in range(50):
    print(british_foods[i]['product_name'])

'''
