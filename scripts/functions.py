import json
from urllib.request import urlopen
from sys import exit

################################################################
### various useful functions to be imported to other scripts ###
################################################################

def get_adsorbent(adsorbent_json):

    adsorbent = input("adsorbent >> ")

    # find hashkey for adsorbent
    adsorbent_hashkey = None
    for x in adsorbent_json:
      if x['name'] == adsorbent or adsorbent in x['synonyms']:
        adsorbent_hashkey = x['hashkey']
        break

    if adsorbent_hashkey == None:
      exit("adsorbent not found")

    return adsorbent_hashkey

def get_adsorbate(adsorbate_json):

    adsorbate = input("adsorbate >> ")

    # find InChIKey for adsorbate
    adsorbate_InChIKey = None
    for x in adsorbate_json:
      if x['name'] == adsorbate or adsorbate in x['synonyms']:
        adsorbate_InChIKey = x['InChIKey']
        break

    if adsorbate_InChIKey == None:
      exit("adsorbate not found")

    return adsorbate_InChIKey

def get_isotherms(adsorbent, adsorbate, item1):
    file_list = []
    for x in item1:
      # if adsorbate is N2 and adsorbent is CuBTC, add it to list
      if x['adsorbates'][0]['InChIKey'] == f'{adsorbate_InChIKey}' and x['adsorbent']['hashkey'] == f'{adsorbent_hashkey}':
        file_list.append(x['filename'])

    return file_list

def get_data(file_list, ads_unit):
    data = []
    # for each isotherm
    for filename in file_list:
      #open JSON file
      file_ = json.load(urlopen(f"https://adsorbents.nist.gov/isodb/api/isotherm/{filename}.json"))
      print(filename)
      # if the units are what we want
      if file_['adsorptionUnits'] == ads_unit:
        #for each data pt
        for num in range(len(file_['isotherm_data'])):
          #for type in ['pressure', 'total_adsorption']:
            #print(f"{type}: {file_['isotherm_data'][num][type]}")
          # add data pt to list
          data.append((file_['isotherm_data'][num]['pressure'], file_['isotherm_data'][num]['species_data'][0]['adsorption']))
          print((file_['isotherm_data'][num]['pressure'], file_['isotherm_data'][num]['species_data'][0]['adsorption']))
    return data
