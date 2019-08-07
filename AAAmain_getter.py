
import pyiast
import pandas as pd
import os
import json
from urllib.request import urlopen
from sys import exit
import csv
'''
# get list of adsorbents
adsorbent_json = json.load(urlopen("https://adsorbents.nist.gov/matdb/api/materials.json"))

# get list of adsorbates
adsorbate_json = json.load(urlopen("https://adsorbents.nist.gov/isodb/api/gases.json"))


# get list of isotherms for searching
item1 = json.load(urlopen("https://adsorbents.nist.gov/isodb/api/isotherms.json"))



for adsorbent in ['MOF-5']:
    #'CuBTC', 'Zeolite 13X', 'MOF-1', 'UiO-66', 'Activated Carbon'
    for adsorbate1 in ['N2', 'CO2', 'CH4', 'Ar', 'H2', 'H2O']:
        #'',
        for adsorbate2 in ['']:
            #, 'N2', 'CO2', 'CH4', 'Ar', 'H2', 'H2O'
            for temperature in [77, 298, 303, 308]:
                for ads_unit in ['mmol/g', 'mg/g', 'cm3(STP)/g']:

                    # list of good files
                    file_list = []

                    # list of data pts
                    data = []

                    # find hashkey for adsorbent
                    #adsorbent_hashkey = None
                    #while adsorbent_hashkey == None:

                      #adsorbent = input("adsorbent >> ")

                    for x in adsorbent_json:
                        if x['name'] == adsorbent or adsorbent in x['synonyms']:
                          adsorbent_hashkey = x['hashkey']
                          break

                      #if adsorbent_hashkey == None:
                        #print("adsorbent not found")

                    num_adsorbate = 1 if (adsorbate1 == '' or adsorbate2 == '') else 2
                    #while num_adsorbate == None:
                     # try:
                    #    num_adsorbate = int(input("How many adsorbates? >> "))
                     # except ValueError:
                    #    print("please input a valid integer")

                    adsorbate_InChIKey_list = []
                    adsorbate_list = []

                    # find InChIKey for adsorbate
                    #for n in range(num_adsorbate):
                      #adsorbate_InChIKey = None
                      #while adsorbate_InChIKey == None:

                        #adsorbate = input("adsorbate >> ")
                    if adsorbate1 != '':
                        for x in adsorbate_json:
                          if x['name'] == adsorbate1 or adsorbate1 in x['synonyms']:
                            adsorbate_InChIKey_list.append(x['InChIKey'])
                            adsorbate_list.append(adsorbate1)
                            #adsorbate_InChIKey =
                            break

                    if adsorbate2 != '' and not adsorbate1 == adsorbate2:
                        for x in adsorbate_json:
                          if x['name'] == adsorbate2 or adsorbate2 in x['synonyms']:
                            adsorbate_InChIKey_list.append(x['InChIKey'])
                            adsorbate_list.append(adsorbate2)
                            #adsorbate_InChIKey = 1
                            break


                        #if adsorbate_InChIKey == None:
                          #print("adsorbate not found")

                    #temperature = None
                    #while temperature == None:

                      #temperature = input("temp >> ")

                      #try:
                        #temperature = int(temperature)
                        #break
                      #except ValueError:
                        #print("please input a valid integer")

                    #ads_unit = input("adsorption units >> ")

                    # for each isotherm
                    for x in item1:
                      count = 0
                      for key in adsorbate_InChIKey_list:
                        # if adsorbate is N2 and adsorbent is CuBTC, add it to list
                        if {"InChIKey": f"{key}"} in x['adsorbates'] and x['adsorbent']['hashkey'] == f'{adsorbent_hashkey}' and len(x['adsorbates']) == num_adsorbate and x['temperature'] == temperature:
                          count += 1
                      if count == num_adsorbate and x['filename'] not in file_list:
                        file_list.append(x['filename'])

                    # for each isotherm
                    done_files = []
                    for filename in file_list:
                      #open JSON file
                      file_ = json.load(urlopen(f"https://adsorbents.nist.gov/isodb/api/isotherm/{filename}.json"))
                      print(filename)
                      # if the units are what we want
                      if file_['adsorptionUnits'] == ads_unit and filename not in done_files:
                        done_files.append(filename)
                        for l in range(num_adsorbate):
                          #for each data pt
                          for num in range(len(file_['isotherm_data'])):
                            #for type in ['pressure', 'total_adsorption']:
                              #print(f"{type}: {file_['isotherm_data'][num][type]}")
                            # add data pt to list
                            data.append((file_['isotherm_data'][num]['pressure'], file_['isotherm_data'][num]['species_data'][l]['composition'], file_['isotherm_data'][num]['species_data'][l]['adsorption'], adsorbate_list[l], filename))
                            print((file_['isotherm_data'][num]['pressure'], file_['isotherm_data'][num]['species_data'][l]['adsorption'], adsorbate_list[l]))

                    adsorbate_str = ' '.join(adsorbate_list)

                    with open(((adsorbate_str + ' ' + adsorbent + ' ' + str(temperature) + ' ' + ads_unit.replace('/', ' per ') + ".csv") if len(data) != 0 else ('ZZZEMPTY' + adsorbate_str + ' ' +adsorbent + ' ' + str(temperature) + ' ' + ads_unit.replace('/', ' per ') + ".csv")), 'w+') as out:
                        fieldnames = ['pressure', 'composition', 'Q', 'species', 'filename']
                        writer = csv.DictWriter(out, fieldnames=fieldnames)

                        writer.writeheader()

                        for datapoint in data:
                            writer.writerow({'pressure': datapoint[0], 'composition': datapoint[1], 'Q': datapoint[2], 'species': datapoint[3], 'filename': datapoint[4]})

                        out.close()
'''

list_params = []
list_rmse = []
filenames = []

for filename in os.listdir('/users/noahwhelpley/python/NIST_isotherm_project/graph_getting/dump'):
    if filename.endswith(".csv"):



        df_isotherm = pd.read_csv(filename)


        min = None
        good_guess = {'K':1, 'M':1}

        for K in [300, 350, 400, 450, 500]:
            for M in ['-inf', 'inf', 1, 2, 3, 4, 5, 6]:
                try:
                    print(f"{K}, {M}")
                    isotherm = pyiast.ModelIsotherm(df_isotherm, loading_key="Q"  ,pressure_key = "pressure" , model = "BET", param_guess={'K': K, 'M':M})

                    if isotherm.rmse < min or min == None:
                        good_guess['K'], good_guess['M'] = K, M


                except:
                    pass
        try:
            print("\n\nattempt\n\n")
            isotherm = pyiast.ModelIsotherm(df_isotherm, loading_key="Q"  ,pressure_key = "pressure" , model = "BET", param_guess={'K':good_guess['K'], 'M':good_guess['M']})
            print("\n\nsuccess\n\n")
            isotherm.print_params()
            if isotherm.rmse < 25:
                print(f"\n\n\n\n##################\n\n{filename}\n\n##################\n\n\n\n")
                pyiast.plot_isotherm(isotherm)
            list_params.append(isotherm.params)
            list_rmse.append(isotherm.rmse)
            filenames.append(filename)

        except:
            pass
    else:
        pass

'''
with open('/users/noahwhelpley/python/NIST_isotherm_project/graph_getting/results/results.csv', 'w+') as results:
    results.write('langmuir_parameters, rmse, filename\n')
    for index in range(len(list_params)):
        results.write(f"{list_params[index]}, {list_rmse[index]}, {filenames[index]}\n")
    results.close()

'''
print(pyiast._MODELS)
