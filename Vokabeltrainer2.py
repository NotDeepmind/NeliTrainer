import tkinter as tk
from tkinter import filedialog
import json
from datetime import datetime as dt
import datetime as dtt
import os as os
from ChangeManagement import ChangeManagement
import functions
import C_selection

#todo test GUI functions by NOT calling root.mainloop(), but invoking buttons directly without display
# https://stackoverflow.com/questions/27430176/how-can-python-code-with-tkinter-mainloop-be-tested

### Um Alte Daten einzulesen, folgende Variable auf 1 setzen:
read_old_data = 0

### Um das JSON File schön zu formatieren, folgende Variable auf 1 setzen.
### (ohne schöne Formatierung lässt sich erheblich Speicherplatz sparen)
nice_JSON = 0

#compile via console in folder containing MainFile.py --> pyinstaller -F Vokabeltrainer2.py

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
        self.testmode = False
        self.Selector = C_selection.C_selection()

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
            self.AddLabel(self.frame[0], "Benutzerauswahl:")
            self.RadioBtns["user selection"] = tk.StringVar(self.frame[0],value="x")
            optionlist = ["Andreas", "Christa", "Gemeinsam"]
            self.AddRadioButtons(optionlist, self.frame[0], self.RadioBtns["user selection"])

            self.AddLabel(self.frame[0], "Vorgabe auf:")
            self.RadioBtns["language"] = tk.StringVar(self.frame[0], value="x")
            optionlist = ["spanisch", "deutsch"]
            self.AddRadioButtons(optionlist, self.frame[0], self.RadioBtns["language"])

            self.AddLabel(self.frame[1], "Abfragemodus:")
            self.RadioBtns["mode"] = tk.StringVar(self.frame[1], value="x")
            optionlist = ["nach Fälligkeit", "nach Reihenfolge"]
            self.AddRadioButtons(optionlist, self.frame[1], self.RadioBtns["mode"])

            self.AddLabel(self.frame[1], "Maximale Abfragen bei Reihenfolge:")
            self.MaxNumVocables=tk.Entry(self.frame[1], font = self.fontLayout)
            self.MaxNumVocables.pack()

            self.btn_SelectLecture = tk.Button(self.frameButtons, text="Lektion auswählen", font=self.fontLayout,
                                               command=self.Buttonfunc_LoadData)
            self.btn_SelectLecture.pack()
            if read_old_data == 1:
                tk.Button(self.frameButtons, text="Read Old Data (Andreas)", font=self.fontLayout, command=self.Buttonfunc_ReadOldData).pack()
            self.ButtonLayout = "MainScreen2"
        elif self.ButtonLayout == "MainScreen2":
            self.btn_SelectLecture.pack_forget()
            self.btn_continue = tk.Button(self.frameButtons, text="Weiter", width=2 * self.width, height=self.height, font=self.fontLayout,
                       command=self.Buttonfunc_Continue)
            self.btn_continue.pack()
            tk.Button(self.frameButtons, text="Einträge ändern", width=2 * self.width, height=self.height,
                       font=self.fontLayout,
                       command=self.Buttonfunc_ChangeManagement).pack()
            tk.Button(self.frameButtons, text="Weitere Vokabeln aus .TSV hinzufügen", width=2 * self.width,
                      height=self.height, font=self.fontLayout,
                      command=self.Buttonfunc_AddVocables).pack()

    def AddLabel(self, parent, text):
        tk.Label(parent, text=text, font=self.fontLayout).pack(anchor="w", ipadx=10)

    def AddRadioButtons(self, optionlist, parent, variable):
        RadioBtnsContents = []
        for option in optionlist:
            RadioBtnsContents.append(
                tk.Radiobutton(parent, text=option, variable=variable, value=option))
            RadioBtnsContents[-1].config(font=self.fontLayout)
            RadioBtnsContents[-1].pack(side='top', anchor='w', ipadx=30)

    def Buttonfunc_AddVocables(self):
        pass

    def Buttonfunc_ChangeManagement(self):
        pass

    def Buttonfunc_Continue(self):
        for error in self.RadioBtns["errors"]:
            error.pack_forget()
        errors = 0
        if self.RadioBtns["user selection"].get() == "x":
            self.RadioBtns["errors"].append(tk.Label(self.frame[1], text="Bitte Benutzer auswählen!", fg="RED"))
            self.RadioBtns["errors"][-1].pack(anchor = "w")
            errors = 1
        else:
            self.user=self.RadioBtns["user selection"].get()
            self.vocables, self.Selector = functions.Userselection(self.user, self.vocables, self.Selector)
            print(self.Selector.Entities[1])

        if self.RadioBtns["language"].get() == "x":
            self.RadioBtns["errors"].append(tk.Label(self.frame[1], text="Bitte Sprache auswählen!", fg="RED"))
            self.RadioBtns["errors"][-1].pack(anchor = "w")
            errors = 1
        elif self.RadioBtns["language"].get()=="deutsch":
            self.languagemode = 0
        elif self.RadioBtns["language"].get()=="spanisch":
            self.languagemode = 1

        if self.RadioBtns["mode"].get() == "x":
            self.RadioBtns["errors"].append(tk.Label(self.frame[1], text="Bitte Modus auswählen!", fg="RED"))
            self.RadioBtns["errors"][-1].pack(anchor = "w")
            errors = 1
        elif (self.RadioBtns["mode"].get() == "nach Reihenfolge") and (self.MaxNumVocables.get()==""):
            self.RadioBtns["errors"].append(tk.Label(self.frame[1], text="Bitte Maximal Anzahl eingeben!", fg="RED"))
            self.RadioBtns["errors"][-1].pack(anchor = "w")
            errors = 1
        else:
            self.mode = self.RadioBtns["mode"].get()

        if (self.RadioBtns["user selection"].get() != "x"):
            if (len(self.Selector.Entities[1]) == 0) and (self.RadioBtns["mode"].get() == "nach Fälligkeit"):
                self.RadioBtns["errors"].append(tk.Label(self.frame[1], text="Keine Vokabeln für heute fällig!", fg="RED"))
                self.RadioBtns["errors"][-1].pack(anchor = "w")
                errors = 1

        if errors == 0:
            pass
            #self.MaxNumVocables = self.MaxNumVocables.get()
            #self.Buttonfunc_NextVocable()
            #self.ButtonLayout = 1
            #self.Create_Buttons()

    def Buttonfunc_LoadData(self):
        if self.testmode:
            self.path, self.vocables, self.Selector = functions.LoadData(os.path.dirname(os.path.abspath(__file__)) + "\Testdata.json", self.Selector)
        else:
            self.path, self.vocables, self.Selector = functions.LoadData(filedialog.askopenfilename(), self.Selector)
        self.Create_Buttons()

    def Buttonfunc_ReadOldData(self):
        pass




