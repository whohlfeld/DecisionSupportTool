# This Python file uses the following encoding: utf-8

from Tkinter import *
from tkFileDialog   import askopenfilename
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

    textErgebnis.delete("1.0",END)

    try:
        data = pd.read_csv(entryInput.get(), sep=";")  # Daten werden aus CSV eingelesen

    except:
        textErgebnis.insert(END, "Der Dateipfad ist nicht korrekt\n")
        return

    textErgebnis.insert(END, "Übersicht der eingegebenen Daten:\n\n")
    textErgebnis.insert(END, data.describe())  # statistische Auswertung zu den Eingelesenen Daten wird angezeigt
    textErgebnis.insert(END, "\n\n")

    try:

        investCost = float(entryCost.get())# investitionskosten pro m²

        roofSpace = int(entryFlaeche.get())# Dachfläche in Quadratmetern

        normPower = float(entryPower.get())# Normleistung eines Quadratmeters Solaranlage

        pvCap = roofSpace*normPower# PV Kapazität in Watt, soll nachher auch eingelesen werden

        totalInvest = investCost*(pvCap/1000)

        textErgebnis.insert(END, "Kapazität der PV-Anlage: " + str((pvCap/1000))+" kWp")
        textErgebnis.insert(END, "\n\n")

    except:
        textErgebnis.insert(END, "Zur Berechnung fehlen Werte für die PV-Anlage in der Eingabe\n")
        return

    i=0
    savings = 0

    while(i<data.__len__()):

        if (((data.iat[i,1])*pvCap)>(data.iat[i,4])): # falls mehr Solarstrom produziet wird, als Last anfällt, speise Strom ein, erhalte Entgelt
            textErgebnis.insert(END,"Überkapazität zum Zeitpunkt " + str(data.iat[i,0]) + "\n")
            savingsMomUe = (((data.iat[i,1])*pvCap)/1000)-((data.iat[i,4])*data.iat[0,3]/1000)
            savings = savings + savingsMomUe # die savings werden um die Einspeisevergütung erhöht
            print("momentane Ersparnis: (Ü)" + str(savingsMomUe))

        else:
            savingsMomN = ((data.iat[i,4]/1000*data.iat[i,2]/100)-((data.iat[i,4]/1000)-(data.iat[i,1])*pvCap)/1000*data.iat[0,2]/100)
            #                (Lastgang [W]/1000 * Stromkosten [cent/KWh]/100)- (Lastgang [W]/1000- PV Auslastung * PV Kapazität [W]/1000)* Stromkosten [cent/KWh]/100)
            #                (           in kW                       in Euro                in kW                                   in kW                      in Euro
            savings = savings + savingsMomN

            print("momentane Ersparnis: (N)" + str(savingsMomN))

        print(savings)
        i=i+1

    textErgebnis.insert(END, "\nBerechnung Erfolgreich:\n\nDie jährliche Ersparnis beträgt: " + str(round(savings/1000, 2)) + "€\n\n")
    textErgebnis.insert(END, "Die Amorisationszeit beträgt: " + str(round((totalInvest/(savings/1000)),2)) + " Jahre")

    #-------------------Plotten der Kurven---------------------------

    '''
    plt = data.plot(data["Timestamp", "PV usage [0:1]"])
    plt.show()
    '''


    return


def save():
    return

def schliessen(event=None):
    root.destroy()
    return


def new(event=None):
    textErgebnis.delete("1.0",END)
    entryInput.delete(0,END)
    entryFlaeche.delete(0,END)
    entryPower.delete(0,END)
    entryCost.delete(0,END)
    return

def open(event=None):
    path = askopenfilename()
    entryInput.insert(END, path)
    errmsg = 'Error!'

#-------------Hauptfenster initialisieren------

root = Tk()
root.title("Decision Support Tool")

#-------------Widgets erstellen----------------
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

frameRechts =Frame(root, width=500, height=100)
frameLinks =Frame(root, width=500, height=100)

labelDateneingabe= Label(frameLinks, text ="Dateneingabe:")

labelInput= Label(frameLinks, text = "Pfad der Input-Datei")
entryInput = Entry(frameLinks, width = 20)

labelSolaranlage= Label(frameLinks, text ="Daten Solaranlage:")

labelFlaeche= Label(frameLinks, text="Fläche [m²]")
entryFlaeche = Entry(frameLinks, width = 20)

labelPower= Label(frameLinks, text="Normalleistung [W/m²]")
entryPower = Entry(frameLinks, width = 20)

labelCost= Label(frameLinks, text="Investitionskosten [€/kWp]")
entryCost = Entry(frameLinks, width = 20)


buttonBerechnen = Button(frameLinks,text= "Berechnen", command=berechnenErsparnis)

textErgebnis = Text(frameRechts, width = 80, height =20, yscrollcommand=scrollbar.set)

scrollbar.config(command=textErgebnis.yview)

emptyLabel1 = Label(frameLinks, text="")
emptyLabel2 = Label(frameLinks, text="")
emptyLabel3 = Label(frameLinks, text="")
emptyLabel4 = Label(frameLinks, text="")

#-------------Events---------------------------

root.bind("<Alt-q>", schliessen)

#-------------Menuleiste definieren------------

mLeiste = Menu(root)
root.config(menu=mLeiste)

#-------------Untermenü Datei------------------

dateiMenu = Menu(mLeiste)
mLeiste.add_cascade(label="Datei", menu= dateiMenu)
dateiMenu.add_command(label="Neu", command= new)
dateiMenu.add_command(label="Öffnen", command= open)
dateiMenu.add_command(label="Speichern", command= save)
dateiMenu.add_command(label="Schliessen", command= schliessen, accelerator= "alt + q")

#-------------Widgets platzieren---------------

frameRechts.pack(side = RIGHT)
frameLinks.pack(side = LEFT)

labelDateneingabe.pack()

emptyLabel1.pack()

labelInput.pack()
entryInput.pack()

emptyLabel2.pack()

labelSolaranlage.pack()

emptyLabel3.pack()

labelFlaeche.pack()
entryFlaeche.pack()

labelPower.pack()
entryPower.pack()

labelCost.pack()
entryCost.pack()

emptyLabel4.pack()

buttonBerechnen.pack(side=BOTTOM)

textErgebnis.pack()

root.mainloop()