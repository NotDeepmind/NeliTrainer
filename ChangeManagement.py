class ChangeManagement:
    def __init__(self):
        self.IDs = []
        self.idx = 0
        self.OrigEntires = []
        self.NewEntry = {}

    def Search (self, deutsch, spanisch, kommentar, vocables):
        ID = 0
        self.idx = 0
        found = []
        self.OrigEntires = []
        for vocable in vocables:
            match = 0
            if deutsch == "":
                match += 1
            if spanisch == "":
                match += 1
            if kommentar == "":
                match += 1
            for word in vocable.content["deutsch"]:
                if deutsch in word and deutsch != "":
                    match += 1
                    break
            for word in vocable.content["spanisch"]:
                if spanisch in word and spanisch != "":
                    match += 1
                    break
            if kommentar in vocable.content["kommentar"] and kommentar != "":
                match += 1
            if match == 3:
                found.append(ID)
                Entry_deutsch = ""
                Entry_spanisch = ""
                Entry_kommentar = ""
                for word in vocable.content["deutsch"]:
                    Entry_deutsch += word + ", "
                for word in vocable.content["spanisch"]:
                    Entry_spanisch += word + ", "
                Entry_kommentar = vocable.content["kommentar"]
                self.OrigEntires.append({"deutsch": Entry_deutsch[:-2], "spanisch": Entry_spanisch[:-2], "kommentar": Entry_kommentar, "ID": ID})
            ID += 1
        self.IDs = found

    def next(self):
        self.idx += 1
        if self.idx > len(self.IDs)-1:
            self.idx = 0

    def previous(self):
        self.idx -= 1
        if self.idx < 0:
            self.idx = len(self.IDs) - 1

    def ChangedEntries(self, deutsch, spanisch, kommentar):
        #separate function to take string from user entry and convert deutsch / spanisch to correct lists of entries
        LanguageEntries = [deutsch, spanisch]
        for i, Entry in zip(range(2), LanguageEntries):
            content = Entry.split(",")
            for j, word in zip(range(len(content)), content):
                if len(word) > 0:
                    while word[0] == " ": # remove starting / finishing spaces
                        word = word[1:]
                    while word[-1] == " ":
                        word = word[:-1]
                    content[j] = word
            LanguageEntries[i] = content
        self.NewEntry = {"deutsch": LanguageEntries[0], "spanisch" : LanguageEntries[1], "kommentar" : kommentar}

