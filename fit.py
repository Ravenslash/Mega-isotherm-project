import pyiast
import pandas as pd


df_isotherm = pd.read_csv("/users/noahwhelpley/Downloads/Book2.csv")

isotherm = pyiast.ModelIsotherm(df_isotherm, loading_key="Q"  ,pressure_key = "pressure" , model = "Langmuir")

isotherm.print_params()

pyiast.plot_isotherm(isotherm)
