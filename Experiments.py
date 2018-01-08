# This Python file uses the following encoding: utf-8

from Tkinter import *
from threading import Thread
from time import sleep
from tkFileDialog   import askopenfilename
import pandas as pd
import numpy as np

#----------------------------------Variablen---------------------------------------------------------------------


investCost = 0# [€/kWp] investitionskosten pro kWp

roofSpace = 0# [m²] Dachfläche in Quadratmetern

normPower = 0 #[W/m²] Normleistung eines Quadratmeters Solaranlage

pvCap = (roofSpace*normPower) # [m²*W/m²] = [W] PV Kapazität in Kilowatt

totalInvest = investCost*(pvCap/1000)  # [€/kWp*kWp] = [€] Gesamtinvestition in €



#----------------------------------Berechnung--------------------------------------------------------------------

# berechnet die Ersparnis in cent!

def berechnung(investCost, roofSpace, normPower, pvCap, data):


    leistungspreis = 5.5 # Leistungspreis in €/kW


    i = 0  # Zählvariable für while-schleife
    ersparnis = 0  # Einsparungen, die pro Jahr durch die Solaranlage erreicht werden

    while (i < data.__len__()):

        timestamp = data.iat[i, 0]  # timestamp
        pvUtil = data.iat[i, 1]  # [-] prozentualer Anteil des maximal erzeugbaren PV Stroms der in der betreffenden Stunde erzeugt wird
        costNet = data.iat[i, 2]  # [ct/kWh] Stromkosten Netz in der betreffenden Stunde
        revPV = data.iat[i, 3]  # [ct/kWh] Einspeisevergütung in der betreffenden Stunde
        load = data.iat[i, 4]  # [W] Lastgang in der betreffenden Stunde

        if ((pvUtil * pvCap) > load):  # falls mehr Solarstrom produziet wird, als Last anfällt, speise Strom ein, erhalte Entgelt
            print("Überkapazität zum Zeitpunkt " + str(timestamp) + "\n")
            ersparnisMomUe = (((pvUtil * pvCap) - load) * revPV + load * costNet) / 4000  # Netzentgelte werden gespaart und der Nutzer bekommt Einspeisevergütung (4: 15 min; 1000: Wh)
            ersparnis = ersparnis + ersparnisMomUe  # die savings werden um die Einspeisevergütung erhöht
            print("momentane Ersparnis: (Ü)" + str(ersparnisMomUe))  # zur Überprüfung der Rechnung in der Konsole

        else:
            ersparnisMomN = ((pvUtil * pvCap) * costNet) / 4000  # die Netzentgelte, welche ich ansonsten bezahlen müsste, werden gespaart. (4: 15 min; 1000: Wh)
            ersparnis = ersparnis + ersparnisMomN

            print(timestamp + "PV-Output: " + str((pvUtil) * pvCap)) + " Lastgang: " + str(load)
            print("momentane Ersparnis: (N)" + str(ersparnisMomN))  # zur Überprüfung der Rechnung in der Konsole

        print("Gesamtersparnis: "+ str(ersparnis))  # zur Überprüfung der Rechnung in der Konsole
        i = i + 1

    return ersparnis



def amortisation(ersparnis, totalInvest): # amortisation mit Kapitalwertmethode/Rentenbarwertfaktor

    amortisationsWert = (totalInvest / (ersparnis / 100))

    return amortisationsWert


def rechenThread():
    thread = Thread(target=einlesenAusgeben, args=())
    thread.start()
    while (thread.is_alive()):
        sleep(0.5)
        textErgebnis.update()
        textErgebnis.insert(END, ".")

#----------------------------------Plotten ---------------------------------------------------------------------

def plot():
    '''
    plt = data.plot(data["Timestamp", "PV usage [0:1]"])
    plt.show()
    '''
    return

#----------------------------------Funktionalität GUI -----------------------------------------------------------

def einlesenAusgeben():

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

        investCost = float(entryCost.get())# [€/kWp] investitionskosten pro kWp

        roofSpace = int(entryFlaeche.get())# [m²] Dachfläche in Quadratmetern

        normPower = float(entryPower.get())# [W/m²] Normleistung eines Quadratmeters Solaranlage

        pvCap = (roofSpace*normPower) # [m²*W/m²] = [W] PV Kapazität in Kilowatt

        totalInvest = investCost*(pvCap/1000)  # [€/kWp*kWp] = [€] Gesamtinvestition in €

        textErgebnis.insert(END, "Kapazität der PV-Anlage: " + str((pvCap))+" Wp")
        textErgebnis.insert(END, "\n\n")

        textErgebnis.insert(END, "Berechnung... \n")

        ersparnis = berechnung(investCost, roofSpace, normPower, pvCap, data)

    except:
        textErgebnis.insert(END, "Zur Berechnung fehlen Werte für die PV-Anlage in der Eingabe\n")
        return


    textErgebnis.insert(END, "\nDie jährliche Ersparnis beträgt: " + str(round(ersparnis / 100, 2)) + "€\n\n")

    textErgebnis.insert(END, "Die Amortisationszeit beträgt: " + str(round(amortisation(ersparnis, totalInvest), 2)) + " Jahre \n")

    textErgebnis.insert(END, "\nAlternativen:\n")

    textErgebnis.see("end")


    # weitere Flächengrössen berechnen
    spaces = [roofSpace - 3, roofSpace - 2, roofSpace - 1, roofSpace + 1, roofSpace + 2,roofSpace + 3] # hier noch die Fälle einbauen falls die installierte Fläche kleiner als 4 m² ist!
    faktor = [1.5,1.3,1.1,0.9,0.7,0.5] #faktor, den ich bei den Investitionskosten spare, wenn ich mehr oder weniger Fläche installiere


    for xRoofspace in spaces:

        ersparnis = berechnung(investCost, xRoofspace, normPower, xRoofspace*normPower, data)

        totalInvest = investCost*faktor[spaces.index(xRoofspace)]*(xRoofspace*normPower)/1000 # neue totale Investitionskosten berechnen

        textErgebnis.insert(END, "\nDie jährliche Ersparnis mit " + str(xRoofspace) + " m² installierter Fläche beträgt: "+ str(round(ersparnis / 100, 2)) + "€\n\n")

        textErgebnis.insert(END, "Die Amortisationszeit beträgt dann: " + str(round(amortisation(ersparnis, totalInvest), 2)) + " Jahre\n")

        textErgebnis.see("end")

    #-------------------Plotten der Kurven---------------------------

    try:
        plot(data)
    except:
        print("Kein Plot möglich")

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




#----------------------------------------------------------GUI-----------------------------------------------------



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

labelCost= Label(frameLinks, text="Investition [€/kWp]")
entryCost = Entry(frameLinks, width = 20)


buttonBerechnen = Button(frameLinks,text= "Berechnen", command=rechenThread)

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