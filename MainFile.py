import tkinter as tk
from tkinter import filedialog
import json
from datetime import datetime as dt
import datetime as dtt
import os as os
from ChangeManagement import ChangeManagement

### Um Alte Daten einzulesen, folgende Variable auf 1 setzen:
read_old_data = 0

### Um das JSON File schön zu formatieren, folgende Variable auf 1 setzen.
### (ohne schöne Formatierung lässt sich erheblich Speicherplatz sparen)
nice_JSON = 0

#compile via console in folder containing MainFile.py --> pyinstaller -F MainFile.py

#todo abschlussauswertung am ende --> anzahl der beantwortetetn vokabeln & Anzahl der Antworten zeigen
#todo immer 6 Antwortfelder geben <-- erstmal lassen

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




class C_vocables:
    def __init__(self, vocables):
        self.vocables = vocables

    def vocable(self, presented, requested):
        self.presented = presented
        self.requested = requested

    def CheckEntry(self, idx):
        RecentAnswer = []
        for id in range(len(MyGUI.ET_Answer)):
            RecentAnswer.append(MyGUI.ET_Answer[id].get())
        CorrectInstance2 = 0
        Cheatmode = 0
        for id in range(
                len(MyGUI.ET_Answer)):  # second loop here because all answers have to be saved to cross-check answer
            CorrectInstance = 0
            for id2 in range(len(MyGUI.ET_Answer)):
                if RecentAnswer[id2] == self.requested[id] or RecentAnswer[id2] == "#":
                    label = tk.Label(MyGUI.frame[1], text=self.requested[id], fg="#50AA50",
                                     font=MyGUI.fontLayout).pack()
                    CorrectInstance = 1
                    CorrectInstance2 += 1
            if CorrectInstance == 0:
                label = tk.Label(MyGUI.frame[1], text=self.requested[id], fg="#FF0000",
                                 font=MyGUI.fontLayout).pack()
            if RecentAnswer[id2] == "#":
                Cheatmode = 1
        if Cheatmode == 1:
            CorrectInstance2=len(MyGUI.ET_Answer)
        if MyGUI.user != "":
            self.EnterResults(RecentAnswer, CorrectInstance2, MyGUI.user, idx)

    def EnterResults(self, RecentAnswer, CorrectInstance2, user, id):
        if user in self.vocables[id]["answers"]:
            pass
        else:
            self.vocables[id]["answers"][user] = {}
            self.vocables[id]["answers"][user]["datetime"] = []
            self.vocables[id]["answers"][user]["answer"] = []
            self.vocables[id]["answers"][user]["delay"] = []
            self.vocables[id]["answers"][user]["correctness"] = []
        self.vocables[id]["answers"][user]["datetime"].append(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.vocables[id]["answers"][user]["answer"].append(RecentAnswer)
        if CorrectInstance2 == len(RecentAnswer):
            self.vocables[id]["answers"][user]["correctness"].append("Richtig")
            MyGUI.user_answers.append("Richtig")
            MyGUI.user_answers_idx.append(Selector.idx)
        elif CorrectInstance2 == 0:
            self.vocables[id]["answers"][user]["correctness"].append("Falsch")
            MyGUI.user_answers.append("Falsch")
            MyGUI.user_answers_idx.append(Selector.idx)

    def NextTime(self, id, user, AddedInterval):
        if MyGUI.mode == "nach Fälligkeit":
            TimeToAskAgain = dt.today() + dtt.timedelta(days=AddedInterval)
            self.vocables[id]["answers"][user]["NextTime"] = TimeToAskAgain.strftime("%Y-%m-%d")
            self.vocables[id]["answers"][user]["delay"].append(AddedInterval)
        elif MyGUI.mode == "nach Reihenfolge":
            self.vocables[id]["answers"][user]["delay"].append(-1)
        if len(MyGUI.user_answers) >= MyGUI.MaxNumVocables:
            MyGUI.Buttonfunc_EndSession()
        else:
            MyGUI.Buttonfunc_NextVocable()


class GUI_control:
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
        self.width = 20
        self.height = 1
        self.mode = []
        self.RadioBtns = {}
        self.RadioBtns["errors"]=[]
        self.MaxNumVocables = []

    def Create_Buttons(self):
        for widget in self.frameButtons.winfo_children():
            widget.destroy()
        self.frameButtons.grid_rowconfigure(0, weight=1)
        self.frameButtons.grid_columnconfigure(0, weight=1)
        self.frameButtons.grid_rowconfigure(10, weight=1)
        self.frameButtons.grid_columnconfigure(10, weight=1)
        if self.ButtonLayout == 0:
            self.ButtonLayout = 1
            if self.mode == "nach Fälligkeit":
                tk.Label(self.frameButtons, text="Erneut fragen in:", font=self.fontLayout, width=self.width,
                     height=self.height).grid(row=1, column=2)
                self.Frame_Buttons_delay = tk.Frame(self.frameButtons, width=288, height=45)
                self.Frame_Buttons_delay.grid(row=2, column=2)
                LastDelayList = vocables.vocables[Selector.idx]["answers"][self.user]["delay"]
                LastDelayList.reverse() #reverse once to check from last, because all enties in the "nach Reihenfolge" mode will have a delay of -1 and must be skipped
                LastDelay = []
                for delay in LastDelayList:
                    if delay >= 0:
                        LastDelay = delay
                        break
                for row in IntervalMatrix:
                    if LastDelay >= row[0] and LastDelay <= row[1]:
                        self.IntervalMatrixRow = row #find the right row of the delay matrix
                for id in range(2,5):
                    tk.Button(self.Frame_Buttons_delay, text="+" + str(self.IntervalMatrixRow[id]) + "Tage",
                              command=lambda: vocables.NextTime(Selector.idx, MyGUI.user, self.IntervalMatrixRow[id]),
                              font=self.fontLayout, height=self.height).grid(row=0, column=id-1)
                self.root.bind("<Return>", lambda event: vocables.NextTime(Selector.idx, MyGUI.user, self.IntervalMatrixRow[2]))
                LastDelayList.reverse() #must reverse to again to preserve correct entry

            elif self.mode == "nach Reihenfolge":
                tk.Button(self.frameButtons, text="Nächste Vokabel", command=lambda: vocables.NextTime(Selector.idx, MyGUI.user, 30),
                          font=self.fontLayout, height=self.height, width=self.width).grid(row=0, column=2)
                self.root.bind("<Return>",lambda event: vocables.NextTime(Selector.idx, MyGUI.user, 30))

            self.Button_RemoveUserEntry = tk.Button(self.frameButtons, text="Tippfehler",
                                                    font=self.fontLayout, width=self.width, height=self.height,
                                                    command=self.Buttonfunc_RemoveUserEntry)
            self.Button_RemoveUserEntry.grid(row=3, column=2)

        elif self.ButtonLayout == 1:
            self.CheckVocable = tk.Button(MyGUI.frameButtons, text="Eingabe prüfen", font=self.fontLayout, width=self.width,
                      height=self.height, command=MyGUI.Buttonfunc_CheckEntry)
            self.CheckVocable.pack()
            tk.Button(self.frameButtons, text="Session beenden", font=self.fontLayout, width=self.width,
                      height=self.height,command=self.Buttonfunc_EndSession).pack()
            self.root.bind("<Return>", MyGUI.Buttonfunc_CheckEntry_Hotkey)
            self.ButtonLayout = 0
        elif self.ButtonLayout == "MainScreen":
            for widget in self.frameButtons.winfo_children():
                widget.destroy()
            for widget in self.frame[0].winfo_children():
                widget.destroy()
            for widget in self.frame[1].winfo_children():
                widget.destroy()
            self.RadioBtnsContents=[]
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

            self.SelectLecture = tk.Button(MyGUI.frameButtons, text="Lektion auswählen", font=self.fontLayout,
                                           command=MyGUI.Buttonfunc_SelectLecture)
            self.SelectLecture.pack()
            if read_old_data == 1:
                tk.Button(self.frameButtons, text="Read Old Data (Andreas)", font=self.fontLayout, command=self.Buttonfunc_ReadOldData).pack()
            self.ButtonLayout = 1

        elif self.ButtonLayout == 5:
            for i in range(len(self.user_answers)):
                if (self.user_answers[i] == "Falsch"):
                    tk.Button(self.frameButtons, text="Falsche Antworten wiederholen", font=self.fontLayout,
                              width=2 * self.width, height=self.height,
                              command=self.Buttonfunc_Repeat_Wrong_Answers).grid(row=3, column=2)
                    break
            tk.Button(self.frameButtons, text="Speichern & Neustarten", font=self.fontLayout, width=2 * self.width,
                      height=self.height,
                      command=self.Buttonfunc_Save_Restart).grid(row=4, column=2)
            tk.Button(self.frameButtons, text="Speichern & Beenden", font=self.fontLayout, width=2 * self.width,
                      height=self.height,
                      command=self.Buttonfunc_Save_Exit).grid(row=5, column=2)
            self.root.unbind("<Return>")

    def Buttonfunc_RemoveUserEntry(self):
        MyGUI.user_answers[-1] = "Richtig"
        vocables.vocables[Selector.idx]["answers"][MyGUI.user]["correctness"][-1] = "Richtig"
        self.Button_RemoveUserEntry.destroy()

    def Buttonfunc_Userselection(self,username):
        self.user = username
        ### Check for due vocables
        if self.user in vocables.vocables[0]:
            Selector.idx = vocables.vocables[0][self.user]["last_stop"]  # continue from last if simply cycling through
        else:
            vocables.vocables[0][self.user]={}
            vocables.vocables[0][self.user]["last_stop"] = 0
        List_Due_Vocables = []
        for i in range(len(vocables.vocables)):
            try:
                if dt.today() >= dt.strptime(vocables.vocables[i]["answers"][self.user]["NextTime"], "%Y-%m-%d"):
                    List_Due_Vocables.append(i)
            except:
                pass
        Selector.NumbersOfEnteties(List_Due_Vocables)
        # Selector.IDs=-1
        # Selector.NextEntity()
    def Buttonfunc_CheckEntry_Hotkey(self,event):
        self.Buttonfunc_CheckEntry()

    def Buttonfunc_CheckEntry(self):
        vocables.CheckEntry(Selector.idx)
        self.Create_Buttons()

    def Buttonfunc_NextVocable(self):
        for widget in MyGUI.frame[1].winfo_children():
            widget.destroy()
        Selector.NextEntity()
        if self.languagemode == 0:
            vocables.vocable(vocables.vocables[Selector.idx].get("deutsch"),
                             vocables.vocables[Selector.idx].get("spanisch"))
        elif self.languagemode == 1:
            vocables.vocable(vocables.vocables[Selector.idx].get("spanisch"),
                             vocables.vocables[Selector.idx].get("deutsch"))
        MyGUI.ET_Answer = []
        for id in range(len(vocables.requested)):
            MyGUI.ET_Answer.append(tk.Entry(MyGUI.frame[1], font=MyGUI.fontLayout))
            MyGUI.ET_Answer[-1].pack()
        MyGUI.ET_Answer[0].focus()
        for widget in MyGUI.frame[0].winfo_children():
            widget.destroy()
        for word in vocables.presented:
            label = tk.Label(MyGUI.frame[0], font=MyGUI.fontLayout, text=word)
            label.pack()
        tk.Label(MyGUI.frame[0], font=MyGUI.fontLayout, text="").pack()
        if vocables.vocables[Selector.idx].get("kommentar") != "":
            tk.Label(MyGUI.frame[0], font=MyGUI.fontLayout + (" bold",),
                     text="Kommentar: " + vocables.vocables[Selector.idx].get("kommentar")).pack()
        tk.Label(MyGUI.frame[0], font=MyGUI.fontLayout,
                 text="Dies ist Vokabel " + str(1 + len(self.user_answers)) + "/" + str(self.MaxNumVocables) + " der Session").pack()
        if Selector.listID == 0: # Abfragen nach Reihenfolge
            tk.Label(MyGUI.frame[0], font=MyGUI.fontLayout,
                     text="bzw. " + str(Selector.idx + 1) + "/" + str(
                         len(Selector.Entities[Selector.listID])) + " der Datenbank").pack()
        self.Create_Buttons()

    def Buttonfunc_AddVocables(self):
        AddedPath=filedialog.askopenfilename()
        if AddedPath[-3:] != "txt" and AddedPath[-3:] != "tsv":
            print("Es können nur Txt Dateien hinzugefügt werden (Komma getrennt, Tabstopp getrennt)")
        else:
            NewVocs = ParseTxt_toDicts(AddedPath)
            for item in NewVocs:
                exists = 0
                for olditem in vocables.vocables:
                    if item["deutsch"] == olditem["deutsch"]:
                        exists = 1
                        print(item["deutsch"][0] + " exists already")
                if exists == 0:
                    vocables.vocables.append(item)
                    print(item["deutsch"][0] + " newly added to the database")
            self.Buttonfunc_saving()

    def Buttonfunc_ReadOldData(self):
        self.path = filedialog.askopenfilename()
        if self.path[-3:] == "txt" or self.path[-3:] == "tsv":
            vocables.vocables = InitializeOldData(self.path)
        Selector.NumbersOfEnteties(range(len(vocables.vocables)))
        tk.Button(MyGUI.frameButtons, text="Weiter", font=self.fontLayout,command=MyGUI.Buttonfunc_Continue).pack()

    def Buttonfunc_SelectLecture(self):
        # select vocabulary file and open it
        # .txt files can be parsed to a new json library and will be saved by the
        # program as json file
        # if shut properly if a json file with the same name as a txt exists in the same folder,
        # the json will be loaded to prevent resetting of the json

        self.path = filedialog.askopenfilename()
        if self.path != "":
            if self.path[-3:] == "txt" or self.path[-3:] == "tsv":
                if os.path.isfile(self.path[:-3] + "json"):
                    with open(self.path[:-3] + "json", encoding='UTF8') as json_file:
                        vocables.vocables = json.load(json_file)
                else:
                    vocables.vocables = ParseTxt_toDicts(self.path)
            elif self.path[-4:] == "json":
                with open(self.path, encoding='UTF8') as json_file:
                    vocables.vocables = json.load(json_file)
            Selector.NumbersOfEnteties(range(len(vocables.vocables)))
            self.SelectLecture.pack_forget()
            tk.Button(MyGUI.frameButtons, text="Weiter", width=2*self.width, height=self.height, font=self.fontLayout,command=MyGUI.Buttonfunc_Continue).pack()
            tk.Button(self.frameButtons, text="Einträge ändern", width=2*self.width, height=self.height, font=self.fontLayout,
                      command=self.Buttonfunc_ChangeManagement).pack()
            tk.Button(self.frameButtons, text="Weitere Vokabeln aus .TSV hinzufügen", width=2*self.width, height=self.height, font=self.fontLayout,
                      command=self.Buttonfunc_AddVocables).pack()

    def Buttonfunc_ChangeManagement(self):
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
        FoundEntries=[]
        for item in Attributes:
            i += 1
            tk.Label(self.frame[1], text=item, font=self.fontLayout, anchor="w").grid(row=i*2, column=1, sticky="W")
            FoundEntries.append(tk.Entry(self.frame[1], font=self.fontLayout, width=30))
            FoundEntries[-1].grid(row=2*i+1, column=1, columnspan=2)
        tk.Button(self.frame[1], text="Nächstes", font=self.fontLayout,
                  command= lambda: CM.next(FoundEntries)).grid(row=8,column=2, sticky="W")
        tk.Button(self.frame[1], text="Vorheriges", font=self.fontLayout,
                  command= lambda: CM.previous(FoundEntries)).grid(row=8,column=1, sticky="E")
        tk.Button(self.frame[1], text="Speichern", font=self.fontLayout,
                  command=lambda: self.Buttonfunc_CM_save(FoundEntries)).grid(row=9,column=1,columnspan=2)
        tk.Button(self.frame[0], text="Suchen", font=self.fontLayout,
                  command=lambda: self.Buttonfunc_Suchen(SearchEntries[0].get(),SearchEntries[1].get(),SearchEntries[2].get(),vocables.vocables,FoundEntries)).grid(row=5,column=1,columnspan=2)
        self.ButtonLayout = "MainScreen"
        tk.Button(self.frameButtons, text="Zurück zum Hauptmenü", font=self.fontLayout, command=self.Create_Buttons).pack()
    def Buttonfunc_Suchen(self, deutsch, spanisch, kommentar, vokabeln, FoundEntries):
        CM.AddVokabeln(vokabeln)
        CM.Search(deutsch, spanisch, kommentar)
        if CM.IDs == []:
            tk.Label(self.frame[1], text="Eintrag nicht gefunden", anchor="w", fg="RED").grid(row=1, column=1,columnspan=2, sticky="W")
        elif len(CM.IDs)>1:
            tk.Label(self.frame[1], text=str(len(CM.IDs)) + " Einträge gefunden", anchor="w", fg="RED").grid(row=1, column=1,columnspan=2, sticky="W")
            CM.display(FoundEntries)
    def Buttonfunc_CM_save(self, FoundEntries):
        i=0
        for key in ["deutsch", "spanisch", "kommentar"]:
            content = FoundEntries[i].get().split(",")
            if key != "kommentar":
                for word in content:
                    if len(word) > 0:
                        while word[0] == " ":
                            word = word[1:]
                        while word[-1] == " ":
                            word = word[:-1]
            FoundEntries[i].delete(0, "end")
            i += 1
            vocables.vocables[CM.IDs[CM.idx]][key] = content


    def Buttonfunc_Continue(self):
        for error in self.RadioBtns["errors"]:
            error.pack_forget()
        errors = 0
        if self.RadioBtns["user selection"].get() == "x":
            self.RadioBtns["errors"].append(tk.Label(self.frame[1], text="Bitte Benutzer auswählen!", fg="RED"))
            self.RadioBtns["errors"][-1].pack(anchor = "w")
            errors = 1
        else:
            self.Buttonfunc_Userselection(self.RadioBtns["user selection"].get())

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
            if (len(Selector.Entities[1]) == 0) and (self.RadioBtns["mode"].get() == "nach Fälligkeit"):
                self.RadioBtns["errors"].append(tk.Label(self.frame[1], text="Keine Vokabeln für heute fällig!", fg="RED"))
                self.RadioBtns["errors"][-1].pack(anchor = "w")
                errors = 1

        if errors == 0:
            self.MaxNumVocables = self.MaxNumVocables.get()
            self.Buttonfunc_NextVocable()
            self.ButtonLayout = 1
            self.Create_Buttons()

    def Buttonfunc_EndSession(self):
        for widget in MyGUI.frame[1].winfo_children():
            widget.destroy()
        for widget in MyGUI.frame[0].winfo_children():
            widget.destroy()
        tk.Label(self.frame[0], text=str(self.user) + ",", font=("Helvetica", 30)).pack()
        tk.Label(self.frame[0], text="du hast in dieser Session insgesamt ").pack()
        tk.Label(self.frame[0], text=str(len(MyGUI.user_answers)), font=("Helvetica", 30)).pack()
        tk.Label(self.frame[0], text=" Vokabeln beantwortet!").pack()
        tk.Label(self.frame[0], text="Davon waren:").pack()
        tk.Label(self.frame[0],
                 text=str(len([i for i, x in enumerate(MyGUI.user_answers) if x == "Richtig"])) + " richtig und",
                 justify="left", anchor="w").pack()
        tk.Label(self.frame[0],
                 text=str(len([i for i, x in enumerate(MyGUI.user_answers) if x == "Falsch"])) + " falsch").pack()
        self.ButtonLayout = 5
        if Selector.listID==0:
            vocables.vocables[0][self.user]["last_stop"] = Selector.idx
        self.Create_Buttons()

    def Buttonfunc_Repeat_Wrong_Answers(self):
        New_Indexes = []
        for i in range(len(self.user_answers)):
            if (self.user_answers[i] == "Falsch") and self.mode == "nach Fälligkeit" :
                New_Indexes.append(self.user_answers_idx[i])
            elif (self.user_answers[i] == "Falsch") and self.mode == "nach Reihenfolge":
                New_Indexes.append(self.user_answers_idx[i])
            elif (self.user_answers[i] == "Falsch") and (Selector.listID > 1):
                New_Indexes.append(self.user_answers_idx[i])
        self.MaxNumVocables=len(New_Indexes)
        Selector.IDs=-1
        Selector.NumbersOfEnteties(New_Indexes)
        self.user_answers=[]
        self.user2_answers=[]
        Selector.listID=len(Selector.Entities)-1
        self.Buttonfunc_NextVocable()
        MyGUI.ButtonLayout = 1
        MyGUI.Create_Buttons()

    def Buttonfunc_Save_Restart(self):
        self.Buttonfunc_saving()
        self.restart = True
        self.root.destroy()


    def Buttonfunc_Save_Exit(self):
        self.Buttonfunc_saving()
        self.root.destroy()

    def Buttonfunc_saving(self):
        if self.path[-3:] == "txt" or self.path[-3:] == "tsv":
            with open(self.path[:-3] + "json", 'w', encoding='UTF8') as fp:
                if nice_JSON == 1:
                    json.dump(vocables.vocables, fp, indent=4)
                else:
                    json.dump(vocables.vocables, fp)
        elif self.path[-4:] == "json":
            with open(self.path, 'w', encoding='UTF8') as fp:
                if nice_JSON == 1:
                    json.dump(vocables.vocables, fp, indent=4)
                else:
                    json.dump(vocables.vocables, fp)



class C_selection:
    def __init__(self):
        self.IDs = -1 # das hier ist einfach ein zähler
        self.idx = -1   # das hier ist der entsprechende index nach der korrelationsliste, die in Entities abelegt werden kann/soll
                        # --> Entities[1] enthält die indices der fälligen vokabeln
        self.listID = 1
        self.Entities = []

    def NumbersOfEnteties(self, NumberOfEnteties):
        self.Entities.append(NumberOfEnteties)

    def NextEntity(self):
        self.IDs += 1
        if MyGUI.mode == "nach Reihenfolge" and self.listID == 1:
            self.IDs = vocables.vocables[0][MyGUI.user]["last_stop"]
            self.listID = 0
        if MyGUI.mode == "nach Fälligkeit" and type(MyGUI.MaxNumVocables) != int:
            MyGUI.MaxNumVocables = len(self.Entities[self.listID])
        elif MyGUI.mode == "nach Reihenfolge" and type(MyGUI.MaxNumVocables) != int:
            MyGUI.MaxNumVocables = int(MyGUI.MaxNumVocables)
        if MyGUI.mode == "nach Reihenfolge" and self.IDs >=len(self.Entities[0]):
            self.IDs = 0
        self.idx = self.Entities[self.listID][self.IDs]


def ParseTxt_toDicts(path):
    ListOfDicts = []
    file = open(path, "r+", encoding='utf-8')
    file_content = file.readlines()
    for id in range(len(file_content)):
        strings = file_content[id].split("\t")
        if len(strings) == 3:
            # format german strings to get single german entries
            stringsDeutsch = strings[0].split(",")
            try:
                stringsDeutsch.remove("2x")
            except ValueError:
                pass
            if stringsDeutsch[-1] == "":
                del stringsDeutsch[-1]
            # format spanish string to get single entries
            stringsSpanisch = strings[1]
            stringsSpanisch = stringsSpanisch.strip().split(
                ",")  # the strip cmd removes trailing \n, which couldn't get removed by other means
            for id2 in range(len(stringsSpanisch)):  # check and add single "a" to previous entry b/c its just declanation
                if stringsSpanisch[id2] == "a":
                    stringsSpanisch[id2 - 1] = stringsSpanisch[id2 - 1] + ",a"
            while "a" in stringsSpanisch: stringsSpanisch.remove("a")
            if stringsSpanisch[-1] == "":
                del stringsSpanisch[-1]
            stringsKommentar = strings[2].strip()
            ListOfDicts.append({"spanisch": stringsSpanisch, "deutsch": stringsDeutsch,
                                "answers": {}, "kommentar": stringsKommentar})
        else:
            print("There is an Issue with your .TSV: Number of columns != 3")
    return (ListOfDicts)

def InitializeOldData(path):
    ListOfDicts = []
    file = open(path, "r+", encoding='utf-8')
    file_content = file.readlines()
    for line in file_content:
        strings = line.split("\t")
        stringsDeutsch = strings[0].split(",")
        if stringsDeutsch[-1] == "":
            del stringsDeutsch[-1]
        stringsSpanisch = strings[1].split(",")
        stringsKommentar = strings[2]
        stringsAnswer = []
        for id in range(len(stringsSpanisch)):
            stringsAnswer.append("")
        if stringsSpanisch[-1] == "":
            del stringsSpanisch[-1]
        IntDueA = int(strings[3])
        IntDueA = dt.today() + dtt.timedelta(IntDueA-1629)
        IntDelayA = int(strings[4].strip())
        IntDueC = int(strings[5])
        IntDueC = dt.today() + dtt.timedelta(IntDueC-1629)
        IntDelayC = int(strings[6].strip())

        ListOfDicts.append({
            "spanisch" : stringsSpanisch,
            "deutsch" : stringsDeutsch,
            "kommentar" : stringsKommentar,
            "answers" : {
                "Andreas": {
                    "datetime" :    [""],
                    "answer" :      [stringsAnswer],
                    "delay" :       [IntDelayA],
                    "correctness" : ["Richtig"],
                    "NextTime" :    IntDueA.strftime("%Y-%m-%d")
                },
                "Christa": {
                    "datetime":     [""],
                    "answer":       [stringsAnswer],
                    "delay":        [IntDelayC],
                    "correctness":  ["Richtig"],
                    "NextTime":     IntDueC.strftime("%Y-%m-%d")
                }
            }
        })
        ListOfDicts[0]["Andreas"]={"last_stop": 0}
        ListOfDicts[0]["Christa"]={"last_stop": 0}
    return ListOfDicts





            # self.vocables[id]["answers"][user] = {}
            # self.vocables[id]["answers"][user]["datetime"] = []
            # self.vocables[id]["answers"][user]["answer"] = []
            # self.vocables[id]["answers"][user]["delay"] = []
            # self.vocables[id]["answers"][user]["correctness"] = []
            # vocables.vocables[0][self.user]["last_stop"] = 0


MyGUI = GUI_control()
MyGUI.restart = False
vocables = C_vocables([])
Selector = C_selection()
MyGUI.Create_Buttons()
CM = ChangeManagement()
MyGUI.root.mainloop()
while MyGUI.restart:
    del MyGUI
    del vocables
    del Selector
    MyGUI = GUI_control()
    MyGUI.restart = False
    vocables = C_vocables([])
    Selector = C_selection()
    MyGUI.Create_Buttons()
    MyGUI.root.mainloop()
