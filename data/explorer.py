import json

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

print(chinese_meals, 'of Chinese origin.')
print(british_meals, 'of British origin.')

for food in foods:
	for country in food['countries_en'].split(','):
		if country in ['China','Hong Kong','Singapore']:
			print(food)

#print(national_origins)
