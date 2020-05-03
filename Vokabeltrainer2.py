import tkinter as tk
from tkinter import filedialog
import json
from datetime import datetime as dt
import datetime as dtt
import os as os
from ChangeManagement import ChangeManagement as CM
import functions
import C_selection
import C_vocables
from database import Database
import csv
from VT_logger import logger, exceptionHandling

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')



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

# todo implement a proper user management

# todo double check whether or not to move to django and operate a progressive web app using proper service workers

# # # Um Alte Daten einzulesen, folgende Variable auf 1 setzen:
read_old_data = 0

# compile via terminal in folder containing MainFile.py --> pyinstaller -F --icon=icon.ico  Vokabeltrainer2.py
# first test only --> python test_Vokabeltrainer2.py MyTestCase.test_Andreas_deutsch_Fälligkeit
# test with coverage --> pytest --cov

IntervalMatrix = []
# defines the optional interval when answering vocables in "nach Fälligkeit" mode.
# first column and second column define the last interval
# third to fifth column are the new interval presented to the user as buttons
# e.g. vocable's last interval was 15 days, then the user can choose to repeat the same vocable after 22, 1 or 11 days.
# the use is to either increase the interval steadily when happy with the learning success, decrease the interval
# slightly to improve leaning performance, or start again at interval of 1 day if much stronger focus on the particular
# vocable is desired.
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
        self.root.report_callback_exception = exceptionHandling # save occuring exceptions to log file
        self.ET_Answer = [] # list of entry fields for user answers to vocables
        self.label_presented=[] # presented vocables as labels
        self.fontLayout = ("Helvetica", "18") # as of now controls the font of all text in the GUI
        self.languagemode = [] # sets the language presented, 0 = german, 1 = spanish, will be chosen at the start up menu
        self.ButtonLayout = "MainScreen" # the buttom frame containing buttons has multiple templates, the currently used template can be stored here
        self.path = "" # defines the path to the vocable database
        self.path_AddVocables = "" # defines the path to a TSV or TXT if adding vocables to the main database
        self.user = "" # contains the current user
        self.user_answers = [] # lists all answers given during the session
        self.user_answers_idx = [] # lists the index in the vocable list of any answer of the session
        self.user_answers_NumVocables = -1 # number of vocables trained during session
        self.user_answers_total = 0 # number of vocables trained in all session (continues even when repeating wrong answers, greater or equal to self.user_answers_NumVocables
        self.answer_datetime = "" # Timestamp of a recent answer, used in case of "Tippfehler" to correct the db entry
        self.width = 20 # common button width
        self.height = 1 # common button height
        self.mode = [] # either "nach Fälligkeit" or "nach Reihenfolge", set during start up menu
        self.RadioBtns = {} # stores all the radio buttons in start up menu
        self.RadioBtns["errors"]=[] # used in start up menu if radio buttons are chosen wrong and/or are missing
        self.MaxNumVocables = 0 # set in start up menu for "nach Reihenfolge", defines how many vocables to ask in this session
        self.vocables = [] # stores the list of all vocables in current database
        self.current_vocable = C_vocables.C_vocables(None)
        self.testmode = False # used only during testing
        self.Selector = C_selection.C_selection() # initialize selection object, only on is used to determine which vocable to ask during training
        self.presented = [] # labels of presented words of current vocable during training
        self.requested = [] # labels of correct answers for all words curing training
        self.kommentar = "" # comment field content during training
        self.btn_delete = [] # button widget in changemanagement to delete entries from database
        self.btn_search = tk.Button() # button widget in changemanagement to search for entries in database
        self.btn_Tippfehler = tk.Button()


    def Create_Buttons(self,ButtonLayout = None):
        """ This method manages the buttons at the bottom part of the GUI
        The correct layout is chosen via the ButtonLayout variable"""
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
                tk.Button(self.frameButtons,
                          text="Read Old Data (Andreas)",
                          font=self.fontLayout,
                          command=self.Buttonfunc_ReadOldData).pack()

        ###############################################################################################################

        elif self.ButtonLayout == "MainScreen2":
            LecName = self.path.split("/")
            LecName = LecName[-1].split(".")
            tk.Label(self.frame[1], text = "", font = self.fontLayout).pack()
            tk.Label(self.frame[1], text = LecName[0], font = self.fontLayout, fg = "#0000FF").pack()
            self.btn_SelectLecture.pack_forget()
            self.btn_continue = tk.Button(self.frameButtons,
                                          text="Weiter",
                                          width=2 * self.width,
                                          height=self.height,
                                          font=self.fontLayout,
                                          command=self.Buttonfunc_Continue)
            self.btn_continue.pack()
            tk.Button(self.frameButtons,
                      text="Einträge ändern",
                      width=2 * self.width,
                      height=self.height,
                      font=self.fontLayout,
                      command=self.Buttonfunc_ChangeManagement).pack()
            tk.Button(self.frameButtons,
                      text="Weitere Vokabeln aus .TSV hinzufügen",
                      width=2 * self.width,
                      height=self.height,
                      font=self.fontLayout,
                      command=self.Buttonfunc_AddVocables).pack()
            tk.Label(self.frameButtons,
                     text="Deutsch | Spanisch | Kommentar | Fällig Andreas YYYY-MM-DD | Fällig Christa YYYY-MM-DD").pack()
            tk.Button(self.frameButtons,
                      text="Datenbank als .TSV speichern",
                      width=2*self.width,
                      height=self.height,
                      font=self.fontLayout,
                      command=self.Buttonfunc_saveTSV).pack()

        ###############################################################################################################

        elif self.ButtonLayout == "AskVocable":
            self.CheckVocable = tk.Button(self.frameButtons,
                                          text="Eingabe prüfen",
                                          font=self.fontLayout,
                                          width=self.width,
                                          height=self.height,
                                          command=self.Buttonfunc_CheckEntry)
            self.CheckVocable.pack()
            tk.Button(self.frameButtons,
                      text="Session beenden",
                      font=self.fontLayout,
                      width=self.width,
                      height=self.height,
                      command=self.Buttonfunc_EndSession).pack()
            self.root.bind("<Return>", lambda event: self.CheckVocable.invoke())

        ###############################################################################################################

        if self.ButtonLayout == "CheckedVocable":
            if self.mode == "nach Fälligkeit":
                tk.Label(self.frameButtons,
                         text="Erneut fragen in:",
                         font=self.fontLayout,
                         width=self.width,
                         height=self.height).grid(row=1, column=1)
                self.Frame_Buttons_delay = tk.Frame(self.frameButtons,
                                                    width=288,
                                                    height=45)
                self.Frame_Buttons_delay.grid(row=2, column=1)
                intervals = functions.intervals(self.current_vocable, IntervalMatrix, self.user)
                Buttons=[]
                Buttons.append(tk.Button(self.Frame_Buttons_delay,
                                         text="+" + str(intervals[0]) + "Tage",
                                         command=lambda: self.Buttonfunc_AddDelay(intervals[0]),
                                         font=self.fontLayout,
                                         height=self.height))
                Buttons[-1].grid(row=1, column=0)
                Buttons.append(tk.Button(self.Frame_Buttons_delay,
                                         text="+" + str(intervals[1]) + "Tage",
                                         command=lambda: self.Buttonfunc_AddDelay(intervals[1]),
                                         font=self.fontLayout,
                                         height=self.height))
                Buttons[-1].grid(row=1, column=1)
                Buttons.append(tk.Button(self.Frame_Buttons_delay,
                                         text="+" + str(intervals[2]) + "Tage",
                                         command=lambda: self.Buttonfunc_AddDelay(intervals[2]),
                                         font=self.fontLayout,
                                         height=self.height))
                Buttons[-1].grid(row=1, column=2)
                self.root.bind("<Return>", lambda event: Buttons[0].invoke())
            elif self.mode == "nach Reihenfolge":
                self.btn_NextVocable = tk.Button(self.frameButtons,
                                                 text="Nächste Vokabel",
                                                 command=lambda: self.Buttonfunc_AddDelay(-1),
                                                 font=self.fontLayout,
                                                 height=self.height,
                                                 width=self.width)
                self.btn_NextVocable.grid(row=1, column=1)
                self.root.bind("<Return>",lambda event: self.btn_NextVocable.invoke())
            self.btn_Tippfehler = tk.Button(self.frameButtons,
                                            text="Tippfehler",
                                            font=self.fontLayout,
                                            width=self.width,
                                            height=self.height,
                                            command=self.Buttonfunc_Tippfehler)
            self.btn_Tippfehler.grid(row=3, column=1)

        ###############################################################################################################

        elif self.ButtonLayout == "EndSession":
            if "Falsch" in self.user_answers:
                tk.Button(self.frameButtons,
                          text="Falsche Antworten wiederholen",
                          font=self.fontLayout,
                          width=2 * self.width,
                          height=self.height,
                          command=self.Buttonfunc_Repeat_Wrong_Answers).grid(row=3, column=2)
            tk.Button(self.frameButtons,
                      text="Speichern & Neustarten",
                      font=self.fontLayout,
                      width=2 * self.width,
                      height=self.height,
                      command=self.Buttonfunc_Save_Restart).grid(row=4, column=2)
            tk.Button(self.frameButtons,
                      text="Speichern & Beenden",
                      font=self.fontLayout,
                      width=2 * self.width,
                      height=self.height,
                      command=self.Buttonfunc_Save_Exit).grid(row=5, column=2)
            self.root.unbind("<Return>")


    def AddLabel(self, parent, text):
        """ More compact way to add labels """
        tk.Label(parent,
                 text=text,
                 font=self.fontLayout).pack(anchor="w", ipadx=10)

    def AddRadioButtons(self, optionlist, parent, variable):
        """ More compact way to add a list of radio buttons to choose from """
        RadioBtnsContents = []
        for option in optionlist:
            RadioBtnsContents.append(
                tk.Radiobutton(parent, text=option, variable=variable, value=option))
            RadioBtnsContents[-1].config(font=self.fontLayout)
            RadioBtnsContents[-1].pack(side='top', anchor='w', ipadx=30)

    def Buttonfunc_AddDelay(self, delay):
        """ Used in Vocable Questionare. In modus 'Nach Fälligkeit' a delay is set after every answer. """
        logger.debug('Adding a new Interval of ' + str(delay) + ' days')
        self.current_vocable.AddDelay(self.user, delay, self.mode, self.path)
        if len(self.user_answers) >= self.MaxNumVocables:
            self.Buttonfunc_EndSession()
        else:
            self.Buttonfunc_NextVocable()

    def Buttonfunc_AddVocables(self):
        """ Used to add additional vocables from a tsv to a DB file """
        logger.info("Adding vocables from tsv file")
        self.path, self.vocables, self.Selector = functions.LoadData(self.path, self.Selector)
        self.vocables = functions.AddVocables(self.vocables, self.path_AddVocables, self.path)
        self.path, self.vocables, self.Selector = functions.LoadData(self.path, C_selection.C_selection)

    def Buttonfunc_ChangeManagement(self):
        """ Starts the ChangeManagement, hence allowing to search and change vocable entries within current DB """
        logger.info("Entering ChangeManagement")
        self.path, self.vocables, self.Selector = functions.LoadData(self.path, self.Selector)
        self.SearchResults = CM()
        for widget in self.frameButtons.winfo_children():
            widget.destroy()
        for widget in self.frame[0].winfo_children():
            widget.destroy()
        for widget in self.frame[1].winfo_children():
            widget.destroy()
        # building labels and entry fields for the left side of the GUI:
        tk.Label(self.frame[0],
                 text="SUCHE:",
                 font=self.fontLayout).grid(row=1, column=1)
        i = 0
        SearchEntries=[]
        Attributes = ["Deutsch:", "Spanisch:", "Kommentar:"]
        for item in Attributes:
            i += 1
            tk.Label(self.frame[0], text=item, font=self.fontLayout, anchor="w").grid(row=i+1, column=1, sticky="W")
            SearchEntries.append(tk.Entry(self.frame[0], font=self.fontLayout))
            SearchEntries[-1].grid(row=i+1, column=2)
        tk.Label(self.frame[1], text="Gefunden:").grid(row=1, column=1)
        # building labels and entry fields for the right side of the GUI:
        i = 0
        self.FoundEntries=[]
        for item in Attributes:
            i += 1
            tk.Label(self.frame[1], text=item, font=self.fontLayout, anchor="w").grid(row=i*2, column=1, sticky="W")
            self.FoundEntries.append(tk.Entry(self.frame[1], font=self.fontLayout, width=30))
            self.FoundEntries[-1].grid(row=2*i+1, column=1, columnspan=2)
        tk.Button(self.frame[1],
                  text="Nächstes",
                  font=self.fontLayout,
                  command= lambda: self.Buttonfunc_CM_next(self.FoundEntries)).grid(row=8,column=2, sticky="W")
        tk.Button(self.frame[1],
                  text="Vorheriges",
                  font=self.fontLayout,
                  command= lambda: self.Buttonfunc_CM_previous(self.FoundEntries)).grid(row=8,column=1, sticky="E")
        tk.Button(self.frame[1],
                  text="Speichern",
                  font=self.fontLayout,
                  command=lambda: self.Buttonfunc_CM_save(self.FoundEntries)).grid(row=9,column=1,columnspan=2)
        self.btn_search = tk.Button(self.frame[0],
                                    text="Suchen",
                                    font=self.fontLayout,
                                    command=lambda: self.Buttonfunc_CM_search(SearchEntries[0].get(),
                                                                              SearchEntries[1].get(),
                                                                              SearchEntries[2].get(),
                                                                              self.FoundEntries))
        self.btn_search.grid(row=5,column=1,columnspan=2)
        self.btn_delete=[]
        self.btn_delete.append(tk.Button(self.frame[1],
                                         text="Vokabel löschen",
                                         font=self.fontLayout,
                                         command=self.Buttonfunc_CM_delete1))
        self.btn_delete.append(tk.Button(self.frame[1],
                                         text="Wirklich löschen",
                                         font=self.fontLayout,
                                         command= lambda: self.Buttonfunc_CM_delete2(self.FoundEntries)))
        self.btn_delete.append(tk.Label(self.frame[1],
                                        text=" ",
                                        font=self.fontLayout))
        self.btn_delete[0].grid(row=10,column=1,columnspan=2)
        self.ButtonLayout = "MainScreen"
        tk.Button(self.frameButtons,
                  text="Zurück zum Hauptmenü",
                  font=self.fontLayout,
                  command=self.Create_Buttons).pack()

    def Buttonfunc_CM_next(self, ResultFields):
        """ Show next results in ChangeManagement menu """
        self.SearchResults.next()
        self.CM_refreshResults(ResultFields)

    def Buttonfunc_CM_previous(self, ResultFields):
        """ Show previous results in ChangeManagement menu """
        self.SearchResults.previous()
        self.CM_refreshResults(ResultFields)

    def Buttonfunc_CM_save(self, ResultFields):
        """ Save the Changes made to the current search result during ChangeManagement """
        self.SearchResults.ChangedEntries(ResultFields[0].get(),
                                          ResultFields[1].get(),
                                          ResultFields[2].get(),
                                          self.path)
        for field in ResultFields:
            field.delete(0, "end")

    def Buttonfunc_CM_delete1(self):
        """ Button to delete current search result from DB. Will require a second button press to actually delete. """
        self.btn_delete[0].grid_forget()
        self.btn_delete[2].grid(row=10,column=1,columnspan=2)
        self.btn_delete[1].grid(row=11,column=1,columnspan=2)

    def Buttonfunc_CM_delete2(self, ResultFields):
        """ Second instance of delete button during ChangeManagement. """
        self.btn_delete[1].grid_forget()
        self.btn_delete[2].grid_forget()
        self.btn_delete[0].grid(row=10,column=1,columnspan=2)
        db = Database(self.path)
        db.delete_vocable(self.SearchResults.OrigEntires[self.SearchResults.idx]["vocID"])
        self.btn_search.invoke()

    def Buttonfunc_CM_search(self, deutsch, spanisch, kommentar, ResultFields):
        """ Takes the Entries made on the left side of the GUI and searches the DB for corresponding entries in the
            vocables table.
        Results are sent to 'self.CM_refreshResults' for proper display on the right side of the GUI """
        self.SearchResults.Search(deutsch, spanisch, kommentar, self.path)
        if len(self.SearchResults.IDs) == 0:
            tk.Label(self.frame[1],
                     text="Eintrag nicht gefunden",
                     anchor="w",
                     fg="RED").grid(row=1, column=1,columnspan=2, sticky="W")
            logger.warning("User has been searching for non-existing vocable, with keys deutsch: '"
                           + deutsch + "', spanisch: '" + spanisch + "', kommentar: '" + kommentar + "'")
            for field in ResultFields:
                field.delete(0, "end")
        self.CM_refreshResults(ResultFields)

    def CM_refreshResults(self, ResultFields):
        """ Manages the display of search results on the right side of the GUI during ChangeManagement """
        if len(self.SearchResults.IDs) > 0:
            logger.info("Refreshing Results in Change Management, showing vocID: "
                        + str(self.SearchResults.OrigEntires[self.SearchResults.idx]["vocID"]))
            for field in ResultFields:
                field.delete(0, "end")

            ResultFields[0].insert(0, self.SearchResults.OrigEntires[self.SearchResults.idx]["deutsch"])
            ResultFields[1].insert(0, self.SearchResults.OrigEntires[self.SearchResults.idx]["spanisch"])
            ResultFields[2].insert(0, self.SearchResults.OrigEntires[self.SearchResults.idx]["kommentar"])

    def Buttonfunc_CheckEntry(self):
        """ During Questionare of vocables, this button functions checks answers of the user for correctness """
        logger.info("Checking vocable with vocID: " + str(self.current_vocable.content['vocID']))
        label_colors, correctness, self.answer_datetime = functions.CheckEntry(self.ET_Answer,
                                                                               self.current_vocable,
                                                                               self.requested,
                                                                               self.user,
                                                                               self.Selector,
                                                                               self.path,
                                                                               self.mode)
        self.user_answers.append(correctness)
        self.user_answers_idx.append(self.Selector.idx)
        # show correct answers as label in green, wrong answers show the correct word in red:
        for request, color in zip(self.requested, label_colors):
            tk.Label(self.frame[1],
                     text=request,
                     font=self.fontLayout,
                     fg=color).pack()
        self.Create_Buttons("CheckedVocable")

    def Buttonfunc_Continue(self):
        """ At the main screen, after selection all radio buttons, this button function will start the questionare """
        for error in self.RadioBtns["errors"]:
            error.pack_forget()
        errors = 0
        if self.RadioBtns["user selection"].get() == "x":
            self.RadioBtns["errors"].append(tk.Label(self.frame[1], text="Bitte Benutzer auswählen!", fg="RED"))
            self.RadioBtns["errors"][-1].pack(anchor = "w")
            errors = 1
        else:
            self.user=self.RadioBtns["user selection"].get()
            self.path, self.vocables, self.Selector = functions.LoadData(self.path,
                                                                         C_selection.C_selection(),
                                                                         user=self.user)

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
                self.RadioBtns["errors"].append(tk.Label(self.frame[1],
                                                         text="Keine Vokabeln für heute fällig!",
                                                         fg="RED"))
                self.RadioBtns["errors"][-1].pack(anchor="w")
                errors = 1
        if errors == 0:
            logger.info("Running user: " + self.user + " in languagemode "
                        + str(self.languagemode) + " in mode " + self.mode)
            self.Buttonfunc_NextVocable()
        else:
            logger.warning("At least on Selection in Startscreen was not done properly")

    def Buttonfunc_EndSession(self):
        """ This exists the questionare and shows result statistics in the GUI
        The function is either called when all due vocables have been answered or prematurely as the corresponding
            button gets pressed during questionare"""
        logger.info('Finishing the session')
        self.user_answers_NumVocables, corrects, falses, self.user_answers_total = \
            functions.EndSession(self.user_answers, self.user_answers_NumVocables, self.user_answers_total)
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
        """ After checking an answer and at the beginning of the questionare, this button function prepares vocable
            information to be displayed in the GUI --> german, spanish and comment contents """
        logger.info("Continuing to Questionare of Vocables")
        self.presented, self.requested, self.kommentar, self.MaxNumVocables, self.current_vocable = \
            functions.NextVocable(self.Selector,
                                  self.mode,
                                  self.path,
                                  self.user,
                                  self.languagemode,
                                  self.vocables,
                                  self.MaxNumVocables)
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
            self.label_presented.append(tk.Label(self.frame[0],
                                                 font=self.fontLayout,
                                                 text=word))
            self.label_presented[-1].pack()
        tk.Label(self.frame[0],
                 font=self.fontLayout,
                 text="").pack() #just leave an empty line
        if self.kommentar != "":
            tk.Label(self.frame[0],
                     font=self.fontLayout + (" bold",),
                     text="Kommentar: " + self.kommentar).pack()
        tk.Label(self.frame[0],
                 font=self.fontLayout,
                 text="Dies ist Vokabel " + str(1 + len(self.user_answers)) + "/"
                      + str(self.MaxNumVocables) + " der Session").pack()
        if self.Selector.listID == 0: # Abfragen nach Reihenfolge
            tk.Label(self.frame[0],
                     font=self.fontLayout,
                     text="bzw. " + str(self.current_vocable.content["vocID"]) + "/" + str(
                         len(self.Selector.Entities[self.Selector.listID])) + " der Datenbank").pack()
        self.Create_Buttons("AskVocable")

    def Buttonfunc_LoadData(self):
        """ selects and loads the desired database when pressing the button at the start of the program """
        if self.path == "" and not self.testmode:
            self.path = filedialog.askopenfilename()
        elif self.testmode:
            self.path = os.path.dirname(os.path.abspath(__file__)) + "\Testdata.json"
        logger.info('Loading File: ' + self.path)
        self.Create_Buttons("MainScreen2")

    def Buttonfunc_Repeat_Wrong_Answers(self):
        """ After finishing a session of questionare, this function can be called by the corresponding button to
            start another questinare only asking those vocables, that have been answered incorrectly during the last
            session """
        logger.info('Repeating wrong answers')
        self.path, self.vocables, unnecessary = functions.LoadData(self.path, C_selection.C_selection(), user=self.user)
        self.user_answers, self.user_answers_idx, self.Selector, self.MaxNumVocables = \
            functions.Repeat_Wrong_Answers(self.user_answers,
                                           self.user_answers_idx,
                                           self.Selector)
        self.Buttonfunc_NextVocable()
        self.Create_Buttons("AskVocable")

    def Buttonfunc_Save_Exit(self):
        """ Button function to save all results and Exit the program """
        functions.saving(self.path, self.vocables)
        self.root.destroy()

    def Buttonfunc_Save_Restart(self):
        """ Button function to restart the program using the previously selected DB"""
        functions.saving(self.path, self.vocables)
        self.restart = 1
        self.root.destroy()

    def Buttonfunc_saveTSV(self):
        """ Button function available after selection a DB to export the vocables table as TSV-file """
        logger.info("Exporting file " + self.path + " as TSV file")
        self.path, self.vocables, self.Selector = functions.LoadData(self.path, self.Selector)
        [file_no_extension, waste] = self.path.split(".")
        if os.path.isfile(file_no_extension + "_export.tsv"):
            logger.warning("TSV Export to file that already exists ("
                           + file_no_extension
                           + ") no action taken to not override current file!")
        else:
            functions.saveTSV(self.vocables, file_no_extension + "_export.tsv")

    def Buttonfunc_Tippfehler(self):
        """ Button function after answered a vocable during questionare. After Checking the answer, even wrong answers
            will be saved as correct to the user's answer table in the DB if this button is pressed. """
        logger.info("Pressed Tippfehler for vocID " + str(self.Selector.idx))
        db = Database(self.path)
        db.set_answer_Tippfehler(self.user, self.answer_datetime)
        self.btn_Tippfehler.destroy()


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
