import tkinter as tk
from tkinter import filedialog
import json
import C_vocables
from datetime import datetime as dt
import datetime as dtt
import os as os
from ChangeManagement import ChangeManagement





def SelectLecture(path):
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
    return path, ListOfObjects

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



















def testfunction(widget):
    testlabel = tk.Label(widget, text="test")
    return testlabel

def testmethod(testclass):
    return testclass.testaction()