import pyiast
import pandas as pd
import os
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



for adsorbent in ['CuBTC', 'Zeolite 13X', 'MOF-1', 'UiO-66', 'Activated Carbon']:
    for adsorbate1 in ['','N2', 'CO2', 'CH4', 'Ar', 'H2', 'H2O']:
        for adsorbate2 in ['', 'N2', 'CO2', 'CH4', 'Ar', 'H2', 'H2O']:
            for temperature in [77, 298, 303, 308]:
                for ads_unit in ['mmol/g', 'mg/g', 'cm3(STP)/g']:

                    # list of good files
                    file_list = []

                    # list of data pts
                    data = []

                    for x in adsorbent_json:
                        if x['name'] == adsorbent or adsorbent in x['synonyms']:
                          adsorbent_hashkey = x['hashkey']
                          break


                    num_adsorbate = 1 if (adsorbate1 == '' or adsorbate2 == '') else 2
                    

                    adsorbate_InChIKey_list = []
                    adsorbate_list = []


                    if adsorbate1 != '':
                        for x in adsorbate_json:
                          if x['name'] == adsorbate1 or adsorbate1 in x['synonyms']:
                            adsorbate_InChIKey_list.append(x['InChIKey'])
                            adsorbate_list.append(adsorbate1)
                            break

                    if adsorbate2 != '' and not adsorbate1 == adsorbate2:
                        for x in adsorbate_json:
                          if x['name'] == adsorbate2 or adsorbate2 in x['synonyms']:
                            adsorbate_InChIKey_list.append(x['InChIKey'])
                            adsorbate_list.append(adsorbate2)
                            break




                    # for each isotherm
                    for x in item1:
                      count = 0
                      for key in adsorbate_InChIKey_list:
                        # if adsorbate is right and adsorbent is right, add it to list
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
                            # add data pt to list
                            data.append((file_['isotherm_data'][num]['pressure'], file_['isotherm_data'][num]['species_data'][l]['composition'], file_['isotherm_data'][num]['species_data'][l]['adsorption'], adsorbate_list[l], filename))
                            print((file_['isotherm_data'][num]['pressure'], file_['isotherm_data'][num]['species_data'][l]['adsorption'], adsorbate_list[l]))
                    
                    # make string of adsorbate names
                    adsorbate_str = ' '.join(adsorbate_list)
                    
                    # make file systematically named for combination of metadata, but if there's no data, add 'ZZZEMPTY' to name so it gets sorted to the end alphabetically
                    with open(((adsorbate_str + ' ' + adsorbent + ' ' + str(temperature) + ' ' + ads_unit.replace('/', ' per ') + ".csv") if len(data) != 0 else ('ZZZEMPTY' + adsorbate_str + ' ' +adsorbent + ' ' + str(temperature) + ' ' + ads_unit.replace('/', ' per ') + ".csv")), 'w+') as out:
                        # prepare to write to csv
                        fieldnames = ['pressure', 'composition', 'Q', 'species', 'filename']
                        writer = csv.DictWriter(out, fieldnames=fieldnames)

                        writer.writeheader()
                        
                        # write datapoints to csv
                        for datapoint in data:
                            writer.writerow({'pressure': datapoint[0], 'composition': datapoint[1], 'Q': datapoint[2], 'species': datapoint[3], 'filename': datapoint[4]})

                        out.close()

# creating lists
list_params = []
list_rmse = []
filenames = []

# for each output csv (replace path with path you output to in previous block)
for filename in os.listdir('/users/noahwhelpley/python/NIST_isotherm_project/single_fitting/trial2'):
    if filename.endswith(".csv"):
        
        df_isotherm = pd.read_csv(filename)

        # set defaults for optimization algorithm guesses
        min = None
        good_guess = {'K':1, 'M':1}
        
        # run through set of starting guesses for the optimization algorithm
        for K in [300, 350, 400, 450, 500]:
            for M in ['-inf', 'inf', 1, 2, 3, 4, 5, 6]:
                # this is in try block because pyiast throws an exception if its optimization takes too long
                # (also a large reason why many satrting guesses are tried
                try:
                    # print guesses
                    print(f"{K}, {M}")
                    # create model
                    isotherm = pyiast.ModelIsotherm(df_isotherm, loading_key="Q"  ,pressure_key = "pressure" , model = "Langmuir", param_guess={'K': K, 'M':M})
                    
                    # if it's the best model, use those parameter guesses
                    if isotherm.rmse < min or min == None:
                        good_guess['K'], good_guess['M'] = K, M

                except:
                    pass
        # in try block for same reason
        # (if no good guesses are found and it still fails)
        try:
            print("\n\nattempt\n\n")
            isotherm = pyiast.ModelIsotherm(df_isotherm, loading_key="Q"  ,pressure_key = "pressure" , model = "Langmuir", param_guess={'K':good_guess['K'], 'M':good_guess['M']})
            # if no exception is thrown, prints "success"
            print("\n\nsuccess\n\n")
            isotherm.print_params()
            # change 25 to any threshold desired
            if isotherm.rmse < 25:
                print(f"\n\n\n\n##################\n\n{filename}\n\n##################\n\n\n\n")
                # uncomment if you wish to see the plots, but program halts until graph is exited
                #pyiast.plot_isotherm(isotherm)
            list_params.append(isotherm.params)
            list_rmse.append(isotherm.rmse)
            filenames.append(filename)

        except:
            pass
    else:
        pass

# writes lists obtained to new csv
with open('/users/noahwhelpley/python/NIST_isotherm_project/single_fitting/AAAtrial2/results.csv', 'w+') as results:
    results.write('langmuir_parameters, rmse, filename\n')
    for index in range(len(list_params)):
        results.write(f"{list_params[index]}, {list_rmse[index]}, {filenames[index]}\n")
    results.close()

# prints model types available in pyIAST
# look at pyIAST documentation for parameters for each type to modify the starting guess iterators if you change model type
#print(pyiast._MODELS)
