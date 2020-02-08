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
        self.restart = 0
        self.root = tk.Tk(className=" Nehls'scher Vokabeltrainer")
        self.canvas = tk.Canvas(self.root, height=700, width=900)
        self.canvas.pack()
        self.frame = []
        self.frame.append(tk.Frame(self.root))
        self.frame[0].place(relwidth=0.5, height=500)
        self.frame.append(tk.Frame(self.root))
        self.frame[1].place(relwidth=0.5, height=500, relx=0.5)
        self.frameButtons = tk.Frame(self.root)
        self.frameButtons.place(relwidth=1, height=200, rely=500 / (500 + 200))
        self.ET_Answer = []
        self.label_presented=[]
        self.fontLayout = ("Helvetica", "18")
        self.languagemode = 1
        self.ButtonLayout = "MainScreen"
        self.path = ""
        self.user = ""
        self.user_answers = []
        self.user_answers_idx = []
        self.user_answers_NumVocables = -1
        self.user_answers_total = 0
        self.width = 20
        self.height = 1
        self.mode = []
        self.RadioBtns = {}
        self.RadioBtns["errors"]=[]
        self.MaxNumVocables = 0
        self.ButtonLayout = "MainScreen"
        self.RadioBtnsContents=[]
        self.vocables = []
        self.testmode = False
        self.Selector = C_selection.C_selection()
        self.presented = []
        self.requested = []
        self.kommentar = ""

    def Create_Buttons(self,ButtonLayout = None):
        if ButtonLayout != None:
            self.ButtonLayout = ButtonLayout
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
            self.ET_MaxNumVocables=tk.Entry(self.frame[1], font = self.fontLayout)
            self.ET_MaxNumVocables.pack()

            self.btn_SelectLecture = tk.Button(self.frameButtons, text="Lektion auswählen", font=self.fontLayout,
                                               command=self.Buttonfunc_LoadData)
            self.btn_SelectLecture.pack()
            if read_old_data == 1:
                tk.Button(self.frameButtons, text="Read Old Data (Andreas)", font=self.fontLayout, command=self.Buttonfunc_ReadOldData).pack()
        ####################################################################################################################################
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
        ####################################################################################################################################
        elif self.ButtonLayout == "AskVocable":
            self.CheckVocable = tk.Button(self.frameButtons, text="Eingabe prüfen", font=self.fontLayout, width=self.width,
                      height=self.height, command=self.Buttonfunc_CheckEntry)
            self.CheckVocable.pack()
            tk.Button(self.frameButtons, text="Session beenden", font=self.fontLayout, width=self.width,
                      height=self.height,command=self.Buttonfunc_EndSession).pack()
            self.root.bind("<Return>", lambda event: self.CheckVocable.invoke())
        ####################################################################################################################################
        if self.ButtonLayout == "CheckedVocable":
            if self.mode == "nach Fälligkeit":
                tk.Label(self.frameButtons, text="Erneut fragen in:", font=self.fontLayout, width=self.width, height=self.height).grid(row=1, column=1)
                self.Frame_Buttons_delay = tk.Frame(self.frameButtons, width=288, height=45)
                self.Frame_Buttons_delay.grid(row=2, column=1)
                intervals = functions.intervals(self.vocables[self.Selector.idx], IntervalMatrix, self.user)
                Buttons=[]
                # These buttons cannot be created by a loop, since the lambda functions will always be excecuted with the last iteraton's variable
                Buttons.append(tk.Button(self.Frame_Buttons_delay, text="+" + str(intervals[0]) + "Tage", command=lambda: self.Buttonfunc_AddDelay(intervals[0]), font=self.fontLayout, height=self.height))
                Buttons[-1].grid(row=1, column=0)
                Buttons.append(tk.Button(self.Frame_Buttons_delay, text="+" + str(intervals[1]) + "Tage", command=lambda: self.Buttonfunc_AddDelay(intervals[1]), font=self.fontLayout, height=self.height))
                Buttons[-1].grid(row=1, column=1)
                Buttons.append(tk.Button(self.Frame_Buttons_delay, text="+" + str(intervals[2]) + "Tage", command=lambda: self.Buttonfunc_AddDelay(intervals[2]), font=self.fontLayout, height=self.height))
                Buttons[-1].grid(row=1, column=2)
                self.root.bind("<Return>", lambda event: Buttons[0].invoke())
            elif self.mode == "nach Reihenfolge":
                self.btn_NextVocable = tk.Button(self.frameButtons, text="Nächste Vokabel", command=lambda: self.Buttonfunc_AddDelay(-1), font=self.fontLayout, height=self.height, width=self.width)
                self.btn_NextVocable.grid(row=1, column=1)
                self.root.bind("<Return>",lambda event: self.btn_NextVocable.invoke())
            self.Btn_Tippfehler = tk.Button(self.frameButtons, text="Tippfehler", font=self.fontLayout, width=self.width, height=self.height,  command=self.Buttonfunc_Tippfehler)
            self.Btn_Tippfehler.grid(row=3, column=1)
        ####################################################################################################################################
        elif self.ButtonLayout == "EndSession":
            for i in range(len(self.user_answers)):
                if (self.user_answers[i] == "Falsch"):
                    tk.Button(self.frameButtons, text="Falsche Antworten wiederholen", font=self.fontLayout, width=2 * self.width, height=self.height, command=self.Buttonfunc_Repeat_Wrong_Answers).grid(row=3, column=2)
                    break
            tk.Button(self.frameButtons, text="Speichern & Neustarten", font=self.fontLayout, width=2 * self.width, height=self.height, command=self.Buttonfunc_Save_Restart).grid(row=4, column=2)
            tk.Button(self.frameButtons, text="Speichern & Beenden", font=self.fontLayout, width=2 * self.width, height=self.height, command=self.Buttonfunc_Save_Exit).grid(row=5, column=2)
            self.root.unbind("<Return>")


    def AddLabel(self, parent, text):
        tk.Label(parent, text=text, font=self.fontLayout).pack(anchor="w", ipadx=10)

    def AddRadioButtons(self, optionlist, parent, variable):
        RadioBtnsContents = []
        for option in optionlist:
            RadioBtnsContents.append(
                tk.Radiobutton(parent, text=option, variable=variable, value=option))
            RadioBtnsContents[-1].config(font=self.fontLayout)
            RadioBtnsContents[-1].pack(side='top', anchor='w', ipadx=30)

    def Buttonfunc_AddDelay(self, delay):
        self.vocables[self.Selector.idx].AddDelay(self.user, delay, self.mode)
        if len(self.user_answers) >= self.MaxNumVocables:
            self.Buttonfunc_EndSession()
        else:
            self.Buttonfunc_NextVocable()

    def Buttonfunc_AddVocables(self):
        pass

    def Buttonfunc_ChangeManagement(self):
        pass

    def Buttonfunc_CheckEntry(self):
        self.vocables[self.Selector.idx], label_colors, correctness = functions.CheckEntry(self.ET_Answer, self.vocables[self.Selector.idx], self.requested, self.user)
        self.user_answers.append(correctness)
        self.user_answers_idx.append(self.Selector.idx)
        for request, color in zip(self.requested, label_colors):
            tk.Label(self.frame[1], text=request, font=self.fontLayout, fg=color).pack()
        self.Create_Buttons("CheckedVocable")

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
            self.vocables, self.Selector, self.MaxNumVocables = functions.Userselection(self.user, self.vocables, self.Selector)

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
        elif (self.RadioBtns["mode"].get() == "nach Reihenfolge") and (self.ET_MaxNumVocables.get() == ""):
            self.RadioBtns["errors"].append(tk.Label(self.frame[1], text="Bitte Maximal Anzahl eingeben!", fg="RED"))
            self.RadioBtns["errors"][-1].pack(anchor = "w")
            errors = 1
        elif self.RadioBtns["mode"].get() == "nach Reihenfolge":
            self.MaxNumVocables = int(self.ET_MaxNumVocables.get())
        self.mode = self.RadioBtns["mode"].get()

        if (self.RadioBtns["user selection"].get() != "x"):
            if (len(self.Selector.Entities[1]) == 0) and (self.RadioBtns["mode"].get() == "nach Fälligkeit"):
                self.RadioBtns["errors"].append(tk.Label(self.frame[1], text="Keine Vokabeln für heute fällig!", fg="RED"))
                self.RadioBtns["errors"][-1].pack(anchor = "w")
                errors = 1
        if errors == 0:
            self.Buttonfunc_NextVocable()

    def Buttonfunc_EndSession(self):
        self.user_answers_NumVocables, corrects, falses, self.user_answers_total, self.vocables[0] = functions.EndSession(self.user_answers, self.user_answers_NumVocables, self.Selector, self.user_answers_total,
                                                                                                                       self.vocables[0], self.user)
        for frame in self.frame:
            for widget in frame.winfo_children():
                widget.destroy()
        tk.Label(self.frame[0], text=str(self.user) + ",", font=("Helvetica", 30)).pack()
        tk.Label(self.frame[0], text="du hast in dieser Session insgesamt ").pack()
        tk.Label(self.frame[0], text=str(self.user_answers_NumVocables), font=("Helvetica", 30)).pack()
        tk.Label(self.frame[0], text=" Vokabeln beantwortet!").pack()
        tk.Label(self.frame[0], text="Im letzten Durchgang waren:").pack()
        tk.Label(self.frame[0], text=corrects + " richtig und", justify="left", anchor="w").pack()
        tk.Label(self.frame[0], text=falses + " falsch", justify="left", anchor="w").pack()
        tk.Label(self.frame[0], text="Das hier war der " + str(len(self.Selector.Entities)-1) + ". Durchgang.").pack()
        tk.Label(self.frame[0], text="Insgesamt hast du " + str(self.user_answers_total) + " Fragen beantwortet.").pack()
        self.Create_Buttons("EndSession")


    def Buttonfunc_NextVocable(self):
        self.presented, self.requested, self.kommentar = functions.NextVocable(self.Selector, self.mode, self.vocables[0].content[self.user]["last_stop"], self.languagemode, self.vocables)
        for frame in self.frame:
            for widget in frame.winfo_children():
                widget.destroy()
        self.ET_Answer = [] #delete old information
        for id in range(len(self.requested)):
            self.ET_Answer.append(tk.Entry(self.frame[1], font=self.fontLayout))
            self.ET_Answer[-1].pack()
        self.ET_Answer[0].focus() #set cursor to first Entry field
        self.label_presented=[]
        for word in self.presented:
            self.label_presented.append(tk.Label(self.frame[0], font=self.fontLayout, text=word))
            self.label_presented[-1].pack()
        tk.Label(self.frame[0], font=self.fontLayout, text="").pack() #just leave an empty line
        if self.kommentar != "":
            tk.Label(self.frame[0], font=self.fontLayout + (" bold",),
                     text="Kommentar: " + self.kommentar).pack()
        tk.Label(self.frame[0], font=self.fontLayout,
                 text="Dies ist Vokabel " + str(1 + len(self.user_answers)) + "/" + str(self.MaxNumVocables) + " der Session").pack()
        if self.Selector.listID == 0: # Abfragen nach Reihenfolge
            tk.Label(self.frame[0], font=self.fontLayout,
                     text="bzw. " + str(self.Selector.idx + 1) + "/" + str(
                         len(self.Selector.Entities[self.Selector.listID])) + " der Datenbank").pack()
        self.Create_Buttons("AskVocable")

    def Buttonfunc_LoadData(self):
        if self.testmode:
            self.path, self.vocables, self.Selector = functions.LoadData(os.path.dirname(os.path.abspath(__file__)) + "\Testdata.json", self.Selector)
        else:
            self.path, self.vocables, self.Selector = functions.LoadData(filedialog.askopenfilename(), self.Selector)
        self.Create_Buttons("MainScreen2")

    def Buttonfunc_ReadOldData(self):
        pass

    def Buttonfunc_Repeat_Wrong_Answers(self):
        self.user_answers, self.user_answers_idx, self.Selector, self.MaxNumVocables = functions.Repeat_Wrong_Answers(self.user_answers, self.user_answers_idx, self.Selector)
        self.Buttonfunc_NextVocable()
        self.Create_Buttons("AskVocable")

    def Buttonfunc_Save_Exit(self):
        functions.saving(self.path, self.vocables,1)
        self.root.destroy()

    def Buttonfunc_Save_Restart(self):
        functions.saving(self.path, self.vocables,1)
        self.restart = 1
        self.root.destroy()

    def Buttonfunc_Tippfehler(self):
        self.vocables[self.Selector.idx], self.user_answers = functions.tippfehler(self.vocables[self.Selector.idx], self.user, self.user_answers)
        self.Btn_Tippfehler.destroy()



if __name__ == "__main__":
    GUI = MyGUI()
    GUI.restart = 1
    GUI.root.destroy()
    while GUI.restart == 1:
        del GUI
        GUI = MyGUI()
        GUI.Create_Buttons("MainScreen")
        GUI.root.mainloop()




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