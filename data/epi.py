import csv

with open('epi_r.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader:
        print line['']

