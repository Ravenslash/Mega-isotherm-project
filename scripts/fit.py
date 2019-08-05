import pyiast
import pandas as pd

# replace path with csv containing isotherm data
df_isotherm = pd.read_csv("/users/noahwhelpley/Downloads/Book2.csv")

isotherm = pyiast.ModelIsotherm(df_isotherm, loading_key="Q"  ,pressure_key = "pressure" , model = "Langmuir")

isotherm.print_params()

pyiast.plot_isotherm(isotherm)
