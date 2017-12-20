# This Python file uses the following encoding: utf-8

from Tkinter import *
from threading import Thread
from time import sleep
from tkFileDialog   import askopenfilename
import pandas as pd
import numpy as np

#----------------------------------Variablen---------------------------------------------------------------------

'''
To Do:

- Alle Methoden müssen noch einen Dokumentations-string bekommen
- Leistungspreis einlesen aus Excel
-  einlesenAusgeben und berechnen verschlanken (auslagern)

'''

#----------------------------------Berechnung--------------------------------------------------------------------

# berechnet die Ersparnis in cent!

def berechnung(pvCap, data):

    ersparnis = 0 # Einsparungen, die pro Jahr durch die Solaranlage erreicht werden

    '''muss noch aus excfel eingelesen werden data.iat[1,5]'''

    leistungspreis =  5.5 # Leistungspreis in €/kW

    maxNachfrage = 0

    j = 0  # Zählvariable für while-schleife

    while (j < data.__len__()):
        vergleichsWert = data["Lastgang_[W]"][j] - pvCap * data["PV usage [0:1]"][j]
        if vergleichsWert > maxNachfrage:
            maxNachfrage = vergleichsWert
        j += 1

    if maxNachfrage < data["Lastgang_[W]"].max():
        leistungspreisErsparnis = (data["Lastgang_[W]"].max() - maxNachfrage)/1000* leistungspreis # in kW umgerechnet und dann mit Leistungspreis multipliziert
        ersparnis = leistungspreisErsparnis
    else:
        leistungspreisErsparnis = 0

    i = 0  # Zählvariable für while-schleife

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
        i += 1

    return (ersparnis, leistungspreisErsparnis)



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

    loeschenText() # löscht die Daten im Textfeld der GUI

    try:
        data = pd.read_csv(eingabeDatei.get(), sep=";")  # Daten werden aus CSV eingelesen

    except:
        ausgabeText("Der Dateipfad ist nicht korrekt\n")
        return

    ausgabeText("Übersicht der eingegebenen Daten:\n\n")
    ausgabeText(data.describe())  # statistische Auswertung zu den Eingelesenen Daten wird angezeigt
    ausgabeText("\n\n")


    try:

        investKosten = float(einlesenKosten())# [€/kWp] investitionskosten pro kWp

        dachFlaeche = int(einlesenFlaeche())# [m²] Dachfläche in Quadratmetern

        normLeistung = float(einlesenLeistung())# [W/m²] Normleistung eines Quadratmeters Solaranlage

        pvCap = (dachFlaeche*normLeistung) # [m²*W/m²] = [W] PV Kapazität in Kilowatt

        gesamtInvest = investKosten*(pvCap/1000)  # [€/kWp*kWp] = [€] Gesamtinvestition in €

        ausgabeText("Kapazität der PV-Anlage: " + str((pvCap))+" Wp")
        ausgabeText("\n\n")
        ausgabeText("Berechnung... \n")

        ersparnis, leistungsErsparnis = berechnung(pvCap, data)


    except:
        ausgabeText("Zur Berechnung fehlen Werte für die PV-Anlage in der Eingabe\n")
        return


    gesamtErsparnis = ersparnis + leistungsErsparnis

    ausgabeText("\nDie Leistungsersparnis beträgt: " + str(leistungsErsparnis) + "€\n\n")

    ausgabeText("\nDie gesamte jährliche Ersparnis beträgt: " + str(round(gesamtErsparnis / 100, 2)) + "€\n\n")

    ausgabeText("Die Amortisationszeit beträgt: " + str(round(amortisation(gesamtErsparnis, gesamtInvest), 2)) + " Jahre \n")

    ausgabeText("\nAlternativen:\n")

    textErgebnis.see("end")


    # weitere Flächengrössen berechnen
    spaces = [dachFlaeche - 3, dachFlaeche - 2, dachFlaeche - 1, dachFlaeche + 1, dachFlaeche + 2,dachFlaeche + 3] # hier noch die Fälle einbauen falls die installierte Fläche kleiner als 4 m² ist!
    faktor = [1.5,1.3,1.1,0.9,0.7,0.5] #faktor, den ich bei den Investitionskosten spare, wenn ich mehr oder weniger Fläche installiere


    for xRoofspace in spaces:

        ersparnis, leistungsErsparnis = berechnung(xRoofspace*normLeistung, data)

        gesamtErsparnis = ersparnis + leistungsErsparnis

        gesamtInvest = investKosten*faktor[spaces.index(xRoofspace)]*(xRoofspace*normLeistung)/1000 # neue totale Investitionskosten berechnen

        ausgabeText("\nDie jährliche Ersparnis mit " + str(xRoofspace) + " m² installierter Fläche beträgt: "+ str(round(gesamtErsparnis / 100, 2)) + "€\n\n")

        ausgabeText("\nDie Leistungsersparnis beträgt: " + str(leistungsErsparnis) + "€\n\n")

        ausgabeText("Die Amortisationszeit beträgt dann: " + str(round(amortisation(gesamtErsparnis, gesamtInvest), 2)) + " Jahre\n")

        endeAnzeigen()

    #-------------------Plotten der Kurven---------------------------

    try:
        plot(data)
    except:
        print("Kein Plot möglich")

    return



#------------------------------------GUI (Darstellung)---------------------------------------------------------


#-----------------Lesen/schreiben GUI----------

'''Hier muss die gesamte ein und ausgabe der GUI hin, welche jetzt noch mit der berechnung verknüpft ist - bsp aufruf von ein- und ausgabe-Methoden'''


#------einlesen---------

def einlesenKosten():
    return eingabeKosten.get()

def einlesenFlaeche():
    return eingabeFlaeche.get()

def einlesenLeistung():
    return eingabeLeistung.get()

#-----ausgeben-----------

def ausgabeText(string): #gibt Text im Textfeld aus
    textErgebnis.insert(END, string)
    return

def loeschenText(): #löscht den Text im Textfeld
    textErgebnis.delete("1.0", END)
    return

def endeAnzeigen(): #scrollt zum Ende des Textfeldes
    textErgebnis.see("end")
    return

#-----------------Funktionen GUI-Menü---------

def save():
    return

def schliessen(event=None):
    root.destroy()
    return


def new(event=None):
    textErgebnis.delete("1.0",END)
    eingabeDatei.delete(0, END)
    eingabeFlaeche.delete(0, END)
    eingabeLeistung.delete(0, END)
    eingabeKosten.delete(0, END)
    return

def open(event=None):
    path = askopenfilename()
    eingabeDatei.insert(END, path)
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
eingabeDatei = Entry(frameLinks, width = 20)

labelSolaranlage= Label(frameLinks, text ="Daten Solaranlage:")

labelFlaeche= Label(frameLinks, text="Fläche [m²]")
eingabeFlaeche = Entry(frameLinks, width = 20)

labelLeistung= Label(frameLinks, text="Normalleistung [W/m²]")
eingabeLeistung = Entry(frameLinks, width = 20)

labelKosten= Label(frameLinks, text="Investition [€/kWp]")
eingabeKosten = Entry(frameLinks, width = 20)


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
eingabeDatei.pack()

emptyLabel2.pack()

labelSolaranlage.pack()

emptyLabel3.pack()

labelFlaeche.pack()
eingabeFlaeche.pack()

labelLeistung.pack()
eingabeLeistung.pack()

labelKosten.pack()
eingabeKosten.pack()

emptyLabel4.pack()

buttonBerechnen.pack(side=BOTTOM)


textErgebnis.pack()

root.mainloop()