def AddLabel(parent, text, GUI):
    tk.Label(parent, text=text, font=GUI.fontLayout).pack(anchor="w", ipadx=10)
def AddRadioButtons(optionlist, parent, variable, GUI):
    RadioBtnsContents=[]
    for option in optionlist:
        RadioBtnsContents.append(
            tk.Radiobutton(parent, text=option, variable=variable, value=option))
        RadioBtnsContents[-1].config(font=GUI.fontLayout)
        RadioBtnsContents[-1].pack(side='top', anchor='w', ipadx=30)


if __name__ == "__main__":
    MyGUI = MyGUI()
    MyGUI.Create_Buttons()
    MyGUI.root.mainloop()



# class testclass:
#     def testaction(self):
#         self.test=True
#
# testc = testclass()
# functions.testmethod(testc)
# print(testc.test)
#
# root = tk.Tk(className=" Nehls'scher Vokabeltrainer")
# canvas = tk.Canvas(root, height=500, width=900)
# canvas.pack()
# frame = []
# frame.append(tk.Frame(root))
# frame[0].place(relwidth=0.5, height=300)
# frame.append(tk.Frame(root))
# frame[1].place(relwidth=0.5, height=300, relx=0.5)
# frameButtons = tk.Frame(root)
# frameButtons.place(relwidth=1, height=160, rely=300 / (300 + 160))
# functions.testfunction(frameButtons).pack()

#root.mainloop()