import unittest
import Vokabeltrainer2 as VT

exec(open("./CreateTestData.py").read())

class MyTestCase(unittest.TestCase):
    def test_something(self):
        MyGUI = VT.MyGUI()
        MyGUI.testmode = True
        MyGUI.Create_Buttons()
        widgets = MyGUI.frameButtons.winfo_children()
        self.assertEqual(widgets[0].cget("text"), "Lektion auswählen")
        widgets[0].invoke()
        widgets = MyGUI.frameButtons.winfo_children()
        self.assertEqual(widgets[0].cget("text"), "Weiter")
        MyGUI.RadioBtns["mode"].set("Nach Reihenfolge")
        MyGUI.RadioBtns["language"].set("deutsch")
        MyGUI.RadioBtns["user selection"].set("Andreas")

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
