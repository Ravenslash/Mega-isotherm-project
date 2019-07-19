import json
from urllib.request import urlopen

# get list of isotherms for searching
item1 = json.load(urlopen("https://adsorbents.nist.gov/isodb/api/isotherms.json"))

# list of good files
file_list = []

# list of data pts
data = []

# for each isotherm
for x in item1:
  # if adsorbate is N2 and adsorbent is CuBTC, add it to list
  if x['adsorbates'][0]['InChIKey'] == 'IJGRMHOSHXDMSA-UHFFFAOYSA-N' and x['adsorbent']['hashkey'] == 'NIST-MATDB-991daf7313251e7e607e2bab2da57e33':
    file_list.append(x['filename'])

# for each isotherm
for filename in file_list:
  #open JSON file
  file_ = json.load(urlopen(f"https://adsorbents.nist.gov/isodb/api/isotherm/{filename}.json"))
  print(filename)
  # if the units are what we want
  if file_['adsorptionUnits'] == 'cm3(STP)/g':
    #for each data pt
    for num in range(len(file_['isotherm_data'])):
      #for type in ['pressure', 'total_adsorption']:
        #print(f"{type}: {file_['isotherm_data'][num][type]}")
      # add data pt to list
      data.append((file_['isotherm_data'][num]['pressure'], file_['isotherm_data'][num]['species_data'][0]['adsorption']))
      print((file_['isotherm_data'][num]['pressure'], file_['isotherm_data'][num]['species_data'][0]['adsorption']))
