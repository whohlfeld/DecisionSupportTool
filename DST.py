# This Python file uses the following encoding: utf-8

from Tkinter import *
from threading import Thread
from time import sleep
from tkFileDialog import askopenfilename
import pandas as pd
import matplotlib.pyplot as pt

#----------------------------------Variablen---------------------------------------------------------------------

'''
To Do:

- Alle Methoden müssen noch einen Dokumentations-string bekommen
- Leistungspreis: Demodaten wo einer anfallen würde - was ist ein sinnvoller Leistungspreis? Kroener zitieren
- Faktoren bei verschiedenen Flächen - macht das Sinn? - Installationskosten?? https://www.rechnerphotovoltaik.de/
- Ausarbeitung der Ergebnisse - Gebäude vergleichen? Reichen 2-3 Beispiele (PV-Anlagen unterschiedlich!)

'''

#----------------------------------Berechnung--------------------------------------------------------------------

# berechnet die Ersparnis in cent!

def berechnung(pvCap, data):

    ersparnis, leistungsPreisErsparnis = berechnungLeistungsPreisErsparnis(pvCap, data) # in €

    i = 0  # Zählvariable für while-schleife

    while (i < data.__len__()):

        timestamp = data.iat[i, 0]  # timestamp
        pvUtil = float(data.iat[i, 1])  # [-] prozentualer Anteil des maximal erzeugbaren PV Stroms der in der betreffenden Stunde erzeugt wird
        costNet = float(data.iat[i, 2])/100  # [€/kWh] Stromkosten Netz in der betreffenden Stunde
        revPV = float(data.iat[i, 3])/100  # [€/kWh] Einspeisevergütung in der betreffenden Stunde
        load = float(data.iat[i, 4])  # [kW] Lastgang in der betreffenden Stunde

        if ((pvUtil * pvCap) > load):  # falls mehr Solarstrom produziert wird, als Last anfällt, speise Strom ein, erhalte Entgelt
            ersparnisMomUe = (((pvUtil * pvCap) - load) * revPV + load * costNet) / 4 # in € - Netzentgelte werden gespart und der Nutzer bekommt Einspeisevergütung (durch 4: 15 min)
            ersparnis = ersparnis + ersparnisMomUe  # die savings werden um die Einspeisevergütung erhöht
            print(timestamp + " PV-Output: " + str(pvUtil * pvCap) + "kW,  Lastgang: " + str(load) + "kW"
            ", momentane Ersparnis: (Ü)" + str(ersparnisMomUe) + "€")  # zur Überprüfung der Rechnung in der Konsole

        else:
            ersparnisMomN = ((pvUtil * pvCap) * costNet) / 4 # in € - Netzentgelte, welche ich ansonsten bezahlen müsste, werden gespaart. (durch 4: 15 min)
            ersparnis = ersparnis + ersparnisMomN

            print(timestamp + " PV-Output: " + str(pvUtil * pvCap) + "kW,  Lastgang: " + str(load) + "kW"
            ", momentane Ersparnis: (N)" + str(ersparnisMomN) + "€")  # zur Überprüfung der Rechnung in der Konsole

        print("Gesamtersparnis: "+ str(ersparnis) + "€")  # zur Überprüfung der Rechnung in der Konsole
        i += 1

    return (ersparnis, leistungsPreisErsparnis)



def berechnungLeistungsPreisErsparnis(pvCap, data): # wenn durch PV die Leistungsspitze gekappt wird, dann spart man, falls nicht , dann nicht

    ersparnis = 0 # Einsparungen, die pro Jahr durch die Solaranlage erreicht werden

    leistungsPreis = float(data.iat[0,5]) # Leistungspreis in €/kW aus Excel

    maxNachfrage = 0

    j = 0  # Zählvariable für while-schleife

    while (j < data.__len__()): # Ermittlung der maximalen Stromnachfrage unter Berücksichtigung der PV Nutzung
        restNachfrage = data["Lastgang_[W]"][j] - pvCap * data["PV usage [0:1]"][j]
        if restNachfrage > maxNachfrage:
            maxNachfrage = restNachfrage # in kW
        j += 1

    if maxNachfrage < data["Lastgang_[W]"].max(): # falls sich die Lastspitze durch die PV Nutzung verringert hat - Einsparung
        leistungsPreisErsparnis = (data["Lastgang_[W]"].max() - maxNachfrage) * leistungsPreis # in kW umgerechnet und dann mit Leistungspreis multipliziert
        ersparnis = leistungsPreisErsparnis
    else:
        leistungsPreisErsparnis = 0


    return ersparnis, leistungsPreisErsparnis


