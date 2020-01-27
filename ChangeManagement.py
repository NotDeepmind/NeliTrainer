class ChangeManagement:
    def __init__(self):
        self.vokabeln = []
        self.IDs = []
        self.idx = 0

    def AddVokabeln(self, list):
        self.vokabeln = list

    def Search (self, deutsch, spanisch, kommentar):
        ID = 0
        found = []
        for entry in self.vokabeln:
            match = 0
            if deutsch == "":
                match += 1
            if spanisch == "":
                match += 1
            if kommentar == "":
                match += 1
            for word in entry["deutsch"]:
                if deutsch in word and deutsch != "":
                    match += 1
                    break
            for word in entry["spanisch"]:
                if spanisch in word and spanisch != "":
                    match += 1
                    break
            for word in entry["kommentar"]:
                if kommentar in word and kommentar != "":
                    match += 1
                    break
            if match == 3:
                found.append(ID)
                print(match)

            ID += 1
        self.IDs = found

    def display(self, FoundEntries):
        id = 0
        fields = ["deutsch", "spanisch", "kommentar"]
        for field in fields:
            if field != "kommentar":
                oldEntry = ""
                for word in self.vokabeln[self.IDs[self.idx]][field]:
                    oldEntry = oldEntry + word + ","
                oldEntry = oldEntry[:-1]
            else:
                oldEntry = self.vokabeln[self.IDs[self.idx]][field]
            FoundEntries[id].delete(0, "end")
            FoundEntries[id].insert(0, oldEntry)
            id += 1

    def next(self, FoundEntries):
        self.idx += 1
        if self.idx > len(self.IDs)-1:
            self.idx = 0
        self.display(FoundEntries)

    def previous(self, FoundEntries):
        self.idx -= 1
        if self.idx < 0:
            self.idx = len(self.IDs) - 1
        self.display(FoundEntries)



