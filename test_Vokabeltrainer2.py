import unittest
import Vokabeltrainer2 as VT
from datetime import datetime as dt
import datetime as dtt

exec(open("./CreateTestData.py").read())

class MyTestCase(unittest.TestCase):
    def test_Andreas_Fälligkeit(self):
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
        """
        MyGUI = VT.MyGUI()
        MyGUI.testmode = True
        MyGUI.Create_Buttons()
        widgets = MyGUI.frameButtons.winfo_children()
        self.assertEqual(widgets[0].cget("text"), "Lektion auswählen") #Choose Lecture at right position
        widgets[0].invoke()
        widgets = MyGUI.frameButtons.winfo_children()
        self.assertEqual(widgets[0].cget("text"), "Weiter") #continue button found
        MyGUI.RadioBtns["mode"].set("nach Fälligkeit")
        MyGUI.RadioBtns["language"].set("deutsch")
        MyGUI.RadioBtns["user selection"].set("Andreas")
        widgets[0].invoke() #starting questionare of "fällige" vocables
        #MyGUI.root.mainloop()
        self.Questionare_Fälligkeit(
            MyGUI,
            ["dTest1-1F", "", "Kommentar: testKommentar", "Dies ist Vokabel 1/4 der Session"],
            1,
            ["sTest1-1F"],
            ["sTest1-1F"],
            ["#50AA50"],
            [2, 1, 1],
            0
        )
        self.Questionare_Fälligkeit(
            MyGUI,
            ["dTest1-3F", "", "Kommentar: testKommentar", "Dies ist Vokabel 2/4 der Session"],
            3,
            ["sTest3-1F-B"],
            ["sTest3-1F-A", "sTest3-1F-B", "sTest3-1F-C"],
            ["#FF0000", "#50AA50", "#FF0000"],
            [6, 1, 3],
            1
        )
        self.Questionare_Fälligkeit(
            MyGUI,
            ["dTest2-1F-A", "dTest2-1F-B", "", "Dies ist Vokabel 3/4 der Session"],
            1,
            [""],
            ["sTest1-2F"],
            ["#FF0000"],
            [15, 1, 7],
            2
        )
        self.Questionare_Fälligkeit(
            MyGUI,
            ["dTest4-4F-A", "dTest4-4F-B", "dTest4-4F-C", "dTest4-4F-D", "", "Dies ist Vokabel 4/4 der Session"],
            4,
            ["#"],
            ["sTest4-4F-A", "sTest4-4F-B", "sTest4-4F-C", "sTest4-4F-D"],
            ["#50AA50", "#50AA50", "#50AA50", "#50AA50"],
            [61, 1, 30],
            0
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

        #MyGUI.root.mainloop()

    def Check_EndSession_Labels(self, GUI, labels):
        widgets = GUI.frame[0].winfo_children()
        self.assertEqual(widgets[0].cget("text"), labels[0])
        self.assertEqual(widgets[2].cget("text"), labels[1])
        self.assertEqual(widgets[5].cget("text"), labels[2])
        self.assertEqual(widgets[6].cget("text"), labels[3])
        self.assertEqual(widgets[7].cget("text"), labels[4])
        self.assertEqual(widgets[8].cget("text"), labels[5])


    def Questionare_Fälligkeit(self, GUI, Labels_Presented, no_of_entries, Entries, results, colors, delays, delay_idx):
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
        widgets = GUI.Frame_Buttons_delay.winfo_children()
        for widget, delay in zip(widgets, delays):
            self.assertEqual(widget.cget("text"), "+" + str(delay) + "Tage")
        widgets = GUI.Frame_Buttons_delay.winfo_children()
        current_idx = int(GUI.Selector.idx)
        widgets[delay_idx].invoke()
        NewDate = dt.today() + dtt.timedelta(delays[delay_idx])
        self.assertEqual(GUI.vocables[current_idx].content["answers"]["Andreas"]["NextTime"], NewDate.strftime("%Y-%m-%d"))





if __name__ == '__main__':
    unittest.main()
