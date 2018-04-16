import csv
import sys
import json
csv.field_size_limit(sys.maxsize)

allData = []
with open('./en.openfoodfacts.org.products.tsv', 'rU') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    for line in reader:
        try:
            for country in line['countries_en'].split(','):
                if country in ['China','United Kingdom']:
                    allData.append(line)
        except AttributeError:
            pass


print json.dumps(allData)
