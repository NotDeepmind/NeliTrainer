#todo adapt SQL db here too
from database import Database
from VT_logger import logger

class ChangeManagement:
    def __init__(self):
        self.IDs = []
        self.idx = 0
        self.OrigEntires = []
        self.NewEntry = {}

    def Search (self, deutsch, spanisch, kommentar, path):
        self.OrigEntires = []
        self.idx = 0
        logger.info("Searching for " + deutsch + "; " + spanisch + "; " + kommentar)
        db = Database(path)
        results = db.find_vocable(deutsch, spanisch, kommentar)
        for result in results:
            self.OrigEntires.append({
                'vocID': result[0],
                'deutsch': result[1],
                'spanisch': result[2],
                'kommentar': result[3],
            })
        self.IDs = range(len(self.OrigEntires))

    def next(self):
        self.idx += 1
        if self.idx > len(self.IDs)-1:
            self.idx = 0

    def previous(self):
        self.idx -= 1
        if self.idx < 0:
            self.idx = len(self.IDs) - 1

    def ChangedEntries(self, deutsch, spanisch, kommentar, path):
        db = Database(path)
        logger.info("Saving changed on vocID: " + str(self.OrigEntires[self.idx]["vocID"]))
        logger.debug("New contents are:")
        logger.debug("german: " + deutsch + ", spanisch: " + spanisch + ", comment: " + kommentar)
        db.set_vocable(self.OrigEntires[self.idx]["vocID"], deutsch, spanisch, kommentar)
