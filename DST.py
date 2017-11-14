# This Python file uses the following encoding: utf-8

from Tkinter import *
from numpy import *


#-------------Funktionen-----------------------
def leer():
    return

def schliessen(event=None):
    root.destroy()
    return

dateihandler = open("Inputs_WHO.csv")
inhalt = dateihandler.read()
zeilen = inhalt.split("\n")

inputTabelle = []

for i in range(len(zeilen)):
    spalten = zeilen[i].split(";")
    inputTabelle.append(spalten)
    inputTabelle[i][1:] =[float(zahl)for zahl in inputTabelle[i][1:]]

pvOutput= [zeile[1] for zeile in inputTabelle] #die spalte PVOutput wird aus der Inputtabelle ausgelesen.



print(inputTabelle[2][1])
print(inputTabelle[2])

print(inputTabelle.__len__())

print(pvOutput)

#----------------------------------------------------------GUI-----------------------------------------------------

#-------------Hauptfenster initialisieren------

root = Tk()
root.title("Decision Support Tool")

#-------------Widgets erstellen----------------

frameRechts =Frame(root, width=500, height=100)
frameLinks =Frame(root, width=500, height=100)


labelDateneingabe= Label(frameLinks, text ="Dateneingabe")

labelLastgang= Label(frameLinks, text = "Lastgang")
entryLastgang = Entry(frameLinks, width = 20)

labelFlaeche= Label(frameLinks, text="Fläche der Solaranlage")
entryFlaeche = Entry(frameLinks, width = 20)

buttonBerechnen = Button(frameLinks,text= "Berechnen" )

textErgebnis= Text(frameRechts, width = 50, height =20)

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

labelLastgang.pack()
entryLastgang.pack()

emptyLabel1.pack()

labelFlaeche.pack()
entryFlaeche.pack()

emptyLabel2.pack()

buttonBerechnen.pack(side=BOTTOM)

textErgebnis.pack()

root.mainloop()
