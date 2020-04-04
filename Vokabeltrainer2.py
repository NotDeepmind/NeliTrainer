import tkinter as tk
from tkinter import filedialog
import json
from datetime import datetime as dt
import datetime as dtt
import os as os
from ChangeManagement import ChangeManagement as CM
import functions
import C_selection
import csv

"""
This is a vocable trainer program.
For now, it is designed to be used by 3 different users (Andreas, Christa, gemeinsam).
It uses language data in german and spanish, the presented language can be chosen freely, e.g. german is presented and spanish has to be entered by the user.
There are two modes of vocable training:
    "nach Reihenfolge" is a simple mode to ask a list of vocables, starting at the first and working through the whole list. The number of vocables to be checked for a session is to be entered by the user. When 
        finishing a session and restarting at a later date, the asked vocables continues after the last answered entry in the last session.
    "nach Fälligkeit" uses a system of intervals for each vocable in the list. Every vocable for every user has a date, when the vocable is to be checked again. After answering, the user can chose an interval of days 
        to wait until the vocable is asked again. This System makes sure that the user can learn vocables that are harder to memorize more often. The number of vocables per session results from the due vocables and 
        can large, but forces the user to learn every vocable at least once in 180 days (the maximum interval between checks), regardless of the "nach Reihenfolge" work.
        
Additional functions are:
    A section where entries in the database can be looked up and modified as desired.
    A section to add new entries in a list of TSV, which can be created using common online sources for vocable lists.
    All Entries can be decorated by a "kommentar", which is presented to the user during questioning regardless of the presented language. This is mainly used to give context where necessary, e.g. "schnell" (fast) can 
        be understoof in a temporal context or in terms of velocity.
    After checking the answer to an asked vocable, the correctly entered results are highlighted in green while wrong or missing entries are highlighted in red. Where multiple answers are necessary, 
        separated entry fields are given equal to the number of entries required. All answeres given are stored in the database for further evaluation at a later point and/or in a separate program. In case of 
        accidental misspelling of answers, a button "Tippfehler" can be used to disregard all wrong answers. Also, if desired by the user an entry of a simple "#"-character is a wildcard entry and counts for all 
        entries to be correct (effectively skipping easy vocables)
    After completing a session, either by answering all the vocables of prematurely be the corresponding button, a screen will appear showing the number of answered vocables as well as correct and wrong answers. From 
        here, the wrong answers can be repeated to improve the learning effect. This loop can be repeated as often as desired, or until all vocables have been answered correctly at least once.
    After finishing a session the results have to be saved by pressing the correspoing buttons "Speichern & Beenden" or "Speichern & Neustarten". While the former will quit the program, the latter one will repeat from 
        the selection screen but memorize the chosen vocable database. 
    When answering "nach Fälligkeit", after every vocable the user can choose 1 out of 3 intervals for when to be asked the same vocable again. The possible intervals presented to the user depend on the previous 
        interval and are defined in the list "IntervalMatrix" at the beginning of this code.


Datastructure:
 
This is the main File for the vocable trainer program.
Here the Namespace is defined and all GUI related code.
All functions and classes/methods are separated from these GUI definitions to facilitate a change of GUI Framework at any later point in development.
The classes used are defined in C_vocables, every vocable entry is an object of this class. The vocable database is a list of these objects.
C-Selection contains the information about which vocables are to show. Hence, the index numbers (corresponding to the list of vocables) are stored here. After every go-through of the vocables, the wrong answers can be
    repeated and are stored in another list of indices. Any advanced logic in presented vocables (e.g. randomly chosen entries) should be made here.
The ChangeManagement class contains all methods to handle the searching of vocable entries and changing these.
functions.py is used where classes do not seem ideal, e.g. building the list of vocable objects when loading a file.
"""

#todo restrcutre data and use SQL database
#todo implement a proper user management

#todo double check whether or not to move to django and operate a prograssive web app using proper service workers

### Um Alte Daten einzulesen, folgende Variable auf 1 setzen:
read_old_data = 0

### Um das JSON File schön zu formatieren, folgende Variable auf 1 setzen.
### (ohne schöne Formatierung lässt sich erheblich Speicherplatz sparen)
nice_JSON = 0

#compile via console in folder containing MainFile.py --> pyinstaller -F Vokabeltrainer2.py

