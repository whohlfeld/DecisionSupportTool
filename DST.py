# This Python file uses the following encoding: utf-8

from Tkinter import *
import matplotlib as mpl
import numpy as np
import pandas as pd



# ------------------------------------------Variablendeklaration-----------------------------------------------------------


# -------------------------------------------Einlesen der CSV---------------------------------------------------------------



#----------------------------------------------------------GUI-----------------------------------------------------

#----------------Funktionalität GUI------------

def berechnen():
    data = pd.read_csv(entryInput.get(), sep=";")
    i=0
    while(i<data.__len__()):
        textErgebnis.insert(END, data.loc[i, ["Timestamp"]])
        i=i+1
    return

def leer():
    return

def schliessen(event=None):
    root.destroy()
    return

#-------------Hauptfenster initialisieren------

root = Tk()
root.title("Decision Support Tool")

berechnen()

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

buttonBerechnen = Button(frameLinks,text= "Berechnen", command=berechnen)

textErgebnis = Text(frameRechts, width = 70, height =20, yscrollcommand=scrollbar.set)

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