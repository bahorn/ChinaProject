import json
import random
import math
# generates data based on what users like.

def personaGenerate():
    pass

# Generate fake data
def fakeFoodData(n, d):
    result = []
    for i in range(n):
        newData = [0.0 for _ in range(d)]
        newLabel = [0.0 for _ in range(d)]
        for i in range(1, random.randrange(math.ceil(d*0.1))):
            newData[i] = random.uniform(-1, 1)
        for i in range(1, random.randrange(math.ceil(d*0.15))):
            newLabel[i] = random.uniform(0, 1)
        result.append((newData, newLabel))
    return result

if __name__ == "__main__":
    fakeData = fakeFoodData(10, 5170)
    with open('./data/data.json', 'w') as fakeDataFile:
        fakeDataFile.write(json.dumps(fakeData))
    fakeDataFile.close()
