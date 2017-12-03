# This Python file uses the following encoding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# -------------------------------------------Einlesen der CSV---------------------------------------------------------------

data = pd.read_csv("Inputs_WHO.csv", sep=";") # Name durch entryInput.get() auswechseln

print(data.describe()) # statistische Auswertung zu den Eingelesenen Daten wird angezeigt


# ------------------------------------------Variablendeklaration-----------------------------------------------------------

pvCap = 4800 # PV Kapazität in Watt, soll nachher auch eingelesen werden
pvUtil = data.iat[0,1]# prozentualer Anteil des maximal erzeugbaren PV Stroms der in der betreffenden Stunde erzeugt wird
savings = 0 # Einsparungen, die pro Jahr durch die Solaranlage erreicht werden
load = data.iat[0,4]# Lastgang in der betreffenden Stunde
costNet = data.iat[0,2]# Stromkosten Netz in der betreffenden Stunde
revPV = data.iat[0,3]# Einspeisevergütung in der betreffenden Stunde


#----------------------------------------------------------GUI-----------------------------------------------------

#----------------Funktionalität GUI------------

def berechnenErsparnis():

    print("Es sind " + str(data.__len__()) + " Werte vorhanden.")
    i=0
    savings = 0
    while(i<data.__len__()):


        if (((data.iat[i,1])*pvCap)>(data.iat[i,4])): # falls mehr Solarstrom produziet wird, als Last anfällt, speise Strom ein, erhalte Entgelt
            print("Überkapazität zum Zeitpunkt " + str(data.iat[i,0]))
            savings = savings + (((data.iat[i,1])*pvCap)/1000)-((data.iat[i,4])*data.iat[0,3]/1000) # die savings werden um die Einspeisevergütung erhöht

        else:
            savings = savings + ((data.iat[i,4]/1000*data.iat[i,2]/100)-((data.iat[i,4]/1000)-(data.iat[i,1])*pvCap)/1000*data.iat[0,2]/100) # print durch textErgebnis.insert(), END auswechseln
            #                (Lastgang [W] * Stromkosten [cent/KWh]/100)- (Lastgang [W]- PV Auslastung * PV Kapazität [W])* Stromkosten [cent/KWh]/100)
            #                (                  in Euro                                                                         in Euro
        i=i+1

    print("Die jährliche Ersparnis beträgt: " + str(round(savings/1000, 2)) + "€")

    #-------------------Plotten der Kurven---------------------------
    '''
    x = np.linspace(0, 35039,35039)

    plot = data.plot(data[x, "PV usage [0:1]"], kind = "line")
    plt.show()
    '''


    return

berechnenErsparnis()
