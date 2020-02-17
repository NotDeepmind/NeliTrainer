class C_selection:
    def __init__(self):
        self.IDs = -1 # das hier ist einfach ein zähler
        self.idx = []   # das hier ist der entsprechende index nach der korrelationsliste, die in Entities abelegt werden kann/soll
                        # --> Entities[1] enthält die indices der fälligen vokabeln
        self.listID = -1 # listID 1 corresponds to mode "nach Fälligkeit"
                        # listID 0 corresponds to mode "nach Reihenfolge"
                        # listID > 1 corresponds to additional runs through wrong answered vocables
        self.Entities = []

    def NumbersOfEnteties(self, NumberOfEnteties):
        self.Entities.append(NumberOfEnteties)

    def NextEntity(self, mode, last_stop):
        #initiate correctly depending on mode
        if self.IDs == -1 and mode == "nach Reihenfolge" and len(self.Entities) == 2:
            self.listID = 0
            self.IDs = last_stop
        elif self.IDs == -1 and mode == "nach Fälligkeit" and len(self.Entities) == 2:
            self.listID = 1
            self.IDs = -1
        self.IDs += 1
        #restart if end of list is reached
        if self.IDs >= len(self.Entities[0]) and mode == "nach Reihenfolge":
            self.IDs = 0
        elif self.IDs >= len(self.Entities[-1]) and mode == "nach Fälligkeit":
            print("Trying to call more Entries than exist?!")
        self.idx = self.Entities[self.listID][self.IDs]