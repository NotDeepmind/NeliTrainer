import tkinter as tk
from tkinter import filedialog
import json
from datetime import datetime as dt
import datetime as dtt
import os as os

VokabelnProSession = 5


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
        for id in range(
                len(MyGUI.ET_Answer)):  # second loop here because all answers have to be saved to cross-check answer
            CorrectInstance = 0
            for id2 in range(len(MyGUI.ET_Answer)):
                if RecentAnswer[id2] == self.requested[id]:
                    label = tk.Label(MyGUI.frame[1], text=self.requested[id], fg="#50AA50",
                                     font=MyGUI.fontLayout).pack()
                    CorrectInstance = 1
                    CorrectInstance2 += 1
            if CorrectInstance == 0:
                label = tk.Label(MyGUI.frame[1], text=self.requested[id], fg="#FF0000",
                                 font=MyGUI.fontLayout).pack()
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
            if user == MyGUI.user:
                MyGUI.user_answers.append("Richtig")
            elif user == MyGUI.user2:
                MyGUI.user2_answers.append("Richtig")
        elif CorrectInstance2 == 0:
            self.vocables[id]["answers"][user]["correctness"].append("Falsch")
            if user == MyGUI.user:
                MyGUI.user_answers.append("Falsch")
            elif user == MyGUI.user2:
                MyGUI.user2_answers.append("Falsch")

    def NextTime(self, id, user, AddedInterval):
        TimeToAskAgain = dt.today() + dtt.timedelta(days=AddedInterval)
        self.vocables[id]["answers"][user]["NextTime"] = TimeToAskAgain.strftime("%Y-%m-%d")
        self.vocables[id]["answers"][user]["delay"].append(AddedInterval)
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
        self.ButtonLayout = 2
        self.path = ""
        self.user = ""
        self.user2 = ""
        self.user_answers = []
        self.user2_answers = []
        self.width = 20
        self.height = 1

    def Create_Buttons(self):
        for widget in self.frameButtons.winfo_children():
            widget.destroy()
        self.frameButtons.grid_rowconfigure(0, weight=1)
        self.frameButtons.grid_columnconfigure(0, weight=1)
        self.frameButtons.grid_rowconfigure(10, weight=1)
        self.frameButtons.grid_columnconfigure(10, weight=1)
        if self.ButtonLayout == 0:
            self.ButtonLayout = 1
            tk.Label(self.frameButtons, text="Erneut fragen in:", font=self.fontLayout, width=self.width,
                     height=self.height).grid(row=1, column=2)
            # tk.Button(self.frameButtons, text='Nächste Vokabel', font=self.fontLayout, width=self.width, height=self.height,
            #                             command=self.Buttonfunc_NextVocable).grid(row=2, column=2)
            # tk.Button(self.frameButtons, text="Spanisch <--> Deutsch", font=self.fontLayout, width=self.width, height = self.height,
            #                              command=self.Buttonfunc_SwitchLanguage).grid(row = 3, column = 2)

            self.Frame_Buttons_delay = tk.Frame(self.frameButtons, width=288, height=45, bg="RED")
            self.Frame_Buttons_delay.grid(row=2, column=2)
            tk.Button(self.Frame_Buttons_delay, text="1d",
                      command=lambda: vocables.NextTime(Selector.idx, MyGUI.user, 1),
                      font=self.fontLayout, height=self.height).grid(row=0, column=0)
            tk.Button(self.Frame_Buttons_delay, text="3d",
                      command=lambda: vocables.NextTime(Selector.idx, MyGUI.user, 3),
                      font=self.fontLayout, height=self.height).grid(row=0, column=1)
            tk.Button(self.Frame_Buttons_delay, text="7d",
                      command=lambda: vocables.NextTime(Selector.idx, MyGUI.user, 7),
                      font=self.fontLayout, height=self.height).grid(row=0, column=2)
            tk.Button(self.Frame_Buttons_delay, text="30d",
                      command=lambda: vocables.NextTime(Selector.idx, MyGUI.user, 30),
                      font=self.fontLayout, height=self.height).grid(row=0, column=3)
            tk.Button(self.Frame_Buttons_delay, text="180d",
                      command=lambda: vocables.NextTime(Selector.idx, MyGUI.user, 30),
                      font=self.fontLayout, height=self.height).grid(row=0, column=4)

            if self.user2 != "":
                tk.Label(self.frameButtons, text="Beisizer Ergebnis:").grid(row=1, column=1)
                self.Beisitzer_correct = tk.Button(self.frameButtons, text="Richtig", font=self.fontLayout,
                                                   width=self.width, height=self.height,
                                                   command=self.Buttonfunc_Beisizer_correct)
                self.Beisitzer_correct.grid(row=2, column=1)
                self.Beisitzer_wrong = tk.Button(self.frameButtons, text="Falsch", font=self.fontLayout,
                                                 width=self.width, height=self.height,
                                                 command=self.Buttonfunc_Beisizer_wrong)
                self.Beisitzer_wrong.grid(row=3, column=1)
            self.Button_RemoveUserEntry = tk.Button(self.frameButtons, text="Antwort löschen",
                                                    font=self.fontLayout, width=self.width, height=self.height,
                                                    command=self.Buttonfunc_RemoveUserEntry)
            self.Button_RemoveUserEntry.grid(row=3, column=2)
        elif self.ButtonLayout == 1:
            self.CheckVocable = tk.Button(MyGUI.frameButtons, text="Eingabe prüfen", font=self.fontLayout, width=self.width,
                      height=self.height, command=MyGUI.Buttonfunc_CheckEntry)
            self.CheckVocable.pack()
            tk.Button(self.frameButtons, text="Session beenden", font=self.fontLayout, width=self.width,
                      height=self.height,command=self.Buttonfunc_EndSession).pack()
            self.ButtonLayout = 0
            if len(self.user_answers) >= VokabelnProSession:
                self.Buttonfunc_EndSession()
        elif self.ButtonLayout == 2:
            self.SelectLecture = tk.Button(MyGUI.frameButtons, text="Lektion auswählen", font=self.fontLayout,
                                           command=MyGUI.Buttonfunc_SelectLecture)
            self.SelectLecture.pack()
            self.ButtonLayout = 3
        elif self.ButtonLayout == 3:
            tk.Button(MyGUI.frameButtons, text="Andreas", font=self.fontLayout,width=self.width, height=self.height,
                      command=MyGUI.Buttonfunc_user1).pack()
            tk.Button(MyGUI.frameButtons, text="Christa", font=self.fontLayout,width=self.width, height=self.height,
                      command=MyGUI.Buttonfunc_user2).pack()
            tk.Button(MyGUI.frameButtons, text="Tester", font=self.fontLayout,width=self.width, height=self.height,
                      command=MyGUI.Buttonfunc_user3).pack()
            tk.Button(MyGUI.frameButtons, text="Kein Benutzer", font=self.fontLayout,width=self.width, height=self.height,
                      command=MyGUI.Buttonfunc_user4).pack()
            self.ButtonLayout = 4
        elif self.ButtonLayout == 4:
            if self.user == "":
                self.ButtonLayout = 6
                self.Buttonfunc_NextVocable()
                self.Create_Buttons()
            else:
                tk.Label(MyGUI.frame[1], text="Mit Beisitzer?", font=("Helvetica", "30")).pack()
                if self.user != "Andreas":
                    tk.Button(MyGUI.frameButtons, text="Andreas", font=self.fontLayout,width=self.width, height=self.height,
                              command=MyGUI.Buttonfunc_user1).pack()
                if self.user != "Christa":
                    tk.Button(MyGUI.frameButtons, text="Christa", font=self.fontLayout,width=self.width, height=self.height,
                              command=MyGUI.Buttonfunc_user2).pack()
                if self.user != "Tester":
                    tk.Button(MyGUI.frameButtons, text="Tester", font=self.fontLayout,width=self.width, height=self.height,
                              command=MyGUI.Buttonfunc_user3).pack()
                tk.Button(MyGUI.frameButtons, text="Kein Benutzer", font=self.fontLayout,width=self.width, height=self.height,
                          command=MyGUI.Buttonfunc_user4).pack()
                self.ButtonLayout = 6
        elif self.ButtonLayout == 5:
            for i in range(len(self.user_answers)):
                if (self.user_answers[i] == "Falsch"):
                    tk.Button(self.frameButtons, text="Falsche Antworten wiederholen", font=self.fontLayout,
                              width=2 * self.width, height=self.height,
                              command=self.Buttonfunc_Repeat_Wrong_Answers).grid(row=3, column=2)
                    break
            tk.Button(self.frameButtons, text="Speichern & Beenden", font=self.fontLayout, width=2 * self.width,
                      height=self.height,
                      command=self.Buttonfunc_Save_Exit).grid(row=4, column=2)
        elif self.ButtonLayout == 6: #todo hier auswahl der sprache
            tk.Button(MyGUI.frameButtons, text="Vorgabe Deutsch", font=self.fontLayout,width=self.width, height=self.height,
                      command=lambda: self.Buttonfunc_SwitchLanguage(0)).pack()
            tk.Button(MyGUI.frameButtons, text="Vorgabe Spanisch", font=self.fontLayout,width=self.width, height=self.height,
                      command=lambda: self.Buttonfunc_SwitchLanguage(1)).pack()
            tk.Button(MyGUI.frameButtons, text="Vokabeln aus Txt hinzufügen", font=self.fontLayout,width=self.width, height=self.height,
                      command=self.Buttonfunc_AddVocables).pack()
            self.ButtonLayout=0

    def Buttonfunc_RemoveUserEntry(self):
        del MyGUI.user_answers[-1]
        del vocables.vocables[Selector.idx]["answers"][MyGUI.user]["datetime"][-1]
        del vocables.vocables[Selector.idx]["answers"][MyGUI.user]["answer"][-1]
        del vocables.vocables[Selector.idx]["answers"][MyGUI.user]["correctness"][-1]
        self.Button_RemoveUserEntry.destroy()

    def Buttonfunc_RemoveUser2Entry(self):
        del MyGUI.user2_answers[-1]
        del vocables.vocables[Selector.idx]["answers"][MyGUI.user2]["datetime"][-1]
        del vocables.vocables[Selector.idx]["answers"][MyGUI.user2]["answer"][-1]
        del vocables.vocables[Selector.idx]["answers"][MyGUI.user2]["correctness"][-1]
        self.Button_RemoveUser2Entry.destroy()
        self.Beisitzer_correct = tk.Button(self.frameButtons, text="Richtig", font=self.fontLayout, width=self.width,
                                           height=self.height,
                                           command=self.Buttonfunc_Beisizer_correct)
        self.Beisitzer_correct.grid(row=2, column=1)
        self.Beisitzer_wrong = tk.Button(self.frameButtons, text="Falsch", font=self.fontLayout, width=self.width,
                                         height=self.height,
                                         command=self.Buttonfunc_Beisizer_wrong)
        self.Beisitzer_wrong.grid(row=3, column=1)

    def Buttonfunc_user1(self):
        if self.user == "":
            self.user = "Andreas"
            self.Userselection()
        elif self.user2 == "":
            self.user2 = "Andreas"
        self.Create_Buttons()

    def Buttonfunc_user2(self):
        if self.user == "":
            self.user = "Christa"
            self.Userselection()
        elif self.user2 == "":
            self.user2 = "Christa"
        self.Create_Buttons()

    def Buttonfunc_user3(self):
        if self.user == "":
            self.user = "Tester"
            self.Userselection()
        elif self.user2 == "":
            self.user2 = "Tester"
        self.Create_Buttons()

    def Buttonfunc_user4(self):
        self.Create_Buttons()

    def Userselection(self):
        ### Check for due vocables
        if self.user in vocables.vocables[0]:
            Selector.idx = vocables.vocables[0][self.user]["last_stop"]  # continue from last if simplay cycling through
        else:
            vocables.vocables[0][self.user]={}
            vocables.vocables[0][self.user]["last_stop"] = -1
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

    def Buttonfunc_Beisizer_correct(self):
        vocables.EnterResults(["__Als Beisitzer__"], 1, MyGUI.user2, Selector.idx)
        self.Beisitzer_correct.destroy()
        self.Beisitzer_wrong.destroy()
        self.Button_RemoveUser2Entry = tk.Button(self.frameButtons, text="Verklickt (" + self.user2 + ")",
                                                 font=self.fontLayout, width=self.width, height=self.height,
                                                 command=self.Buttonfunc_RemoveUser2Entry)
        self.Button_RemoveUser2Entry.grid(row=2, column=1)

    def Buttonfunc_Beisizer_wrong(self):
        vocables.EnterResults(["__Als Beisitzer__"], 0, MyGUI.user2, Selector.idx)
        self.Beisitzer_correct.destroy()
        self.Beisitzer_wrong.destroy()
        self.Button_RemoveUser2Entry = tk.Button(self.frameButtons, text="Verklickt (" + self.user2 + ")",
                                                 font=self.fontLayout, width=self.width, height=self.height,
                                                 command=self.Buttonfunc_RemoveUser2Entry)
        self.Button_RemoveUser2Entry.grid(row=2, column=1)

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
            MyGUI.ET_Answer[id].pack()
        for widget in MyGUI.frame[0].winfo_children():
            widget.destroy()
        for word in vocables.presented:
            label = tk.Label(MyGUI.frame[0], font=MyGUI.fontLayout, text=word)
            label.pack()
        tk.Label(MyGUI.frame[0], font=MyGUI.fontLayout, text="").pack()
        tk.Label(MyGUI.frame[0], font=MyGUI.fontLayout,
                 text="Dies ist die " + str(1 + len(self.user_answers)) + ". Vokabel").pack()
        if (len(Selector.Entities[1]) - len(self.user_answers) > 0) and (Selector.listID == 1):
            tk.Label(MyGUI.frame[0], font=MyGUI.fontLayout, text="Es gibt noch " + str(
                len(Selector.Entities[1]) - len(self.user_answers)) + " fällige Vokabeln").pack()
        elif Selector.listID > 1:
            tk.Label(MyGUI.frame[0], font=MyGUI.fontLayout, text="Es gibt noch " + str(
                len(Selector.Entities[-1]) - len(self.user_answers)) + " fällige Vokabeln").pack()
        self.Create_Buttons()

    def Buttonfunc_AddVocables(self):
        AddedPath=filedialog.askopenfilename()
        if AddedPath[-3:] != "txt":
            print("Es können nur Txt Dateien hinzugefügt werden (Komma getrennt, Tabstopp getrennt)")
        else:
            NewVocs = ParseTxt_toDicts(AddedPath)
            for item in NewVocs:
                exists = 0
                for olditem in vocables.vocables:
                    if item["spanisch"] == olditem["spanisch"]:
                        exists = 1
                        print(item["spanisch"])
                        print(item["spanisch"][0] + " exists already")
                if exists == 0:
                    vocables.vocables.append(item)
                    print(item["spanisch"][0] + " newly added to the database")

    def Buttonfunc_SelectLecture(self):
        # select vocabulary file and open it
        # .txt files can be parsed to a new json library and will be saved by the
        # program as json file
        # if shut properly if a json file with the same name as a txt exists in the same folder,
        # the json will be loaded to prevent resetting of the json
        self.path = filedialog.askopenfilename()
        if self.path[-3:] == "txt":
            if os.path.isfile(self.path[:-3] + "json"):
                with open(self.path[:-3] + "json", encoding='UTF8') as json_file:
                    vocables.vocables = json.load(json_file)
            else:
                vocables.vocables = ParseTxt_toDicts(self.path)
        elif self.path[-4:] == "json":
            with open(self.path, encoding='UTF8') as json_file:
                vocables.vocables = json.load(json_file)
        Selector.NumbersOfEnteties(range(len(vocables.vocables)))
        self.Create_Buttons()

    def Buttonfunc_SwitchLanguage(self,Language_ID):
        self.languagemode = Language_ID
        self.Buttonfunc_NextVocable()
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
        if self.user2 != "":
            tk.Label(self.frame[1], text=str(self.user2) + ",", font=("Helvetica", 30)).pack()
            tk.Label(self.frame[1], text="du hast in dieser Session insgesamt ").pack()
            tk.Label(self.frame[1], text=str(len(MyGUI.user2_answers)), font=("Helvetica", 30)).pack()
            tk.Label(self.frame[1], text=" Vokabeln beantwortet!").pack()
            tk.Label(self.frame[1], text="Davon waren:").pack()
            tk.Label(self.frame[1],
                     text=str(len([i for i, x in enumerate(MyGUI.user2_answers) if x == "Richtig"])) + " richtig und",
                     justify="left", anchor="w").pack()
            tk.Label(self.frame[1],
                     text=str(len([i for i, x in enumerate(MyGUI.user2_answers) if x == "Falsch"])) + " falsch").pack()
        self.ButtonLayout = 5
        if Selector.listID==0:
            vocables.vocables[0][self.user]["last_stop"] = Selector.idx
        self.Create_Buttons()

    def Buttonfunc_Repeat_Wrong_Answers(self):
        New_Indexes = []
        for i in range(len(self.user_answers)):
            if (self.user_answers[i] == "Falsch") and (i < len(Selector.Entities[1])) and (Selector.listID <= 1):
                New_Indexes.append(Selector.Entities[1][i])
            elif (self.user_answers[i] == "Falsch") and (i >= len(Selector.Entities[1])) and (Selector.listID <= 1):
                i = i - len(Selector.Entities[1]) + vocables.vocables[0][self.user]["last_stop"]
                while i >= len(Selector.Entities[0]):
                    i -= len(Selector.Entities[0])
                New_Indexes.append(Selector.Entities[0][i])
            elif (self.user_answers[i] == "Falsch") and (Selector.listID > 1):
                New_Indexes.append(Selector.Entities[-1][i])
        global VokabelnProSession
        VokabelnProSession=len(New_Indexes)
        Selector.IDs=-1
        Selector.NumbersOfEnteties(New_Indexes)
        self.user_answers=[]
        self.user2_answers=[]
        Selector.listID=len(Selector.Entities)-1
        self.Buttonfunc_NextVocable()
        MyGUI.ButtonLayout = 1
        MyGUI.Create_Buttons()

    def Buttonfunc_Save_Exit(self):
        if self.path[-3:] == "txt":
            with open(self.path[:-3] + "json", 'w', encoding='UTF8') as fp:
                json.dump(vocables.vocables, fp, sort_keys=True, indent=4)
        elif self.path[-4:] == "json":
            with open(self.path, 'w', encoding='UTF8') as fp:
                json.dump(vocables.vocables, fp, sort_keys=True, indent=4)
        self.root.destroy()


