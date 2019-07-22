import json
from urllib.request import urlopen
from sys import exit
import csv

# get list of adsorbents
adsorbent_json = json.load(urlopen("https://adsorbents.nist.gov/matdb/api/materials.json"))

# get list of adsorbates
adsorbate_json = json.load(urlopen("https://adsorbents.nist.gov/isodb/api/gases.json"))


# get list of isotherms for searching
item1 = json.load(urlopen("https://adsorbents.nist.gov/isodb/api/isotherms.json"))

# list of good files
file_list = []

# list of data pts
data = []

# find hashkey for adsorbent
adsorbent_hashkey = None
while adsorbent_hashkey == None:

    adsorbent = input("adsorbent >> ")

    for x in adsorbent_json:
      if x['name'] == adsorbent or adsorbent in x['synonyms']:
        adsorbent_hashkey = x['hashkey']
        break

    if adsorbent_hashkey == None:
      print("adsorbent not found")

# find InChIKey for adsorbate
adsorbate_InChIKey = None
while adsorbate_InChIKey == None:

    adsorbate = input("adsorbate >> ")

    for x in adsorbate_json:
      if x['name'] == adsorbate or adsorbate in x['synonyms']:
        adsorbate_InChIKey = x['InChIKey']
        break

    if adsorbate_InChIKey == None:
      print("adsorbate not found")

# for each isotherm
for x in item1:
  # if adsorbate is N2 and adsorbent is CuBTC, add it to list
  if x['adsorbates'][0]['InChIKey'] == f'{adsorbate_InChIKey}' and x['adsorbent']['hashkey'] == f'{adsorbent_hashkey}' and len(x['adsorbates']) == 1:
    file_list.append(x['filename'])

# for each isotherm
for filename in file_list:
  #open JSON file
  file_ = json.load(urlopen(f"https://adsorbents.nist.gov/isodb/api/isotherm/{filename}.json"))
  print(filename)
  # if the units are what we want
  if file_['adsorptionUnits'] == 'mmol/g':
    #for each data pt
    for num in range(len(file_['isotherm_data'])):
      #for type in ['pressure', 'total_adsorption']:
        #print(f"{type}: {file_['isotherm_data'][num][type]}")
      # add data pt to list
      data.append((file_['isotherm_data'][num]['pressure'], file_['isotherm_data'][num]['species_data'][0]['adsorption'], filename))
      print((file_['isotherm_data'][num]['pressure'], file_['isotherm_data'][num]['species_data'][0]['adsorption']))

with open("out.csv", 'w') as out:
    fieldnames = ['pressure', 'Q', 'filename']
    writer = csv.DictWriter(out, fieldnames=fieldnames)

    writer.writeheader()

    for datapoint in data:
        writer.writerow({'pressure': datapoint[0], 'Q': datapoint[1], 'filename': datapoint[2]})

    out.close()