IntervalMatrix = []
# defines the optional interval when answering vocables in "nach Fälligkeit" mode.
    # first column and second column define the last interval
    # third to fifth column are the new interval presented to the user as buttons
    # e.g. a vocable's last interval was 15 days, then the user can choose to repeat the same vocable after 22, 1 or 11 days.
    # the use is to either increase the interval steadily when happy with the learning success, decrease the interval slightly to improve leaning performance, or start again at interval of 1 day if much stronger focus
    # on the particular vocable is desired.
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
        self.restart = 0 # used in "Speichern & Beenden" button, 0 > close program, 1 > restart program
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
        # The GUi is separated roughly in 3 regions when training vocable data
        # +--------------+--------------+
        # | frame[0]     | frame[1]     |
        # | presented    | user answers |
        # +--------------+--------------+
        # |    frameButtons             |
        # | pressable buttons here      |
        # +-----------------------------+
        self.ET_Answer = [] # list of entry fields for user answers to vocables
        self.label_presented=[] # presented vocables as labels
        self.fontLayout = ("Helvetica", "10") # as of now controls the font of all text in the GUI
        self.languagemode = [] # sets the language presented, 0 = german, 1 = spanish, will be chosen at the start up menu
        self.ButtonLayout = "MainScreen" # the buttom frame containing buttons has multiple templates, the currently used template can be stored here
        self.path = "" # defines the path to the vocable database
        self.path_AddVocables = "" # defines the path to a TSV or TXT if adding vocables to the main database
        self.user = "" # contains the current user
        self.user_answers = [] # lists all answers given during the session
        self.user_answers_idx = [] # lists the index in the vocable list of any answer of the session
        self.user_answers_NumVocables = -1 # number of vocables trained during session
        self.user_answers_total = 0 # number of vocables trained in all session (continues even when repeating wrong answers, greater or equal to self.user_answers_NumVocables
        self.width = 20 # common button width
        self.height = 1 # common button height
        self.mode = [] # either "nach Fälligkeit" or "nach Reihenfolge", set during start up menu
        self.RadioBtns = {} # stores all the radio buttons in start up menu
        self.RadioBtns["errors"]=[] # used in start up menu if radio buttons are chosen wrong and/or are missing
        self.MaxNumVocables = 0 # set in start up menu for "nach Reihenfolge", defines how many vocables to ask in this session
        self.vocables = [] # stores the list of all vocables in current database
        self.testmode = False # used only during testing
        self.Selector = C_selection.C_selection() # initialize selection object, only on is used to determine which vocable to ask during training
        self.presented = [] # labels of presented words of current vocable during training
        self.requested = [] # labels of correct answers for all words curing training
        self.kommentar = "" # comment field content during training

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
            if self.path != "":
                self.btn_SelectLecture.invoke()
            if read_old_data == 1:
                tk.Button(self.frameButtons, text="Read Old Data (Andreas)", font=self.fontLayout, command=self.Buttonfunc_ReadOldData).pack()
        ####################################################################################################################################
        elif self.ButtonLayout == "MainScreen2":
            LecName = self.path.split("/")
            LecName = LecName[-1].split(".")
            tk.Label(self.frame[1], text = "", font = self.fontLayout).pack()
            tk.Label(self.frame[1], text = LecName[0], font = self.fontLayout, fg = "#0000FF").pack()
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
            tk.Label(self.frameButtons, text="Deutsch | Spanisch | Kommentar | Fällig Andreas YYYY-MM-DD | Fällig Christa YYYY-MM-DD").pack()
            tk.Button(self.frameButtons, text="Datenbank als .TSV speichern", width=2*self.width, height=self.height, font=self.fontLayout,
                      command=self.Buttonfunc_saveTSV).pack()
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
        self.vocables = functions.AddVocables(self.vocables, self.path_AddVocables)
        #self.Buttonfunc_saving() #for now, the enlarged database is only saved if and when it is used immediately for one of the users. There is no point in adding vocables and not using them right away..

    def Buttonfunc_ChangeManagement(self):
        self.SearchResults = CM()
        for widget in self.frameButtons.winfo_children():
            widget.destroy()
        for widget in self.frame[0].winfo_children():
            widget.destroy()
        for widget in self.frame[1].winfo_children():
            widget.destroy()
        tk.Label(self.frame[0], text="SUCHE:",font=self.fontLayout).grid(row=1, column=1)
        Attributes = ["Deutsch:", "Spanisch:", "Kommentar:"]
        i = 0
        SearchEntries=[]
        for item in Attributes:
            i += 1
            tk.Label(self.frame[0], text=item, font=self.fontLayout, anchor="w").grid(row=i+1, column=1, sticky="W")
            SearchEntries.append(tk.Entry(self.frame[0], font=self.fontLayout))
            SearchEntries[-1].grid(row=i+1, column=2)
        tk.Label(self.frame[1], text="Gefunden:").grid(row=1, column=1)
        i = 0
        self.FoundEntries=[]
        for item in Attributes:
            i += 1
            tk.Label(self.frame[1], text=item, font=self.fontLayout, anchor="w").grid(row=i*2, column=1, sticky="W")
            self.FoundEntries.append(tk.Entry(self.frame[1], font=self.fontLayout, width=30))
            self.FoundEntries[-1].grid(row=2*i+1, column=1, columnspan=2)
        tk.Button(self.frame[1], text="Nächstes", font=self.fontLayout,
                  command= lambda: self.Buttonfunc_CM_next(self.FoundEntries)).grid(row=8,column=2, sticky="W")
        tk.Button(self.frame[1], text="Vorheriges", font=self.fontLayout,
                  command= lambda: self.Buttonfunc_CM_previous(self.FoundEntries)).grid(row=8,column=1, sticky="E")
        tk.Button(self.frame[1], text="Speichern", font=self.fontLayout,
                  command=lambda: self.Buttonfunc_CM_save(self.FoundEntries)).grid(row=9,column=1,columnspan=2)
        tk.Button(self.frame[0], text="Suchen", font=self.fontLayout,
                  command=lambda: self.Buttonfunc_CM_search(SearchEntries[0].get(),SearchEntries[1].get(),SearchEntries[2].get(), self.vocables, self.FoundEntries)).grid(row=5,column=1,columnspan=2)
        self.ButtonLayout = "MainScreen"
        tk.Button(self.frameButtons, text="Zurück zum Hauptmenü", font=self.fontLayout, command=self.Create_Buttons).pack()
    def Buttonfunc_CM_next(self, ResultFields):
        self.SearchResults.next()
        self.CM_refreshResults(ResultFields)
    def Buttonfunc_CM_previous(self, ResultFields):
        self.SearchResults.previous()
        self.CM_refreshResults(ResultFields)
    def Buttonfunc_CM_save(self, ResultFields):
        self.SearchResults.ChangedEntries(ResultFields[0].get(), ResultFields[1].get(), ResultFields[2].get())
        for key in ["deutsch", "spanisch", "kommentar"]:
            self.vocables[self.SearchResults.IDs[self.SearchResults.idx]].content[key] = self.SearchResults.NewEntry[key]
        for field in ResultFields:
            field.delete(0, "end")
        functions.saving(self.path, self.vocables,1)

    def Buttonfunc_CM_search(self, deutsch, spanisch, kommentar, vocables, ResultFields):
        self.SearchResults.Search(deutsch, spanisch, kommentar, vocables)
        if len(self.SearchResults.IDs) == 0:
            tk.Label(self.frame[1], text="Eintrag nicht gefunden", anchor="w", fg="RED").grid(row=1, column=1,columnspan=2, sticky="W")
        self.CM_refreshResults(ResultFields)
    def CM_refreshResults(self, ResultFields):
        if len(self.SearchResults.IDs) > 0:
            for field in ResultFields:
                field.delete(0, "end")
            ResultFields[0].insert(0, self.SearchResults.OrigEntires[self.SearchResults.idx]["deutsch"])
            ResultFields[1].insert(0, self.SearchResults.OrigEntires[self.SearchResults.idx]["spanisch"])
            ResultFields[2].insert(0, self.SearchResults.OrigEntires[self.SearchResults.idx]["kommentar"])

    def Buttonfunc_CheckEntry(self):
        self.vocables[self.Selector.idx], label_colors, correctness, self.vocables[0] = functions.CheckEntry(self.ET_Answer, self.vocables[self.Selector.idx], self.requested, self.user, self.Selector, self.vocables[0])
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
        self.user_answers_NumVocables, corrects, falses, self.user_answers_total = functions.EndSession(self.user_answers, self.user_answers_NumVocables, self.user_answers_total)
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
        elif self.path == "":
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

    def Buttonfunc_saveTSV(self):
        if self.path[-3:] == "txt" or self.path[-3:] == "tsv":
            print("Eine TSV wurde geladen, es macht keinen Sinn diese als TSV neu zu speichern!")
        elif os.path.isfile(self.path[:-5] + "_export.tsv"):
            print("Eine TSV mit diesem Namen ist bereits vorhanden! Bitte alte Datei löschen!")
        else:
            functions.saveTSV(self.vocables, self.path[:-5])
            #print("Created File " + self.path[:-5] + "_export.tsv")

    def Buttonfunc_Tippfehler(self):
        self.vocables[self.Selector.idx], self.user_answers = functions.tippfehler(self.vocables[self.Selector.idx], self.user, self.user_answers)
        self.Btn_Tippfehler.destroy()



if __name__ == "__main__":
    GUI = MyGUI()
    GUI.restart = 1
    GUI.root.destroy()
    while GUI.restart == 1:
        path = GUI.path
        del GUI
        GUI = MyGUI()
        GUI.path = path
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