class C_selection:
    def __init__(self):
        self.idx = -1
        self.IDs = -1
        self.listID = 1
        self.Entities = []

    def NumbersOfEnteties(self, NumberOfEnteties):
        self.Entities.append(NumberOfEnteties)

    def NextEntity(self):
        self.IDs += 1
        if (self.IDs >= len(self.Entities[self.listID])) and self.listID == 1:
            self.IDs = vocables.vocables[0][MyGUI.user]["last_stop"]
            self.listID = 0
        elif (self.IDs >= len(self.Entities[self.listID])):
            self.IDs = 0
        self.idx = self.Entities[self.listID][self.IDs]


def ParseTxt_toDicts(path):
    ListOfDicts = []
    file = open(path, "r+", encoding='utf-8')
    file_content = file.readlines()
    for id in range(len(file_content)):
        strings = file_content[id].split("\t")
        # format german strings to get single german entries
        stringsDeutsch = strings[0].split(",")
        try:
            stringsDeutsch.remove("2x")
        except ValueError:
            pass
        # format spanish string to get single entries
        stringsSpanisch = strings[1]
        stringsSpanisch = stringsSpanisch.strip().split(
            ",")  # the strip cmd removes trailing \n, which couldn't get removed by other means
        for id2 in range(len(stringsSpanisch)):  # check and add single "a" to previous entry b/c its just declanation
            if stringsSpanisch[id2] == "a":
                stringsSpanisch[id2 - 1] = stringsSpanisch[id2 - 1] + ",a"
        while "a" in stringsSpanisch: stringsSpanisch.remove("a")
        ListOfDicts.append({"spanisch": stringsSpanisch, "deutsch": stringsDeutsch,
                            "answers": {}})
    return (ListOfDicts)


MyGUI = GUI_control()
vocables = C_vocables([])
Selector = C_selection()
MyGUI.Create_Buttons()
MyGUI.root.mainloop()
