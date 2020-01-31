class C_selection:
    def __init__(self):
        self.IDs = -1 # das hier ist einfach ein zähler
        self.idx = -1   # das hier ist der entsprechende index nach der korrelationsliste, die in Entities abelegt werden kann/soll
                        # --> Entities[1] enthält die indices der fälligen vokabeln
        self.listID = 1 # listID 1 corresponds to mode "nach Fälligkeit"
                        # listID 0 corresponds to mode "nach Reihenfolge"
                        # listID > 1 corresponds to additional runs through wrong answered vocables
        self.Entities = []

    def NumbersOfEnteties(self, NumberOfEnteties):
        self.Entities.append(NumberOfEnteties)

    def NextEntity(self):
        self.IDs += 1
        print("About to ask next ListID " + str(self.listID) + " with the " + str(self.IDs) + "th entry")
        print("The current List of IDs contains " + str(len(self.Entities[self.listID])) + " Elements")
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
        print("Asking vocable >> " + vocables.vocables[self.idx]["deutsch"][0] + " << at ID " + str(self.idx))