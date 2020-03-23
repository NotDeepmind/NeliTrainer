import unittest
import Vokabeltrainer2 as VT
from datetime import datetime as dt
import datetime as dtt
import os

with open("./CreateTestData.py") as DataCreation:
    exec(DataCreation.read())

class MyTestCase(unittest.TestCase):
    def test_Andreas_deutsch_Fälligkeit(self):
        """
        Testing Inputs:
            - All Inputs are presented correctly
            - Kommentar is shown if it contains a proper string, is left out if not
            - Counter counts correctly
        Testing Outputs:
            - Number of Entry fields is correct with the vocable
            - One correct Answer is properly recognized
            - One Wrong Answer is properly recognized
            - One Correct out of 3 is properly recognized
            - # as one of four answers is properly recognized
            - Correct results are displayed in correct colors
        Testing Delays:
            - The correct buttons are shown to delay the vocable
            - The NewDate for next question seem to be correct
        Testing EndSession Screen:
            - All shown counters are correct
            - Successive identifies the wrong answers correctly
            - Repeating wrong vocables presents the correct vocables
        """
        MyGUI = VT.MyGUI()
        self.Questionare_Startup("Andreas", "deutsch", "nach Fälligkeit", 10, MyGUI)
        self.Questionare_Fälligkeit(
            MyGUI,
            ["dTest1-1F", "", "Kommentar: erste fällig", "Dies ist Vokabel 1/4 der Session"],
            1,
            ["sTest1-1F"],
            ["sTest1-1F"],
            ["#50AA50"],
            [2, 1, 1],
            0,
            "Andreas"
        )
        self.Questionare_Fälligkeit(
            MyGUI,
            ["dTest1-3F", "", "Kommentar: testKommentar", "Dies ist Vokabel 2/4 der Session"],
            3,
            ["sTest3-1F-B"],
            ["sTest3-1F-A", "sTest3-1F-B", "sTest3-1F-C"],
            ["#FF0000", "#50AA50", "#FF0000"],
            [6, 1, 3],
            1,
            "Andreas"
        )
        self.Questionare_Fälligkeit(
            MyGUI,
            ["dTest2-1F-A", "dTest2-1F-B", "", "Kommentar: nur fällig bei Andreas", "Dies ist Vokabel 3/4 der Session"],
            1,
            [""],
            ["sTest1-2F"],
            ["#FF0000"],
            [15, 1, 7],
            2,
            "Andreas"
        )
        self.Questionare_Fälligkeit(
            MyGUI,
            ["dTest4-4F-A", "dTest4-4F-B", "dTest4-4F-C", "dTest4-4F-D", "", "Dies ist Vokabel 4/4 der Session"],
            4,
            ["#"],
            ["sTest4-4F-A", "sTest4-4F-B", "sTest4-4F-C", "sTest4-4F-D"],
            ["#50AA50", "#50AA50", "#50AA50", "#50AA50"],
            [61, 1, 30],
            0,
            "Andreas"
        )
        self.Check_EndSession_Labels(MyGUI, ["Andreas,", "4", "2 richtig und", "2 falsch", "Das hier war der 1. Durchgang.", "Insgesamt hast du 4 Fragen beantwortet."])
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[0].invoke() #start asking all wrong answered vocables
        for id in range(2): #quickly cycle through all 2 to come back to EndSession Screen
            widgets = MyGUI.frameButtons.winfo_children()
            widgets[0].invoke()
            widgets = MyGUI.Frame_Buttons_delay.winfo_children()
            widgets[0].invoke()
        self.Check_EndSession_Labels(MyGUI, ["Andreas,", "4", "0 richtig und", "2 falsch", "Das hier war der 2. Durchgang.", "Insgesamt hast du 6 Fragen beantwortet."])
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[0].invoke() #start asking all wrong answered vocables again
        widgets = MyGUI.frame[1].winfo_children()
        widgets[0].insert(0, "sTest3-1F-A")
        widgets[1].insert(0, "sTest3-1F-B")
        widgets[2].insert(0, "sTest3-1F-C")
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[0].invoke()
        widgets = MyGUI.Frame_Buttons_delay.winfo_children()
        widgets[0].invoke() #answered the first one correctly
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[0].invoke()
        widgets = MyGUI.Frame_Buttons_delay.winfo_children()
        widgets[0].invoke() #answered the second one incorrectly
        self.Check_EndSession_Labels(MyGUI, ["Andreas,", "4", "1 richtig und", "1 falsch", "Das hier war der 3. Durchgang.", "Insgesamt hast du 8 Fragen beantwortet."])
        widgets = MyGUI.frameButtons.winfo_children()
        self.assertEqual(widgets[0].cget("text"), "Falsche Antworten wiederholen")
        widgets[0].invoke()
        widgets = MyGUI.frame[1].winfo_children()
        widgets[0].insert(0, "sTest1-2F")
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[0].invoke()
        widgets = MyGUI.Frame_Buttons_delay.winfo_children()
        widgets[0].invoke()
        self.Check_EndSession_Labels(MyGUI, ["Andreas,", "4", "1 richtig und", "0 falsch", "Das hier war der 4. Durchgang.", "Insgesamt hast du 9 Fragen beantwortet."])
        widgets = MyGUI.frameButtons.winfo_children()
        self.assertNotEqual(widgets[0].cget("text"), "Falsche Antworten wiederholen") #Repeat wrong answers button should have disappeared here
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[1].invoke()
        MyGUI = VT.MyGUI()
        self.Questionare_Startup("Andreas", "deutsch", "nach Fälligkeit", 10, MyGUI)
        widgets = MyGUI.frame[1].winfo_children()
        self.assertEqual(widgets[7].cget("text"), "Keine Vokabeln für heute fällig!") #Check if on restart, all "fällige" vocables are correctly checked
        MyGUI.root.destroy()

    def test_Andreas_spanisch_Reihenfolge(self):
        """
        Testing expands the "nach Fälligkeit"
        Inputs:
            - Check Inputs of the right vokabels
            - Check correctly starting at the first vocable
            - Check corrects continuation after full list is finished
            - Check correct counters during first cycle (location in list of all vocables) and during second cycle (no location in  list of all vocables)
        Outputs:
            - Check correct number of Entry fields
            - Check "#" Wildcard all correct
        EndSession:
            - Check correct screen for first, second and third cycle
            - check correct number of vocables, number of answers, corrects and falses
        RepeatWrongAnswers:
            - Check the correct inputs during second cycle
            - Check correctly ignoring correct answers from previous cycle, also from first to second cycle
        Saving:
            - Check if all "fällige" vocables are checked correctly and when restarting no "fällige" are found and program doesn't continue to questioning
        """
        MyGUI = VT.MyGUI()
        self.Questionare_Startup("Andreas", "spanisch", "nach Reihenfolge", 10, MyGUI)
        self.Questionare_Reihenfolge(
            MyGUI,
            ["sTest1-1R", "", "Kommentar: Erster Eintrag", "Dies ist Vokabel 1/10 der Session", "bzw. 1/8 der Datenbank"],
            1,
            ["dTest1-1R"],
            ["dTest1-1R"],
            ["#50AA50"],
            "Andreas"
        )
        self.Questionare_SkipEntryReihenfolge(7, MyGUI) #just skip the 7 in between and check if first reappears properly
        self.Questionare_Reihenfolge(
            MyGUI,
            ["sTest1-1R", "", "Kommentar: Erster Eintrag", "Dies ist Vokabel 9/10 der Session", "bzw. 1/8 der Datenbank"],
            1,
            ["#"],
            ["dTest1-1R"],
            ["#50AA50"],
            "Andreas"
        )
        self.Questionare_SkipEntryReihenfolge(1, MyGUI)
        self.Check_EndSession_Labels(MyGUI, ["Andreas,", "10", "2 richtig und", "8 falsch", "Das hier war der 1. Durchgang.", "Insgesamt hast du 10 Fragen beantwortet."])
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[0].invoke()
        self.Questionare_Reihenfolge(
            MyGUI,
            ["sTest3-1R-A", "sTest3-1R-B", "sTest3-1R-C", "", "Kommentar: testKommentar", "Dies ist Vokabel 1/8 der Session"],
            1,
            ["dTest1-3R"],
            ["dTest1-3R"],
            ["#50AA50"],
            "Andreas"
        )
        self.Questionare_SkipEntryReihenfolge(7, MyGUI)
        self.Check_EndSession_Labels(MyGUI, ["Andreas,", "10", "1 richtig und", "7 falsch", "Das hier war der 2. Durchgang.", "Insgesamt hast du 18 Fragen beantwortet."])
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[0].invoke()
        self.Questionare_Reihenfolge(
            MyGUI,
            ["sTest1-2R", "", "Dies ist Vokabel 1/7 der Session"],
            2,
            ["#"],
            ["dTest2-1R-A", "dTest2-1R-B"],
            ["#50AA50", "#50AA50"],
            "Andreas"
        )
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[1].invoke()
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[1].invoke()
        MyGUI = VT.MyGUI()
        self.Questionare_Startup("Andreas", "spanisch", "nach Reihenfolge", 3, MyGUI)
        self.Questionare_Reihenfolge(   # last_stop from first part was set and recognized correctly. Just did 10 answers, starting at vocable 1, going through a full 8 and 2 more leaves us now at vocable 3.
            MyGUI,
            ["sTest1-2R", "", "Dies ist Vokabel 1/3 der Session", "bzw. 3/8 der Datenbank"],
            2,
            ["#"],
            ["dTest2-1R-A", "dTest2-1R-B"],
            ["#50AA50", "#50AA50"],
            "Andreas"
        )
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[1].invoke()
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[1].invoke()
        MyGUI = VT.MyGUI()
        self.Questionare_Startup("Andreas", "spanisch", "nach Reihenfolge", 3, MyGUI)
        self.Questionare_Reihenfolge(   # last_stop from second run was set correctly, as we wanted to answer 3 vocables but ended the session early after the first answer, leaving us at vocable 4
            MyGUI,
            ["sTest4-4R-A", "sTest4-4R-B", "sTest4-4R-C", "sTest4-4R-D", "", "Dies ist Vokabel 1/3 der Session", "bzw. 4/8 der Datenbank"],
            4,
            ["#"],
            ["dTest4-4R-A", "dTest4-4R-B", "dTest4-4R-C", "dTest4-4R-D"],
            ["#50AA50", "#50AA50", "#50AA50", "#50AA50"],
            "Andreas"
        )
        MyGUI.root.destroy()

    def test_Christa_spanisch_Fällgikeit(self):
        """
        Expand testing from "Andreas" cases
            - Check correct inputs
            - Check correct counters, here being one less compared to "Andreas"
            - Check if answering works properly, delays are chosen correctly and set correctly
            - Check if premature ending the session works properly
            - Check if one leftout vocable is correctly asked when starting again
        """
        MyGUI = VT.MyGUI()
        self.Questionare_Startup("Christa", "spanisch", "nach Fälligkeit", 10, MyGUI)
        self.Questionare_Fälligkeit(
            MyGUI,
            ["sTest1-1F", "", "Kommentar: erste fällig", "Dies ist Vokabel 1/3 der Session"],
            1,
            ["dTest1-1F"],
            ["dTest1-1F"],
            ["#50AA50"],
            [2, 1, 1],
            0,
            "Christa"
        )
        self.Questionare_Fälligkeit(
            MyGUI,
            ["sTest3-1F-A", "sTest3-1F-B", "sTest3-1F-C", "", "Kommentar: testKommentar", "Dies ist Vokabel 2/3 der Session"],
            1,
            ["dTest1-1G"],
            ["dTest1-3F"],
            ["#FF0000"],
            [6, 1, 3],
            1,
            "Christa"
        )
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[1].invoke()
        #here one vocable has to be skipped compared to "Andreas" List
        self.Check_EndSession_Labels(MyGUI, ["Christa,", "2", "1 richtig und", "1 falsch", "Das hier war der 1. Durchgang.", "Insgesamt hast du 2 Fragen beantwortet."])
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[0].invoke()
        self.Questionare_Fälligkeit(
            MyGUI,
            ["sTest3-1F-A", "sTest3-1F-B", "sTest3-1F-C", "", "Kommentar: testKommentar", "Dies ist Vokabel 1/1 der Session"],
            1,
            ["dTest1-3F"],
            ["dTest1-3F"],
            ["#50AA50"],
            [2, 1, 1],
            1,
            "Christa"
        )
        self.Check_EndSession_Labels(MyGUI, ["Christa,", "2", "1 richtig und", "0 falsch", "Das hier war der 2. Durchgang.", "Insgesamt hast du 3 Fragen beantwortet."])
        widgets = MyGUI.frameButtons.winfo_children()
        self.assertNotEqual(widgets[0].cget("text"), "Falsche Antworten wiederholen") #Repeat wrong answers button should have disappeared here
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[1].invoke()
        #start over and do the one missing, because the session before was ended before reaching 3/3
        MyGUI = VT.MyGUI()
        self.Questionare_Startup("Christa", "spanisch", "nach Fälligkeit", 10, MyGUI)
        self.Questionare_Fälligkeit(
            MyGUI,
            ["sTest4-4F-A", "sTest4-4F-B", "sTest4-4F-C", "sTest4-4F-D", "", "Dies ist Vokabel 1/1 der Session"],
            4,
            ["dTest1-3F"],
            ["dTest4-4F-A", "dTest4-4F-B", "dTest4-4F-C", "dTest4-4F-D"],
            ["#FF0000", "#FF0000", "#FF0000", "#FF0000"],
            [61, 1, 30],
            1,
            "Christa"
        )
        MyGUI.root.destroy() # leave one "fällig" open


    def test_Christa_deutsch_Reihenfolge(self):
        """
        Additional testing of "nach Reihenfolge" for second user
        inputs:
            - Checking that starting occurs at the correct index (the forth vocable of the list, as last_stop == 2 marks the next ID of the LAST answered vocable (remember python starts counting at 0))
            - Double Checking all the requirements when asking in sequence
        Saving:
            - Check if after closing the "Reihenfolge" Session, and restarting, the list of vocables is continued at the correct position

        Checking if session can be finished properly before reaching the set limit number of vocables
        """
        MyGUI = VT.MyGUI()
        self.Questionare_Startup("Christa", "deutsch", "nach Reihenfolge", 3, MyGUI)
        self.Questionare_Reihenfolge(
            MyGUI,
            ["dTest4-4R-A", "dTest4-4R-B", "dTest4-4R-C", "dTest4-4R-D", "", "Dies ist Vokabel 1/3 der Session", "bzw. 4/8 der Datenbank"],
            4,
            [""],
            ["sTest4-4R-A", "sTest4-4R-B", "sTest4-4R-C", "sTest4-4R-D"],
            ["#FF0000", "#FF0000", "#FF0000", "#FF0000"],
            "Christa"
        )
        self.Questionare_Reihenfolge(
            MyGUI,
            ["dTest1-1F", "", "Kommentar: erste fällig", "Dies ist Vokabel 2/3 der Session", "bzw. 5/8 der Datenbank"],
            1,
            ["sTest1-1F"],
            ["sTest1-1F"],
            ["#50AA50"],
            "Christa"
        )
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[1].invoke()
        self.Check_EndSession_Labels(MyGUI, ["Christa,", "2", "1 richtig und", "1 falsch", "Das hier war der 1. Durchgang.", "Insgesamt hast du 2 Fragen beantwortet."])
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[0].invoke()
        self.Questionare_Reihenfolge(
            MyGUI,
            ["dTest4-4R-A", "dTest4-4R-B", "dTest4-4R-C", "dTest4-4R-D", "", "Dies ist Vokabel 1/1 der Session"],
            4,
            ["#"],
            ["sTest4-4R-A", "sTest4-4R-B", "sTest4-4R-C", "sTest4-4R-D"],
            ["#50AA50", "#50AA50", "#50AA50", "#50AA50"],
            "Christa"
        )
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[1].invoke()
        #check after savong and restarting that the correct next vocable is shown
        MyGUI = VT.MyGUI()
        self.Questionare_Startup("Christa", "deutsch", "nach Reihenfolge", 3, MyGUI)
        self.Questionare_Reihenfolge(
            MyGUI,
            ["dTest1-3F", "","Kommentar: testKommentar", "Dies ist Vokabel 1/3 der Session"],
            3,
            ["#"],
            ["sTest3-1F-A", "sTest3-1F-B", "sTest3-1F-C"],
            ["#50AA50", "#50AA50", "#50AA50"],
            "Christa"
        )
        MyGUI.root.destroy()

    def test_Tippfehler(self):
        """
        Check if the "Tippfehler" button works as intended "nach Reihenfolge" and "nach Fällgikeit"
        """
        MyGUI = VT.MyGUI()
        self.Questionare_Startup("Christa", "spanisch", "nach Fälligkeit", 3, MyGUI)
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[0].invoke()
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[2].invoke() # mark as tippfehler
        self.assertEqual(MyGUI.vocables[MyGUI.Selector.idx].content["answers"][MyGUI.user]["correctness"][-1], "Richtig")
        self.assertEqual(MyGUI.vocables[MyGUI.Selector.idx].content["answers"][MyGUI.user]["answer"][-1][0], "Tippfehler gemacht")
        widgets = MyGUI.Frame_Buttons_delay.winfo_children()
        widgets[0].invoke()
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[0].invoke()

        MyGUI = VT.MyGUI()
        self.Questionare_Startup("Andreas", "deutsch", "nach Reihenfolge", 3, MyGUI)
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[0].invoke()
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[1].invoke() # mark as tippfehler
        self.assertEqual(MyGUI.vocables[MyGUI.Selector.idx].content["answers"][MyGUI.user]["correctness"][-1], "Richtig")
        self.assertEqual(MyGUI.vocables[MyGUI.Selector.idx].content["answers"][MyGUI.user]["answer"][-1][0], "Tippfehler gemacht")
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[0].invoke()
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[1].invoke()
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[1].invoke()

    def test_ChangeManagement(self):
        """
        Testing the ChangeManagement here, giving the option to search and change entries
        - Searching function is rested for deutsch and kommentar entries
        - correct results are tested for the search, next and previous function buttons (including when pushing next at the end of list and vice versa for previous)
        - saving of changed entries is checked
            > input entries in deutsch and spanisch are properly separated into a list of strings split by ","
            > starting or trailing spaces are removed properly
            > entry is saved for the current session and in file, reloading database remembers the changed entry correctly
        """
        MyGUI = VT.MyGUI()
        self.Questionare_Startup_LoadData(MyGUI)
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[1].invoke()
        widgets_left = MyGUI.frame[0].winfo_children()
        widgets_left[2].insert(0,"4-4")
        widgets_left[7].invoke()
        self.assertEqual(MyGUI.FoundEntries[0].get(), "dTest4-4R-A, dTest4-4R-B, dTest4-4R-C, dTest4-4R-D", "Seach for german Entry did not show correct result")
        widgets_right = MyGUI.frame[1].winfo_children()
        widgets_right[7].invoke() # next result
        self.assertEqual(MyGUI.FoundEntries[0].get(), "dTest4-4F-A, dTest4-4F-B, dTest4-4F-C, dTest4-4F-D", "Next Result is not shown corectly after search")
        widgets_right[7].invoke() # next result
        self.assertEqual(MyGUI.FoundEntries[0].get(), "dTest4-4R-A, dTest4-4R-B, dTest4-4R-C, dTest4-4R-D", "Next Result is not shown properly after reaching the first result again")
        widgets_left[2].delete(0,"end")
        widgets_left[6].insert(0,"test") # testing search for kommentar
        widgets_left[7].invoke()
        self.assertEqual(MyGUI.FoundEntries[1].get(), "sTest3-1R-A, sTest3-1R-B, sTest3-1R-C", "Searching for kommentar did not yield the correct result or spanisch is not shown properly")
        self.assertEqual(MyGUI.FoundEntries[2].get(), "testKommentar", "Searching for kommentar did not yield the correct result or kommentar is not shown properly")
        widgets_left[6].delete(0,"end")
        widgets_left[2].insert(0,"Test") # search for Test in german field, should give 8 results
        widgets_left[7].invoke()
        widgets_right[8].invoke() # previous result
        self.assertEqual(MyGUI.FoundEntries[0].get(), "dTest4-4F-A, dTest4-4F-B, dTest4-4F-C, dTest4-4F-D", "Previous Results is not shown properly (at least when cycling through the full result list, " +
                                                                                                            "going from first results to the last)")
        MyGUI.FoundEntries[0].delete(0, "end")
        MyGUI.FoundEntries[0].insert(0, "new_german, new_german2")
        MyGUI.FoundEntries[1].delete(0, "end")
        MyGUI.FoundEntries[1].insert(0, "new_spanish, new_spanish2")
        MyGUI.FoundEntries[2].delete(0, "end")
        MyGUI.FoundEntries[2].insert(0, "new_comment")
        widgets_right[9].invoke() # save
        widgets_left[2].delete(0,"end")
        widgets_left[2].insert(0,"new_german") # search for Test in german field, should give 8 results
        widgets_left[7].invoke()
        self.assertEqual(MyGUI.vocables[-1].content["deutsch"][0], "new_german", "Changed Entry is not set correctly in MyGUI.vocables")
        self.assertEqual(MyGUI.FoundEntries[1].get(), "new_spanish, new_spanish2", "Changed Entry is not found or not shown correctly")
        MyGUI.root.destroy()
        #reload the data to check if changes are saved correctly in the file
        MyGUI = VT.MyGUI()
        self.Questionare_Startup_LoadData(MyGUI)
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[1].invoke()
        widgets_left = MyGUI.frame[0].winfo_children()
        widgets_left[2].insert(0,"new_german") # search for Test in german field, should give 8 results
        widgets_left[7].invoke()
        self.assertEqual(MyGUI.vocables[-1].content["deutsch"][0], "new_german", "Changed Entry is not set correctly in MyGUI.vocables after reloading the database")
        self.assertEqual(MyGUI.FoundEntries[1].get(), "new_spanish, new_spanish2", "Changed Entry is not found after reloading of database")
        MyGUI.root.destroy()
        #restore the original data file
        with open("./CreateTestData.py") as DataCreation:
            exec(DataCreation.read())

    def test_TSV_export(self):
        """
        Testing the TSV export functionality with the full test database
        loading the first and last line and checking if that is formatted as expected (deutsch, spanisch, kommentar)
        """
        Path_exported_TSV = os.path.dirname(os.path.abspath(__file__)) + r"\Testdata_export.tsv"
        if os.path.isfile(Path_exported_TSV):
            os.remove(Path_exported_TSV) #delete old TSV if one exists
        MyGUI = VT.MyGUI()
        self.Questionare_Startup_LoadData(MyGUI)
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[4].invoke() #export as TSV
        with open(Path_exported_TSV, "r+", encoding='utf-8') as source:
            file_content = source.readlines()
        for i, line in zip(range(len(file_content)), file_content):
            file_content[i] = line[:-1] #removes the trailing \n from every line
        self.assertEqual(file_content[0], "dTest1-1R, 	sTest1-1R, 	Erster Eintrag", "At least the first line of the database was not exported properly to the TSV file.")
        self.assertEqual(file_content[-1], "dTest4-4F-A, dTest4-4F-B, dTest4-4F-C, dTest4-4F-D, 	sTest4-4F-A, sTest4-4F-B, sTest4-4F-C, sTest4-4F-D, 	", "At least the last line of the database was not exported "
                                                                                                                                                               "properly to the TSV file.")

    def test_AddfromTSV(self):
        """
        Testing the import function from TSV to integrate new vocable lists into the database
        > loading of the Testdata_import.tsv example set
        > Check that the fällige vocables for user Christa didnt change
        > repeat the process the check that duplicate entries are found correctly
        > check that the fällige vocables for user Andreas changed correctly, adding a new entry for the day
        > restore original database at the end
        """

        MyGUI = VT.MyGUI()
        MyGUI.path_AddVocables = os.path.dirname(os.path.abspath(__file__)) + r"\Testdata_import.tsv"
        self.Questionare_Startup_LoadData(MyGUI)
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[2].invoke()
        MyGUI.RadioBtns["mode"].set("nach Fälligkeit")
        MyGUI.RadioBtns["language"].set("spanisch")
        MyGUI.RadioBtns["user selection"].set("Christa")
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[0].invoke()
        widgets = MyGUI.frame[0].winfo_children()
        self.assertEqual(widgets[3].cget("text"), "Dies ist Vokabel 1/3 der Session", "Christa has more >fällige< vocables, probably some error in adding of TSV file")
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[1].invoke()
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[1].invoke()
        del MyGUI
        MyGUI = VT.MyGUI()
        MyGUI.path_AddVocables = os.path.dirname(os.path.abspath(__file__)) + r"\Testdata_import.tsv"
        self.Questionare_Startup_LoadData(MyGUI)
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[2].invoke()
        MyGUI.RadioBtns["mode"].set("nach Fälligkeit")
        MyGUI.RadioBtns["language"].set("spanisch")
        MyGUI.RadioBtns["user selection"].set("Andreas")
        widgets = MyGUI.frameButtons.winfo_children()
        widgets[0].invoke()
        widgets = MyGUI.frame[0].winfo_children()
        self.assertNotEqual(widgets[4].cget("text"), "Dies ist Vokabel 1/4 der Session", "The added Entry from the TSC file was not recognized properly")
        self.assertNotEqual(widgets[4].cget("text"), "Dies ist Vokabel 1/6 der Session", "The entry from the import TSV was taking twice, checking of dublicate entries did not work, error in adding of TSV files")
        self.assertEqual(widgets[4].cget("text"), "Dies ist Vokabel 1/5 der Session", "Andreas has not the correct 5 entries, probably an error in adding of TSV file")
        MyGUI.root.destroy()
        with open("./CreateTestData.py") as DataCreation:
            exec(DataCreation.read())

    def Check_EndSession_Labels(self, GUI, labels):
        widgets = GUI.frame[0].winfo_children()
        self.assertEqual(widgets[0].cget("text"), labels[0])
        self.assertEqual(widgets[2].cget("text"), labels[1])
        self.assertEqual(widgets[5].cget("text"), labels[2])
        self.assertEqual(widgets[6].cget("text"), labels[3])
        self.assertEqual(widgets[7].cget("text"), labels[4])
        self.assertEqual(widgets[8].cget("text"), labels[5])

    def Questionare_Startup_LoadData(self, GUI):
        GUI.testmode = True
        GUI.Create_Buttons("MainScreen")
        widgets = GUI.frameButtons.winfo_children()
        self.assertEqual(widgets[0].cget("text"), "Lektion auswählen") #Choose Lecture at right position
        widgets[0].invoke()
    def Questionare_Startup(self, user, language, mode, no, GUI):
        self.Questionare_Startup_LoadData(GUI)
        widgets = GUI.frameButtons.winfo_children()
        self.assertEqual(widgets[0].cget("text"), "Weiter") #continue button found
        GUI.RadioBtns["mode"].set(mode)
        GUI.RadioBtns["language"].set(language)
        GUI.RadioBtns["user selection"].set(user)
        GUI.ET_MaxNumVocables.insert(0, str(no))
        widgets = GUI.frameButtons.winfo_children()
        widgets[0].invoke()

    def Questionare_SkipEntryReihenfolge(self, no, GUI):
        for i in range(2*no):
            widgets = GUI.frameButtons.winfo_children()
            widgets[0].invoke()
    def Questionare_basic(self, GUI, Labels_Presented, no_of_entries, Entries, results, colors, user):
        widgets = GUI.frame[0].winfo_children()
        for widget, label in zip(widgets, Labels_Presented):
            self.assertEqual(widget.cget("text"), label) #correct data presented
        widgets = GUI.frame[1].winfo_children()
        self.assertEqual(len(widgets), no_of_entries) #correct number of answering fields presented
        for widget, entry in zip(widgets, Entries):
            widget.insert(0, entry)
        widgets = GUI.frameButtons.winfo_children()
        self.assertEqual(widgets[0].cget("text"), "Eingabe prüfen") #Check Entry Button at right location found
        widgets[0].invoke()
        widgets = GUI.frame[1].winfo_children()
        i = 0
        for widget in widgets:
            if widget.winfo_class() == "Label":
                self.assertEqual(widget.cget("text"), results[i])
                self.assertEqual(widget.cget("fg"), colors[i])
                i += 1
    def Questionare_Fälligkeit(self, GUI, Labels_Presented, no_of_entries, Entries, results, colors, delays, delay_idx, user):
        self.Questionare_basic(GUI, Labels_Presented, no_of_entries, Entries, results, colors, user)
        widgets = GUI.Frame_Buttons_delay.winfo_children()
        for widget, delay in zip(widgets, delays):
            self.assertEqual(widget.cget("text"), "+" + str(delay) + "Tage")
        widgets = GUI.Frame_Buttons_delay.winfo_children()
        current_idx = int(GUI.Selector.idx)
        widgets[delay_idx].invoke()
        NewDate = dt.today() + dtt.timedelta(delays[delay_idx])
        self.assertEqual(GUI.vocables[current_idx].content["answers"][user]["NextTime"], NewDate.strftime("%Y-%m-%d"), msg=NewDate.strftime("%Y-%m-%d"))
    def Questionare_Reihenfolge(self, GUI, Labels_Presented, no_of_entries, Entries, results, colors, user):
        current_idx = int(GUI.Selector.idx)
        correct_NextTime = GUI.vocables[current_idx].content["answers"][user]["NextTime"]
        self.Questionare_basic(GUI, Labels_Presented, no_of_entries, Entries, results, colors, user)
        widgets = GUI.frameButtons.winfo_children()
        widgets[0].invoke()
        self.assertEqual(GUI.vocables[current_idx].content["answers"][user]["NextTime"], correct_NextTime) # make sure the "NextTime" Entry did not change after answering (must change only in "Fälligkeit" mode)

if __name__ == '__main__':
    unittest.main()
