import tkinter as tk
from tkinter import filedialog
import json
import C_vocables
from datetime import datetime as dt
import os as os
import csv
import math
from database import Database
from VT_logger import logger


def AddVocables(vocables, path_add, path):
    if path_add == "":
        path_add = filedialog.askopenfilename(filetypes=[("TSV Files", "*.tsv *.txt")])
    if path_add[-3:] != "txt" and path_add[-3:] != "tsv":
        logger.warning("User somehow managed to try and load a file with neither txt nor tsv extension")
    else:
        NewVocs = ParseTxt_toDicts(path_add)
    if len(NewVocs) == 0:
        logger.warning("Could not parse any vocables from the TSV!")
    else:
        db = Database(path)
        for entry in NewVocs:
            prev_entry = db.find_vocable(
                ", ".join(entry["deutsch"]),
                ", ".join(entry["spanisch"]),
                entry["kommentar"]
            )
            if len(prev_entry) > 0:
                logger.warning("Trying to add existing vocable to the database, matching vocID "
                               + str(prev_entry[0][0]))
            else:
                db.add_vocable(", ".join(entry["deutsch"]), ", ".join(entry["spanisch"]), entry["kommentar"])
                new_vocID = \
                    db.find_vocable(", ".join(entry["deutsch"]), ", ".join(entry["spanisch"]), entry["kommentar"])
                for user in ["Andreas", "Christa", "Gemeinsam"]:
                    db.add_lessons_entry(user, "Alles", new_vocID[0][0], entry["answers"][user]["NextTime"])
                logger.debug("Added vocable " + ", ".join(entry["deutsch"]) + " to the database")
    return vocables


def CheckEntry(Answers, vocable, requested, user, selector, path, mode):
    if not selector.idx == [] and mode == "nach Reihenfolge" and len(selector.Entities) == 2:
        logger.debug('Setting new last_stop to ' + str(selector.idx))
        db = Database(path)
        db.set_lessons_last_stop(user, 'Alles', selector.idx)
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
    if CorrectInstance2 == len(RecentAnswer):
        correctness = 'Richtig'
    else:
        correctness = 'Falsch'
    answer_datetime = vocable.EnterResults(RecentAnswer, correctness, user, path)
    return label_colors, correctness, answer_datetime


def EndSession(answers, num_vocables, num_total):
    if num_vocables < 0:
        num_vocables = len(answers)
    corrects = str(len([i for i, x in enumerate(answers) if x == "Richtig"]))
    falses = str(len([i for i, x in enumerate(answers) if x == "Falsch"]))
    num_total += len(answers)
    return num_vocables, corrects, falses, num_total


def intervals(vocable, IntervalMatrix, user):
    # for key in vocable.content:
    #     print("content keys: " + key)
    # LastDelaysList = list(vocable.content["answers"][user]["delay"])
    # while -1 in LastDelaysList:
    #     LastDelaysList.remove(-1)
    last_delay = vocable.content['delay']
    for row in IntervalMatrix:
        if last_delay >= row[0] and last_delay <= row[1]:
            logger.debug('Old Delay was ' + str(last_delay) + ', new choices are ' + str(row[2]) + ", "
            + str(row[3]) + ", " + str(row[4]))
            return row[2:]  # find the right row of the delay matrix


def NextVocable(Selector, mode, path, user, language, vocables, MaxNumVocables):
    db = Database(path)
    last_stop = db.read_lesson_last_stop(user, 'Alles')
    Selector.last_stop = last_stop[0][0]
    Selector.NextEntity(mode)
    logger.debug("Trying to find vocable with vocID " + str(Selector.idx))
    for vocable0 in vocables:
        if vocable0.content['vocID'] == Selector.idx:
            logger.debug("found!")
            vocable = vocable0.content
            current_vocable = vocable0
            break
    if language == 0:
        presented = vocable["deutsch"]
        requested = vocable["spanisch"]
    elif language == 1:
        presented = vocable["spanisch"]
        requested = vocable["deutsch"]
    kommentar = vocable["kommentar"]
    if mode == "nach Fälligkeit":
        MaxNumVocables = len(Selector.Entities[-1])
    return presented, requested, kommentar, MaxNumVocables, current_vocable


def LoadData(path, Selector, user = "Andreas"):
    ListOfObjects = []
    path_no_ending, file_extension = path.split(".")
    path = path_no_ending + ".db" # work with db in future
    if not os.path.isfile(path):
        if os.path.isfile(path_no_ending + ".json"):
            with open(path_no_ending + ".json", encoding='UTF8') as json_file:
                vocablesDict = json.load(json_file)
        elif os.path.isfile(path_no_ending + ".tsv"):
            vocablesDict = ParseTxt_toDicts(path_no_ending + ".tsv")
        for entry in vocablesDict:
            ListOfObjects.append(C_vocables.C_vocables(entry))
    db = Database(path)
    if len(ListOfObjects) > 0:
        db.convert_JSON(ListOfObjects)

    # load with different priorities, use db if exists, use json if not, use tsv or txt if no json exists
    # old file formats are converted to db and will solely be used in the future
    ListOfObjects = []
    ListOfVocIDs = []
    ListOfDueVocIDs = []
    for vocID in db.read_lesson_vocIDs(user, "Alles"):
        entry = db.read_vocable_byID(vocID[0])
        if len(entry) > 0:
            entry_dict = {
                'vocID': entry[0][0],
                'deutsch': entry[0][1].split(", "),
                'spanisch': entry[0][2].split(", "),
                'kommentar': entry[0][3]
            }
            ListOfVocIDs.append(entry_dict['vocID'])
            entry_faellig = db.read_lessons_entry_byVocID(user, "Alles", entry_dict['vocID'])
            entry_dict['delay'] = entry_faellig[0][1]
            entry_dict["NextTime"] = entry_faellig[0][2]
            if dt.today() >= dt.strptime(entry_dict["NextTime"], "%Y-%m-%d"):
                ListOfDueVocIDs.append(entry_dict['vocID'])
            ListOfObjects.append(C_vocables.C_vocables(entry_dict))
            logger.debug(
                'Loaded vocables vocID ' + str(entry_dict['vocID'])
                + ', deutsch: ' + ", ".join(entry_dict['deutsch'])
                + ', spanisch: ' + ", ".join(entry_dict['spanisch'])
                + ', kommentar: ' + entry_dict['kommentar']
                + ', last delay was: ' + str(entry_dict['delay'])
                + ', next time on: ' + entry_dict["NextTime"]
            )
        else:
            logger.warning("You tried to load an entry that has vocIDref " + str(vocID[0]) + " in the lesson "
                           + user + "_lesson_Alles, but it does not exist in the vocable table")
            logger.warning("Removing entry from user " + user + "lessons 'Alles'")
            try: db.delete_lesson_entry_byVocID(user, "Alles", vocID[0])
            except: pass
    Selector.NumbersOfEnteties(ListOfVocIDs)
    Selector.NumbersOfEnteties(ListOfDueVocIDs)
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
    with open(path, mode='w', encoding='UTF8', newline='') as exportfile:
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

