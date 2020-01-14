import tkinter as tk
from tkinter import filedialog
import json
from datetime import datetime as dt
import os as os



class C_vocables:
    def __init__(self,vocables):
        self.vocables = vocables

    def vocable(self,presented,requested):
        self.presented = presented
        self.requested = requested

    def CheckEntry(self,idx):
        RecentAnswer=[]
        for id in range(len(MyGUI.ET_Answer)):
            RecentAnswer.append(MyGUI.ET_Answer[id].get())
        CorrectInstance2 = 0
        for id in range(len(MyGUI.ET_Answer)): #second loop here because all answers have to be saved to cross-check answer
            CorrectInstance = 0
            for id2 in range(len(MyGUI.ET_Answer)):
                if RecentAnswer[id2] == self.requested[id]:
                    label=tk.Label(MyGUI.frame[1],text=self.requested[id],fg="#50AA50",font = MyGUI.fontLayout).pack()
                    CorrectInstance=1
                    CorrectInstance2 +=1
            if CorrectInstance==0:
                label = tk.Label(MyGUI.frame[1], text=self.requested[id], fg="#FF0000",
                                 font=MyGUI.fontLayout).pack()
        if MyGUI.user != "":
            self.EnterResults(RecentAnswer,CorrectInstance2,MyGUI.user,idx)

    def EnterResults(self,RecentAnswer,CorrectInstance2,user,id):
        print(id)
        if user in self.vocables[id]["answers"]:
            print("user exists")
        else:
            self.vocables[id]["answers"][user]={}
            self.vocables[id]["answers"][user]["datetime"]=[]
            self.vocables[id]["answers"][user]["answer"]=[]
            self.vocables[id]["answers"][user]["delay"]=[]
            self.vocables[id]["answers"][user]["correctness"]=[]
            print(self.vocables[id]["answers"][user])
        self.vocables[id]["answers"][user]["datetime"].append(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.vocables[id]["answers"][user]["answer"].append(RecentAnswer)
        self.vocables[id]["answers"][user]["delay"].append("")
        if CorrectInstance2 == len(RecentAnswer):
            self.vocables[id]["answers"][user]["correctness"].append("Richtig")
            if user==MyGUI.user:
                MyGUI.user_answers.append("Richtig")
            elif user==MyGUI.user2:
                MyGUI.user2_answers.append("Richtig")
        elif CorrectInstance2 == 0:
            self.vocables[id]["answers"][user]["correctness"].append("Falsch")
            if user==MyGUI.user:
                MyGUI.user_answers.append("Falsch")
            elif user==MyGUI.user2:
                MyGUI.user2_answers.append("Falsch")



class GUI_control:
    def __init__(self):
        self.root = tk.Tk(className=" Nehls'scher Vokabeltrainer")
        self.canvas = tk.Canvas(self.root, height=500, width=900)
        self.canvas.pack()
        self.frame=[]
        self.frame.append(tk.Frame(self.root))
        self.frame[0].place(relwidth=0.5, height=300)
        self.frame.append(tk.Frame(self.root))
        self.frame[1].place(relwidth=0.5, height=300, relx=0.5)
        self.frameButtons = tk.Frame(self.root)
        self.frameButtons.place(relwidth = 1, height = 160, rely = 300/(300+160))
        self.ET_Answer=[]
        self.fontLayout=("Helvetica", "18")
        self.languagemode=1
        self.ButtonLayout = 2
        self.path=""
        self.user = ""
        self.user2 = ""
        self.user_answers=[]
        self.user2_answers=[]
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
            tk.Button(self.frameButtons, text='Nächste Vokabel', font=self.fontLayout, width=self.width, height=self.height,
                                         command=self.Buttonfunc_NextVocable).grid(row=2, column=2)
            tk.Button(self.frameButtons, text="Spanisch <--> Deutsch", font=self.fontLayout, width=self.width, height = self.height,
                                          command=self.Buttonfunc_SwitchLanguage).grid(row = 3, column = 2)
            tk.Button(self.frameButtons, text="Session beenden", font=self.fontLayout, width=self.width, height = self.height,
                                          command=self.Buttonfunc_EndSession).grid(row = 4, column = 2)
            if self.user2 != "":
                tk.Label(self.frameButtons, text="Beisizer Ergebnis:").grid(row=1, column=1)
                self.Beisitzer_correct=tk.Button(self.frameButtons, text="Richtig", font=self.fontLayout, width=self.width, height = self.height,
                                              command=self.Buttonfunc_Beisizer_correct)
                self.Beisitzer_correct.grid(row=2, column = 1)
                self.Beisitzer_wrong=tk.Button(self.frameButtons, text="Falsch", font=self.fontLayout, width=self.width, height = self.height,
                                              command=self.Buttonfunc_Beisizer_wrong)
                self.Beisitzer_wrong.grid(row=3, column = 1)
            tk.Label(self.frameButtons, text="Eingabe rückgängig machen:", font=self.fontLayout).grid(row=1, column=3)
            self.Button_RemoveUserEntry = tk.Button(self.frameButtons, text="Vertippt (" + self.user + ")",
                                                    font=self.fontLayout, width=self.width, height=self.height,
                                                    command=self.Buttonfunc_RemoveUserEntry)
            self.Button_RemoveUserEntry.grid(row=2, column=3)
        elif self.ButtonLayout == 1:
            self.CheckVocable = tk.Button(MyGUI.frameButtons, text="Eingabe prüfen", font=self.fontLayout,
                                          command=MyGUI.Buttonfunc_CheckEntry)
            self.CheckVocable.pack()
            self.ButtonLayout = 0
        elif self.ButtonLayout == 2:
            self.SelectLecture = tk.Button(MyGUI.frameButtons, text="Lektion auswählen", font=self.fontLayout,
                                          command=MyGUI.Buttonfunc_SelectLecture)
            self.SelectLecture.pack()
            self.ButtonLayout = 3
        elif self.ButtonLayout == 3:
            tk.Button(MyGUI.frameButtons, text="Andreas", font=self.fontLayout,
                                          command=MyGUI.Buttonfunc_user1).pack()
            tk.Button(MyGUI.frameButtons, text="Christa", font=self.fontLayout,
                                          command=MyGUI.Buttonfunc_user2).pack()
            tk.Button(MyGUI.frameButtons, text="Tester", font=self.fontLayout,
                                          command=MyGUI.Buttonfunc_user3).pack()
            tk.Button(MyGUI.frameButtons, text="Kein Benutzer", font=self.fontLayout,
                                          command=MyGUI.Buttonfunc_user4).pack()
            self.ButtonLayout = 4
        elif self.ButtonLayout == 4:
            if self.user == "":
                self.ButtonLayout = 0
                self.Buttonfunc_NextVocable()
                self.Create_Buttons()
            else:
                tk.Label(MyGUI.frame[1], text="Mit Beisitzer?", font=("Helvetica", "30")).pack()
                if self.user != "Andreas":
                    tk.Button(MyGUI.frameButtons, text="Andreas", font=self.fontLayout,
                                              command=MyGUI.Buttonfunc_user1).pack()
                if self.user != "Christa":
                    tk.Button(MyGUI.frameButtons, text="Christa", font=self.fontLayout,
                                              command=MyGUI.Buttonfunc_user2).pack()
                if self.user != "Tester":
                    tk.Button(MyGUI.frameButtons, text="Tester", font=self.fontLayout,
                                              command=MyGUI.Buttonfunc_user3).pack()
                tk.Button(MyGUI.frameButtons, text="Kein Benutzer", font=self.fontLayout,
                                              command=MyGUI.Buttonfunc_user4).pack()
                self.ButtonLayout = 0
        elif self.ButtonLayout == 5:
            tk.Button(self.frameButtons, text="Speichern & Beenden", font=self.fontLayout, width=self.width, height = self.height,
                                          command=self.Buttonfunc_Save_Exit).grid(row = 4, column = 2)

    def Buttonfunc_RemoveUserEntry(self):
        del MyGUI.user_answers[-1]
        del vocables.vocables[Selector.idx]["answers"][MyGUI.user]["datetime"][-1]
        del vocables.vocables[Selector.idx]["answers"][MyGUI.user]["answer"][-1]
        del vocables.vocables[Selector.idx]["answers"][MyGUI.user]["correctness"][-1]
        del vocables.vocables[Selector.idx]["answers"][MyGUI.user]["delay"][-1]
        self.Button_RemoveUserEntry.destroy()
    def Buttonfunc_RemoveUser2Entry(self):
        del MyGUI.user2_answers[-1]
        del vocables.vocables[Selector.idx]["answers"][MyGUI.user2]["datetime"][-1]
        del vocables.vocables[Selector.idx]["answers"][MyGUI.user2]["answer"][-1]
        del vocables.vocables[Selector.idx]["answers"][MyGUI.user2]["correctness"][-1]
        del vocables.vocables[Selector.idx]["answers"][MyGUI.user2]["delay"][-1]
        self.Button_RemoveUser2Entry.destroy()
        self.Beisitzer_correct=tk.Button(self.frameButtons, text="Richtig", font=self.fontLayout, width=self.width, height = self.height,
                                      command=self.Buttonfunc_Beisizer_correct)
        self.Beisitzer_correct.grid(row=2, column = 1)
        self.Beisitzer_wrong=tk.Button(self.frameButtons, text="Falsch", font=self.fontLayout, width=self.width, height = self.height,
                                      command=self.Buttonfunc_Beisizer_wrong)
        self.Beisitzer_wrong.grid(row=3, column = 1)

    def Buttonfunc_user1(self):
        if self.user == "":
            self.user="Andreas"
        elif self.user2 == "":
            self.user2="Andreas"
            self.Buttonfunc_NextVocable()
        self.Create_Buttons()
    def Buttonfunc_user2(self):
        if self.user == "":
            self.user = "Christa"
        elif self.user2 == "":
            self.user2 = "Christa"
            self.Buttonfunc_NextVocable()
        self.Create_Buttons()
    def Buttonfunc_user3(self):
        if self.user == "":
            self.user = "Tester"
        elif self.user2 == "":
            self.user2 = "Tester"
            self.Buttonfunc_NextVocable()
        self.Create_Buttons()
    def Buttonfunc_user4(self):
        if self.ButtonLayout == 0:
            self.Buttonfunc_NextVocable()
        self.Create_Buttons()
    def Buttonfunc_Beisizer_correct(self):
        vocables.EnterResults(["__Als Beisitzer__"],1,MyGUI.user2,Selector.idx)
        self.Beisitzer_correct.destroy()
        self.Beisitzer_wrong.destroy()
        self.Button_RemoveUser2Entry = tk.Button(self.frameButtons, text="Verklickt (" + self.user2 + ")",
                                                font=self.fontLayout, width=self.width, height=self.height,
                                                command=self.Buttonfunc_RemoveUser2Entry)
        self.Button_RemoveUser2Entry.grid(row=2, column=1)
    def Buttonfunc_Beisizer_wrong(self):
        vocables.EnterResults(["__Als Beisitzer__"],0,MyGUI.user2,Selector.idx)
        self.Beisitzer_correct.destroy()
        self.Beisitzer_wrong.destroy()
        self.Button_RemoveUser2Entry = tk.Button(self.frameButtons, text="Verklickt (" + self.user2 + ")",
                                                font=self.fontLayout, width=self.width, height=self.height,
                                                command=self.Buttonfunc_RemoveUser2Entry)
        self.Button_RemoveUser2Entry.grid(row=2, column=1)

    def Buttonfunc_CheckEntry(self):
        vocables.CheckEntry(Selector.idx)
        print(Selector.idx)
        self.Create_Buttons()

    def Buttonfunc_NextVocable(self):
        for widget in MyGUI.frame[1].winfo_children():
            widget.destroy()
        Selector.NextEntity()
        if self.languagemode==0:
            vocables.vocable(vocables.vocables[Selector.idx].get("deutsch"),vocables.vocables[Selector.idx].get("spanisch"))
        elif self.languagemode==1:
            vocables.vocable(vocables.vocables[Selector.idx].get("spanisch"),
                             vocables.vocables[Selector.idx].get("deutsch"))
        MyGUI.ET_Answer=[]
        for id in range(len(vocables.requested)):
            MyGUI.ET_Answer.append(tk.Entry(MyGUI.frame[1],font = MyGUI.fontLayout))
            MyGUI.ET_Answer[id].pack()
        for widget in MyGUI.frame[0].winfo_children():
            widget.destroy()
        for word in vocables.presented:
            label = tk.Label(MyGUI.frame[0],font = MyGUI.fontLayout, text=word)
            label.pack()
        self.Create_Buttons()

    def Buttonfunc_SelectLecture(self):
        # select vocabulary file and open it
        # .txt files can be parsed to a new json library and will be saved by the
        # program as json file
        # if shut properly if a json file with the same name as a txt exists in the same folder,
        # the json will be loaded to prevent resetting of the json
        self.path = filedialog.askopenfilename()
        if self.path[-3:] == "txt":
            if os.path.isfile(self.path[:-3]+"json"):
                with open(self.path[:-3]+"json") as json_file:
                    vocables.vocables = json.load(json_file)
            else:
                vocables.vocables = ParseTxt_toDicts(self.path)
                vocables.vocables[0]["last_stop"]=0
        elif self.path[-4:] == "json":
            with open(self.path) as json_file:
                vocables.vocables = json.load(json_file)
                #print(vocables.vocables)
        Selector.NumberOfEnteties(len(vocables.vocables))
        Selector.idx=vocables.vocables[0]["last_stop"]
        self.Create_Buttons()

    def Buttonfunc_SwitchLanguage(self):
        if self.languagemode==1:
            self.languagemode=0
        elif self.languagemode==0:
            self.languagemode=1

    def Buttonfunc_EndSession(self):
        for widget in MyGUI.frame[1].winfo_children():
            widget.destroy()
        for widget in MyGUI.frame[0].winfo_children():
            widget.destroy()
        tk.Label(self.frame[0],text=str(self.user) + "," ,font=("Helvetica",30)).pack()
        tk.Label(self.frame[0],text="du hast in dieser Session insgesamt ").pack()
        tk.Label(self.frame[0],text=str(len(MyGUI.user_answers)),font=("Helvetica",30)).pack()
        tk.Label(self.frame[0],text=" Vokabeln beantwortet!").pack()
        tk.Label(self.frame[0],text="Davon waren:").pack()
        tk.Label(self.frame[0],text=str(len([i for i,x in enumerate(MyGUI.user_answers) if x=="Richtig"])) + " richtig und", justify="left", anchor="w").pack()
        tk.Label(self.frame[0],text=str(len([i for i,x in enumerate(MyGUI.user_answers) if x=="Falsch"])) + " falsch").pack()
        if self.user2 != "":
            tk.Label(self.frame[1], text=str(self.user2) + ",", font=("Helvetica", 30)).pack()
            tk.Label(self.frame[1],text="du hast in dieser Session insgesamt ").pack()
            tk.Label(self.frame[1],text=str(len(MyGUI.user2_answers)),font=("Helvetica",30)).pack()
            tk.Label(self.frame[1],text=" Vokabeln beantwortet!").pack()
            tk.Label(self.frame[1], text="Davon waren:").pack()
            tk.Label(self.frame[1],text=str(len([i for i,x in enumerate(MyGUI.user2_answers) if x=="Richtig"])) + " richtig und", justify="left", anchor="w").pack()
            tk.Label(self.frame[1],text=str(len([i for i,x in enumerate(MyGUI.user2_answers) if x=="Falsch"])) + " falsch").pack()
        self.ButtonLayout=5
        self.Create_Buttons()

    def Buttonfunc_Save_Exit(self):
        vocables.vocables[0]["last_stop"]=Selector.idx
        if self.path[-3:] == "txt":
            with open(self.path[:-3] + "json", 'w') as fp:
                json.dump(vocables.vocables, fp, sort_keys=True, indent=4)
        elif self.path[-4:] == "json":
            with open(self.path, 'w') as fp:
                json.dump(vocables.vocables, fp, sort_keys=True, indent=4)
        self.root.destroy()

class C_selection:
    def __init__(self):
        self.idx=-1

    def NumberOfEnteties(self,NumberOfEnteties):
        self.Entities=NumberOfEnteties

    def NextEntity(self):
        self.idx += 1
        if self.idx >= self.Entities:
            self.idx = 0

def ParseTxt_toDicts(path):
    ListOfDicts=[]
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
        ListOfDicts.append({"spanisch" : stringsSpanisch, "deutsch" : stringsDeutsch,
                            "answers" :{}})
    return(ListOfDicts)



MyGUI=GUI_control()
vocables=C_vocables([])
Selector = C_selection()
MyGUI.Create_Buttons()
MyGUI.root.mainloop()

