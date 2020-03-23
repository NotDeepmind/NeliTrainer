import tkinter as tk
from tkinter import filedialog
import json
import C_vocables
from datetime import datetime as dt
import os as os
import csv
import math



def AddVocables(vocables, path):
    if path == "":
        path = filedialog.askopenfilename()
    if path[-3:] != "txt" and path[-3:] != "tsv":
        print("Es können nur Txt Dateien hinzugefügt werden (Komma getrennt, Tabstopp getrennt)")
    else:
        NewVocs = ParseTxt_toDicts(path)
        NewVocsClassed = []
        for entry in NewVocs:
            NewVocsClassed.append(C_vocables.C_vocables(entry))
        for i, item in zip(range(len(NewVocsClassed)), NewVocsClassed):
            exists = 0
            for olditem in vocables:
                if item.content["deutsch"] == olditem.content["deutsch"] and item.content["spanisch"] == olditem.content["spanisch"] and item.content["kommentar"] == olditem.content["kommentar"]:
                    exists = 1
                    print(item.content["deutsch"][0] + " exists already")
            if exists == 0:
                vocables.insert(math.floor(i*len(vocables) / len(NewVocs)), item)
                #print(item.content["deutsch"][0] + " newly added to the database")
    return vocables

def CheckEntry(Answers, vocable, requested, user, selector, vocable0):
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
    if selector.listID == 0:
        vocable0.content[user]["last_stop"] = selector.idx
    return vocable, label_colors, correctness, vocable0

def EndSession(answers, num_vocables, num_total):
    if num_vocables < 0:
        num_vocables = len(answers)
    corrects = str(len([i for i, x in enumerate(answers) if x == "Richtig"]))
    falses = str(len([i for i, x in enumerate(answers) if x == "Falsch"]))
    num_total += len(answers)
    return num_vocables, corrects, falses, num_total

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
    file.close()
    for id in range(len(file_content)):
        strings = file_content[id].split("\t")
        if len(strings) == 5:
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
            stringsNTAndreas = strings[3].strip()
            stringsNTChrista = strings[4].strip()
            ListOfDicts.append({"spanisch": stringsSpanisch,
                                "deutsch": stringsDeutsch,
                                "kommentar": stringsKommentar,
                                "answers": {
                                    "Andreas": {
                                        "datetime": [""],
                                        "answer": [""],
                                        "delay": [0],
                                        "correctness": ["Richtig"],
                                        "NextTime": stringsNTAndreas
                                    },
                                    "Christa": {
                                        "datetime": [""],
                                        "answer": [""],
                                        "delay": [0],
                                        "correctness": ["Richtig"],
                                        "NextTime": stringsNTChrista
                                    }
                                }
                                })
        else:
            print("There is an Issue with your .TSV: Number of columns != 5")
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

def saving(path, vocables, nice_JSON):
    vocable_list = []
    for vocable in vocables:
        vocable_list.append(vocable.content)
    if path[-3:] == "txt" or path[-3:] == "tsv":
        with open(path[:-3] + "json", 'w', encoding='UTF8') as fp:
            if nice_JSON == 1:
                json.dump(vocable_list, fp, indent=4)
            else:
                json.dump(vocable_list, fp)
    elif path[-4:] == "json":
        with open(path, 'w', encoding='UTF8') as fp:
            if nice_JSON == 1:
                json.dump(vocable_list, fp, indent=4)
            else:
                json.dump(vocable_list, fp)

def saveTSV(vocables, path):
    TSV_lines = []
    for vocable in vocables:
        deutsch = ""
        spanisch = ""
        kommentar = vocable.content["kommentar"]
        for word in vocable.content["deutsch"]:
            deutsch += word + ", "
        for word in vocable.content["spanisch"]:
            spanisch += word + ", "
        TSV_lines.append([deutsch, spanisch, kommentar])
    with open(path + "_export.tsv", mode='w', encoding='UTF8', newline='') as exportfile:
        writer = csv.writer(exportfile, delimiter='\t')
        for line in TSV_lines:
            writer.writerow(line)

def tippfehler(vocable, user, answers):
    vocable.content["answers"][user]["correctness"][-1] = "Richtig"
    vocable.content["answers"][user]["answer"][-1][0] = "Tippfehler gemacht"
    if len(vocable.content["answers"][user]["answer"][-1]) > 1:
        for id in range(1,len(vocable.content["answers"][user]["answer"][-1])):
            vocable.content["answers"][user]["answer"][-1][id] = ""
    answers[-1] = "Richtig"
    return vocable, answers

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