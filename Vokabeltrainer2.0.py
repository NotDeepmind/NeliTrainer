import tkinter as tk
from tkinter import filedialog
import json
from datetime import datetime as dt
import datetime as dtt
import os as os
from ChangeManagement import ChangeManagement
import functions

### Um Alte Daten einzulesen, folgende Variable auf 1 setzen:
read_old_data = 0

### Um das JSON File schön zu formatieren, folgende Variable auf 1 setzen.
### (ohne schöne Formatierung lässt sich erheblich Speicherplatz sparen)
nice_JSON = 0

#compile via console in folder containing MainFile.py --> pyinstaller -F MainFile.py

#todo abschlussauswertung am ende --> anzahl der beantwortetetn vokabeln & Anzahl der Antworten zeigen
#todo immer 6 Antwortfelder geben <-- erstmal lassen

#todo aufgetretene Probleme:
#todo Beim erstmaligen durchgehen der fälligen Vokabeln eines neues JSON files wird vor der letzten Vokabel abgebrochen

IntervalMatrix = []
IntervalMatrix.append([	0	,	0	,	1	,	1	,	1	])
IntervalMatrix.append([	1	,	1	,	2	,	1	,	1	])
IntervalMatrix.append([	2	,	2	,	3	,	1	,	2	])
IntervalMatrix.append([	3	,	3	,	4	,	1	,	2	])
IntervalMatrix.append([	4	,	4	,	5	,	1	,	3	])
IntervalMatrix.append([	5	,	5	,	6	,	1	,	3	])
IntervalMatrix.append([	6	,	6	,	7	,	1	,	4	])
IntervalMatrix.append([	7	,	14	,	15	,	1	,	7	])
IntervalMatrix.append([	15	,	21	,	22	,	1	,	11	])
IntervalMatrix.append([	22	,	29	,	31	,	1	,	15	])
IntervalMatrix.append([	30	,	60	,	61	,	1	,	30	])
IntervalMatrix.append([	61	,	90	,	91	,	1	,	45	])
IntervalMatrix.append([	91	,	120	,	121	,	1	,	60	])
IntervalMatrix.append([	121	,	150	,	151	,	1	,	75	])
IntervalMatrix.append([	151	,	180	,	180	,	1	,	90	])