def amortisation(gesamtErsparnis, gesamtInvest, betriebsKosten): # amortisation mit Kapitalwertmethode/Rentenbarwertfaktor

    r = 0.05 # zinssatz am Kapitalmarkt
    einnahmen = 0
    amortisationsJahre = 0

    while (gesamtInvest>einnahmen):
        gesamtInvest = gesamtInvest + betriebsKosten
        einnahmen = einnahmen + ((gesamtErsparnis-betriebsKosten)/((1+r)**amortisationsJahre))
        amortisationsJahre = amortisationsJahre + 1

    # amortisationsJahre = (gesamtInvest / gesamtErsparnis)

    return amortisationsJahre


def rechenThread():
    thread = Thread(target=einlesenAusgeben, args=())
    thread.start()
    endeAnzeigen()
    while (thread.is_alive()):
        sleep(0.5)
        textErgebnis.update()
        textErgebnis.insert(END, ".")
    return

def uebersicht():
    loeschenText()  # löscht die Daten im Textfeld der GUI

    try:
        data = pd.read_csv(eingabeDatei.get(), sep=";")  # Daten werden aus CSV eingelesen

    except:
        ausgabeText("Der Dateipfad ist nicht korrekt")
        return

    ausgabeText("Übersicht der eingegebenen Daten:\n\n")
    ausgabeText(data.describe())  # statistische Auswertung zu den Eingelesenen Daten wird angezeigt
    ausgabeText("\n\n")

    investKostenPanels = float(einlesenKostenPanels())  # [€/m²] investitionskosten pro kWp

    investKostenAufbau = float(einlesenKostenAufbau())  # [€] Investitionskosten Aufbau System

    betriebsKosten = float(einlesenKostenBetrieb()) # [€] jährliche Betriebskosten des Systems

    panelFlaeche = int(einlesenFlaeche())  # [m²] Dachfläche in Quadratmetern

    normLeistung = float(einlesenLeistung()) / 1000  # [kW/m²] Normleistung eines Quadratmeters Solaranlage

    pvCap = (panelFlaeche * normLeistung)  # [m²*kW/m²] = [kW] PV Kapazität in Kilowatt

    gesamtInvest = investKostenAufbau + investKostenPanels * panelFlaeche  # [€/m²*m²] = [€] Gesamtinvestition in €

    ausgabeText("Kapazität der PV-Anlage: " + str(pvCap) + "kW\n\n")

    ausgabeText("Gesamtinvestition: " + str(gesamtInvest) + "€\n\n")

    return

#----------------------------------Plotten ---------------------------------------------------------------------

def plot(data):

    #pt.plot(data["Count"], data["PV usage [0:1]"])
    #pt.show()

    return


#----------------------------------Funktionalität ----------------------------------------------------------

