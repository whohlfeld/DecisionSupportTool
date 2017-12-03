import pandas as pd

import numpy as np

import matplotlib.pyplot as plt



data = pd.read_csv("Inputs_WHO.csv", sep=";")
#print(type(data))
#print(data.shape)
#print(data.head())
#print(data.columns)
#print(data["Timestamp"].head)
#print(data[["Timestamp", "PV usage [0:1]"]].head) #oberste Zeilen von Spalten Timestamp und PV usage
#print(data.loc[0, ["Timestamp"]]) #erste Zeile ausgeben
#data.describe()
#data["PV usage [0:1]"].plot()

print(data.iat[1,1])