class MyGUI:
    def __init__(self):
        self.root = tk.Tk(className=" Nehls'scher Vokabeltrainer")
        self.canvas = tk.Canvas(self.root, height=500, width=900)
        self.canvas.pack()
        self.frame = []
        self.frame.append(tk.Frame(self.root))
        self.frame[0].place(relwidth=0.5, height=300)
        self.frame.append(tk.Frame(self.root))
        self.frame[1].place(relwidth=0.5, height=300, relx=0.5)
        self.frameButtons = tk.Frame(self.root)
        self.frameButtons.place(relwidth=1, height=160, rely=300 / (300 + 160))
        self.ET_Answer = []
        self.fontLayout = ("Helvetica", "18")
        self.languagemode = 1
        self.ButtonLayout = "MainScreen"
        self.path = ""
        self.user = ""
        self.user_answers = []
        self.user_answers_idx = []
        self.user_answers_NumVocables = -1
        self.width = 20
        self.height = 1
        self.mode = []
        self.RadioBtns = {}
        self.RadioBtns["errors"]=[]
        self.MaxNumVocables = []
        self.ButtonLayout = "MainScreen"
        self.RadioBtnsContents=[]
        self.vocables = []

    def Create_Buttons(self):
        for widget in self.frameButtons.winfo_children():
            widget.destroy()
        self.frameButtons.grid_rowconfigure(0, weight=1)
        self.frameButtons.grid_columnconfigure(0, weight=1)
        self.frameButtons.grid_rowconfigure(10, weight=1)
        self.frameButtons.grid_columnconfigure(10, weight=1)

        if self.ButtonLayout == "MainScreen":
            for widget in self.frameButtons.winfo_children():
                widget.destroy()
            for frame in self.frame:
                for widget in frame.winfo_children():
                    widget.destroy()
            tk.Label(self.frame[0], text = "Benutzerauswahl:", font = self.fontLayout).pack(anchor = "w", ipadx = 10)
            self.RadioBtns["user selection"] = tk.StringVar(self.frame[0],value="x")
            optionlist = ["Andreas", "Christa", "Gemeinsam"]
            for option in optionlist:
                self.RadioBtnsContents.append(tk.Radiobutton(self.frame[0], text=option, variable=self.RadioBtns["user selection"], value=option))
                self.RadioBtnsContents[-1].config(font=self.fontLayout)
                self.RadioBtnsContents[-1].pack(side = 'top', anchor = 'w', ipadx = 30)
            tk.Label(self.frame[0], text="Vorgabe auf:", font=self.fontLayout).pack(anchor="w", ipadx=10)
            self.RadioBtns["language"] = tk.StringVar(self.frame[0], value="x")
            optionlist = ["spanisch", "deutsch"]
            for option in optionlist:
                self.RadioBtnsContents.append(
                    tk.Radiobutton(self.frame[0], text=option, variable=self.RadioBtns["language"], value=option))
                self.RadioBtnsContents[-1].config(font=self.fontLayout)
                self.RadioBtnsContents[-1].pack(side='top', anchor='w', ipadx=30)
            tk.Label(self.frame[1], text="Abfragemodus:", font=self.fontLayout).pack(anchor="w", ipadx=10)
            self.RadioBtns["mode"] = tk.StringVar(self.frame[1], value="x")
            optionlist = ["nach Fälligkeit", "nach Reihenfolge"]
            for option in optionlist:
                self.RadioBtnsContents.append(
                    tk.Radiobutton(self.frame[1], text=option, variable=self.RadioBtns["mode"], value=option))
                self.RadioBtnsContents[-1].config(font=self.fontLayout)
                self.RadioBtnsContents[-1].pack(side='top', anchor='w', ipadx=30)
            tk.Label(self.frame[1], text = "Maximale Abfragen bei Reihenfolge:", font = self.fontLayout).pack()
            self.MaxNumVocables=tk.Entry(self.frame[1], font = self.fontLayout)
            self.MaxNumVocables.pack()

            self.btn_SelectLecture = tk.Button(MyGUI.frameButtons, text="Lektion auswählen", font=self.fontLayout,
                                           command=self.Buttonfunc_SelectLecture)
            self.btn_SelectLecture.pack()
            if read_old_data == 1:
                tk.Button(self.frameButtons, text="Read Old Data (Andreas)", font=self.fontLayout, command=self.Buttonfunc_ReadOldData).pack()
            self.ButtonLayout = "MainScreen2"
        elif self.ButtonLayout == "MainScreen2":
            self.btn_SelectLecture.pack_forget()
            self.btn_continue = tk.Button(MyGUI.frameButtons, text="Weiter", width=2 * self.width, height=self.height, font=self.fontLayout,
                       command=self.Buttonfunc_Continue)
            self.btn_continue.pack()
            tk.Button(self.frameButtons, text="Einträge ändern", width=2 * self.width, height=self.height,
                       font=self.fontLayout,
                       command=self.Buttonfunc_ChangeManagement).pack()
            tk.Button(self.frameButtons, text="Weitere Vokabeln aus .TSV hinzufügen", width=2 * self.width,
                      height=self.height, font=self.fontLayout,
                      command=self.Buttonfunc_AddVocables).pack()

    def Buttonfunc_AddVocables(self):
        pass

    def Buttonfunc_ChangeManagement(self):
        pass

    def Buttonfunc_Continue(self):
        pass

    def Buttonfunc_ReadOldData(self):
        pass

    def Buttonfunc_SelectLecture(self):
        self.path, self.vocables = functions.SelectLecture(filedialog.askopenfilename())
        self.Create_Buttons()


MyGUI = MyGUI()
MyGUI.Create_Buttons()
MyGUI.root.mainloop()



class testclass:
    def testaction(self):
        self.test=True

testc = testclass()
functions.testmethod(testc)
print(testc.test)

root = tk.Tk(className=" Nehls'scher Vokabeltrainer")
canvas = tk.Canvas(root, height=500, width=900)
canvas.pack()
frame = []
frame.append(tk.Frame(root))
frame[0].place(relwidth=0.5, height=300)
frame.append(tk.Frame(root))
frame[1].place(relwidth=0.5, height=300, relx=0.5)
frameButtons = tk.Frame(root)
frameButtons.place(relwidth=1, height=160, rely=300 / (300 + 160))
functions.testfunction(frameButtons).pack()

#root.mainloop()