def einlesenAusgeben():

    loeschenText() # löscht die Daten im Textfeld der GUI

    try:
        data = pd.read_csv(eingabeDatei.get(), sep=";")  # Daten werden aus CSV eingelesen

    except:
        ausgabeText("Der Dateipfad ist nicht korrekt")
        return


    try:

        investKostenPanels = float(einlesenKostenPanels())# [€/m²] investitionskosten pro kWp

        investKostenAufbau = float(einlesenKostenAufbau()) # [€] Investitionskosten Aufbau System

        betriebsKosten = float(einlesenKostenBetrieb())  # [€] jährliche Betriebskosten des Systems

        panelFlaeche = int(einlesenFlaeche())# [m²] Dachfläche in Quadratmetern

        normLeistung = float(einlesenLeistung())/1000# [kW/m²] Normleistung eines Quadratmeters Solaranlage

        pvCap = (panelFlaeche*normLeistung) # [m²*kW/m²] = [kW] PV Kapazität in Kilowatt

        gesamtInvest = investKostenAufbau + investKostenPanels*panelFlaeche  # [€/m²*m²] = [€] Gesamtinvestition in €

        ausgabeText("Kapazität der PV-Anlage: " + str(pvCap) + "kW\n\n")

        ausgabeText("Gesamtinvestition: " + str(gesamtInvest) + "€\n\n")
        ausgabeText("Berechnung:\n\n")


        ersparnis, leistungsPreisErsparnis = berechnung(pvCap, data)

        gesamtErsparnis = (ersparnis + leistungsPreisErsparnis)

    except:
        ausgabeText("Zur Berechnung fehlen Werte für die PV-Anlage in der Eingabe\n")
        return

    ausgabeText("\n\nDie gesamte jährliche Ersparnis beträgt: " + str(round(gesamtErsparnis, 2)) + "€\n\n")

    ausgabeText("Die Leistungspreisersparnis beträgt: " + str(leistungsPreisErsparnis) + "€\n\n")

    ausgabeText("Die Amortisationszeit beträgt: " + str(amortisation(gesamtErsparnis, gesamtInvest, betriebsKosten)) + " Jahre \n\n")

    ausgabeText("Bei einer Gesamtinvestition von: " + str(gesamtInvest) + "€\n\n")

    ausgabeText("Mit jährlichen Betriebskosten von: " + str(betriebsKosten) + "€\n\n")

    ausgabeText("\n------------------------------------------------------------------------\n\n")

    ausgabeText("Alternative Flächen:\n")

    endeAnzeigen()


    # weitere Flächengrössen berechnen
    spaces = [panelFlaeche - 10, panelFlaeche - 5, panelFlaeche - 2, panelFlaeche + 2, panelFlaeche + 5,panelFlaeche + 10] # hier noch die Fälle einbauen falls die installierte Fläche kleiner als 4 m² ist!


    for xRoofspace in spaces:

        if (xRoofspace>0):
            ersparnis, leistungsPreisErsparnis = berechnung(xRoofspace*normLeistung, data)

            gesamtErsparnis = (ersparnis + leistungsPreisErsparnis)

            gesamtInvest = investKostenAufbau + investKostenPanels*(xRoofspace) # neue Investitionskosten berechnen

            ausgabeText("\n\nDie jährliche Ersparnis mit " + str(xRoofspace) + " m² installierter Fläche beträgt: "+ str(round(gesamtErsparnis, 2)) + "€\n\n")

            ausgabeText("Die Leistungspreisersparnis beträgt: " + str(leistungsPreisErsparnis) + "€\n\n")

            ausgabeText("Die Amortisationszeit beträgt dann: " + str(amortisation(gesamtErsparnis, gesamtInvest, betriebsKosten)) + " Jahre\n\n")

            ausgabeText("Bei einer Gesamtinvestition von: " + str(gesamtInvest) + "€\n\n")

            ausgabeText("Mit jährlichen Betriebskosten von: " + str(betriebsKosten) + "€\n\n")

            endeAnzeigen()

    #-------------------Plotten der Kurven---------------------------

    #plot(data)

    return

#------------------------------------GUI (Darstellung)---------------------------------------------------------


#-----------------Lesen/schreiben GUI----------

#------einlesen---------

def einlesenKostenPanels():
    return eingabeKostenPanels.get()

def einlesenFlaeche():
    return eingabeFlaeche.get()

def einlesenLeistung():
    return eingabeLeistung.get()

def einlesenKostenAufbau():
    return eingabeKostenAufbau.get()

def einlesenKostenBetrieb():
    return eingabeKostenBetrieb.get()

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
    eingabeKostenPanels.delete(0, END)
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
labelAusgabe= Label(frameRechts, text ="Ausgabe:")

labelInput= Label(frameLinks, text = "Pfad der Input-Datei")
eingabeDatei = Entry(frameLinks, width = 20)

labelSolaranlage= Label(frameLinks, text ="Daten Solaranlage:")

labelFlaeche= Label(frameLinks, text="Fläche [m²]")
eingabeFlaeche = Entry(frameLinks, width = 20)

labelLeistung= Label(frameLinks, text="Normalleistung [W/m²]")
eingabeLeistung = Entry(frameLinks, width = 20)

labelKostenPanels= Label(frameLinks, text="Investition Panels [€/m²]")
eingabeKostenPanels = Entry(frameLinks, width = 20)

labelKostenAufbau= Label(frameLinks, text="Investition Aufbau [€]")
eingabeKostenAufbau = Entry(frameLinks, width = 20)

labelKostenBetrieb= Label(frameLinks, text="Betriebskosten [€/Jahr]")
eingabeKostenBetrieb = Entry(frameLinks, width = 20)


buttonBerechnen = Button(frameLinks,text= "Berechnen", command=rechenThread)
buttonUebersicht = Button(frameLinks,text= "Übersicht", command=uebersicht)

textErgebnis = Text(frameRechts, width = 80, height =23, yscrollcommand=scrollbar.set)

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

labelDateneingabe.pack(side=TOP)
labelAusgabe.pack(side=TOP)

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

labelKostenPanels.pack()
eingabeKostenPanels.pack()

labelKostenAufbau.pack()
eingabeKostenAufbau.pack()

labelKostenBetrieb.pack()
eingabeKostenBetrieb.pack()

emptyLabel4.pack()

buttonBerechnen.pack(side=RIGHT)
buttonUebersicht.pack(side=LEFT)

textErgebnis.pack()

root.mainloop()