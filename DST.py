# This Python file uses the following encoding: utf-8

from Tkinter import *
import matplotlib as mpl
import numpy as np
import pandas as pd


# ------------------------------------------Variablendeklaration-----------------------------------------------------------

'''
pvUtil = data.iat[0,1]# prozentualer Anteil des maximal erzeugbaren PV Stroms der in der betreffenden Stunde erzeugt wird
savings = 0 # Einsparungen, die pro Jahr durch die Solaranlage erreicht werden
load = data.iat[0,4]# Lastgang in der betreffenden Stunde
costNet = data.iat[0,2]# Stromkosten Netz in der betreffenden Stunde
revPV = data.iat[0,3]# Einspeisevergütung in der betreffenden Stunde
'''

#----------------------------------------------------------GUI-----------------------------------------------------

#----------------Funktionalität GUI------------

def berechnenErsparnis():

    # roof = # Dachfläche in Quadratmetern

    # normPower = # Normleistung eines Quadratmeters Solaranlage

    pvCap = 4800# PV Kapazität in Watt, soll nachher auch eingelesen werden

    data = pd.read_csv(entryInput.get(), sep=";")  # Daten werden aus CSV eingelesen

    textErgebnis.insert(END, data.describe())  # statistische Auswertung zu den Eingelesenen Daten wird angezeigt
    textErgebnis.insert(END, "\n\n")

    i=0
    savings = 0
    while(i<data.__len__()):


        if (((data.iat[i,1])*pvCap)>(data.iat[i,4])): # falls mehr Solarstrom produziet wird, als Last anfällt, speise Strom ein, erhalte Entgelt
            textErgebnis.insert(END,"Überkapazität zum Zeitpunkt " + str(data.iat[i,0]) + "\n")
            savings = savings + (((data.iat[i,1])*pvCap)/1000)-((data.iat[i,4])*data.iat[0,3]/1000) # die savings werden um die Einspeisevergütung erhöht

        else:
            savings = savings + ((data.iat[i,4]/1000*data.iat[i,2]/100)-((data.iat[i,4]/1000)-(data.iat[i,1])*pvCap)/1000*data.iat[0,2]/100) # print durch textErgebnis.insert(), END auswechseln
            #                (Lastgang [W] * Stromkosten [cent/KWh]/100)- (Lastgang [W]- PV Auslastung * PV Kapazität [W])* Stromkosten [cent/KWh]/100)
            #                (                  in Euro                                                                         in Euro
        i=i+1

    textErgebnis.insert(END, "\nDie jährliche Ersparnis beträgt: " + str(round(savings/1000, 2)) + "€")

    #-------------------Plotten der Kurven---------------------------
    '''
    x = np.linspace(0, 35039,35039)

    plot = data.plot(data[x, "PV usage [0:1]"], kind = "line")
    plt.show()
    '''


    return


def leer():
    return

def schliessen(event=None):
    root.destroy()
    return

#-------------Hauptfenster initialisieren------

root = Tk()
root.title("Decision Support Tool")

#-------------Widgets erstellen----------------
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

frameRechts =Frame(root, width=500, height=100)
frameLinks =Frame(root, width=500, height=100)

labelDateneingabe= Label(frameLinks, text ="Dateneingabe")

labelInput= Label(frameLinks, text = "Name der Input-Datei")
entryInput = Entry(frameLinks, width = 20)

labelFlaeche= Label(frameLinks, text="Fläche der Solaranlage")
entryFlaeche = Entry(frameLinks, width = 20)

buttonBerechnen = Button(frameLinks,text= "Berechnen", command=berechnenErsparnis)

textErgebnis = Text(frameRechts, width = 90, height =20, yscrollcommand=scrollbar.set)

scrollbar.config(command=textErgebnis.yview)

emptyLabel1 = Label(frameLinks, text="")
emptyLabel2 = Label(frameLinks, text="")

#-------------Events---------------------------

root.bind("<Alt-q>", schliessen)

#-------------Menuleiste definieren------------

mLeiste = Menu(root)
root.config(menu=mLeiste)

#-------------Untermenü Datei------------------

dateiMenu = Menu(mLeiste)
mLeiste.add_cascade(label="Datei", menu= dateiMenu)
dateiMenu.add_command(label="Neu", command= leer)
dateiMenu.add_command(label="Öffnen", command= leer)
dateiMenu.add_command(label="Speichern", command= leer)
dateiMenu.add_command(label="Schliessen", command= schliessen, accelerator= "alt + q")

#-------------Untermenu Edit-------------------

editMenu = Menu(mLeiste)
mLeiste.add_cascade(label="Edit", menu= editMenu)
editMenu.add_command(label="Rückgängig", command= leer)
editMenu.add_command(label="Wiederholen", command= leer)

#-------------Widgets platzieren---------------

frameRechts.pack(side = RIGHT)
frameLinks.pack(side = LEFT)

labelInput.pack()
entryInput.pack()

emptyLabel1.pack()

labelFlaeche.pack()
entryFlaeche.pack()

emptyLabel2.pack()

buttonBerechnen.pack(side=BOTTOM)

textErgebnis.pack()

root.mainloop()