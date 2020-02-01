import tkinter as tk
from tkinter import filedialog
import json
import C_vocables, C_selection
from datetime import datetime as dt
import datetime as dtt
import os as os
from ChangeManagement import ChangeManagement





def CheckEntry(Answers, vocable, requested, user):
    RecentAnswer = []
    label_colors = []
    for Answer in Answers:
        RecentAnswer.append(Answer.get())
    CorrectInstance2 = 0
    for request in requested:  # second loop here because all answers have to be saved to cross-check answer
        CorrectInstance = 0
        for Answer in RecentAnswer:
            if Answer == request or Answer == "#":
                label_colors.append("#50AA50")
                CorrectInstance = 1
                CorrectInstance2 += 1
        if CorrectInstance == 0:
                label_colors.append("#FF0000") #no combination matched --> wrong Answer
    vocable.EnterResults(RecentAnswer, CorrectInstance2, user)
    correctness = vocable.content["answers"][user]["correctness"][-1]
    return vocable, label_colors, correctness

def EndSession(answers, num_vocables, selector, num_total, vocable0, user):
    if num_vocables < 0:
        num_vocables = len(answers)
    corrects = str(len([i for i, x in enumerate(answers) if x == "Richtig"]))
    falses = str(len([i for i, x in enumerate(answers) if x == "Falsch"]))
    num_total += len(answers)
    if selector.listID == 0:
        vocable0[user]["last_stop"] = selector.idx
    return num_vocables, corrects, falses, num_total, vocable0

def intervals(vocable, IntervalMatrix, user):
    LastDelaysList = list(vocable.content["answers"][user]["delay"])
    while -1 in LastDelaysList:
        LastDelaysList.remove(-1)
    for row in IntervalMatrix:
        if LastDelaysList[-1] >= row[0] and LastDelaysList[-1] <= row[1]:
            IntervalMatrixRow = row[2:]  # find the right row of the delay matrix
    return IntervalMatrixRow

def NextVocable(Selector, mode, last_stop, language, vocables):
    Selector.NextEntity(mode, last_stop)
    vocable = vocables[Selector.idx].content
    if language == 0:
        presented = vocable["deutsch"]
        requested = vocable["spanisch"]
    elif language == 1:
        presented = vocable["spanisch"]
        requested = vocable["deutsch"]
    kommentar = vocable["kommentar"]
    return presented, requested, kommentar

def LoadData(path, Selector):
    ListOfObjects = []
    if path != "":
        if path[-3:] == "txt" or path[-3:] == "tsv":
            if os.path.isfile(path[:-3] + "json"):
                with open(path[:-3] + "json", encoding='UTF8') as json_file:
                    vocablesDict = json.load(json_file)
            else:
                vocablesDict = ParseTxt_toDicts(path)
        elif path[-4:] == "json":
            with open(path, encoding='UTF8') as json_file:
                vocablesDict = json.load(json_file)
    for entry in vocablesDict:
        ListOfObjects.append(C_vocables.C_vocables(entry))
    Selector.NumbersOfEnteties(range(len(ListOfObjects)))
    return path, ListOfObjects, Selector

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

def Repeat_Wrong_Answers(answers, answers_idxs, selector):
    New_indexes = []
    for answer, answer_idx in zip(answers, answers_idxs):
        if answer == "Falsch":
            New_indexes.append(answer_idx)
    selector.NumbersOfEnteties(New_indexes)
    selector.listID = len(selector.Entities)-1
    selector.IDs = -1
    answers = []
    answers_idxs = []
    return answers, answers_idxs, selector, len(New_indexes)

def Userselection(user, vocables, Selector):
    ### Check for due vocables
    if user not in vocables[0].content:
        vocables[0].content[user] = {}
        vocables[0].content[user]["last_stop"] = 0
    List_Due_Vocables = []
    for i in range(len(vocables)):
        try:
            if dt.today() >= dt.strptime(vocables[i].content["answers"][user]["NextTime"], "%Y-%m-%d"):
                List_Due_Vocables.append(i)
        except:
            pass
    Selector.NumbersOfEnteties(List_Due_Vocables)
    MaxEntries = len(List_Due_Vocables)
    return vocables, Selector, MaxEntries


















def testfunction(widget):
    testlabel = tk.Label(widget, text="test")
    return testlabel

def testmethod(testclass):
    return testclass.testaction()