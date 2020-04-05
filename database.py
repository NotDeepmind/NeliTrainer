import sqlite3
from datetime import datetime as dt

class Database:
    def __init__(self, path):
        if path == "":
            path = "database2.db"
        self.conn = sqlite3.connect(path)
        self.c = self.conn.cursor()
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vocables'")
        #print(len(self.c.fetchall()))
        if len(self.c.fetchall()) == 0:
            self.c.execute("""CREATE TABLE vocables (
                           vocID integer PRIMARY KEY AUTOINCREMENT,
                           deutsch text,
                           spanisch text,
                           kommentar text
                           )""")
            self.conn.commit()

        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lessons'")
        if len(self.c.fetchall()) == 0:
            self.c.execute("""CREATE TABLE lessons (
                           user text,
                           name text,
                           ids text,
                           last_stop integer
                           )""")
            self.conn.commit()


    def _check_user(self, user):
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{}_answertable'".format(user))
        if len(self.c.fetchall()) == 0:
            self.c.execute("""CREATE TABLE {}_answertable (
                            answer text,
                            datetime integer,
                            correctness text
                            )""".format(user))
            self.conn.commit()

    def add_answer(self, user, answer, datetime, correctness):
        self._check_user(user)
        self.c.execute("INSERT INTO {}_answertable VALUES (:answer, :datetime, :correctness)".format(user), {'answer': answer, 'datetime': datetime, 'correctness': correctness})



    def add_vocable(self, deutsch, spanisch, kommentar):
        self.c.execute("SELECT * FROM vocables WHERE deutsch=:deutsch AND spanisch=:spanisch AND kommentar=:kommentar", {'deutsch': deutsch, 'spanisch': spanisch, 'kommentar': kommentar})
        if len(self.c.fetchall()) == 0:
            self.c.execute("INSERT INTO vocables (deutsch, spanisch, kommentar) VALUES (:deutsch, :spanisch, :kommentar)", {'deutsch': deutsch, 'spanisch': spanisch, 'kommentar': kommentar})
            self.conn.commit()

    def find_vocable(self, deutsch, spanisch, kommentar):
        if not deutsch:
            deutsch = "%"
        if not spanisch:
            spanisch = "%"
        if not kommentar:
            kommentar = "%"
        self.c.execute("SELECT vocID FROM vocables WHERE deutsch LIKE :deutsch AND spanisch LIKE :spanisch AND kommentar LIKE :kommentar", {'deutsch': "%" + deutsch + "%", 'spanisch': "%" + spanisch + "%",
                                                                                                                                        'kommentar': "%" + kommentar + "%"})
        return self.c.fetchall()

    def delete_vocable(self, ID):
        self.c.execute("DELETE FROM vocables WHERE vocID = :ID", {'ID': ID})
        self.conn.commit()


    def add_lesson(self, user, lesson, IDs):
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{}_lesson_{}'".format(user, lesson))
        if len(self.c.fetchall()) == 0:
            self.c.execute("""CREATE TABLE {}_lesson_{} (
                           vocIDref integer,
                           delay integer,
                           next_time text
                           )""".format(user, lesson))
            self.conn.commit()
        else:
            print("The lesson you tried to create exists already!")
            return False
        for ID in IDs:
            self.c.execute("INSERT INTO {}_lesson_{} VALUES (:ID, 1, :date)".format(user, lesson), {"ID": ID, "date": dt.now().strftime("%Y-%m-%d")})
            self.conn.commit()

    def add_lesson_delay(self, user, lesson, rowid, delay, next_time):
        self.c.execute("UPDATE {}_lesson_{} SET delay = :delay , next_time = :next_time WHERE rowid = {}".format(user, lesson, str(rowid)), {'delay': delay, 'next_time': next_time})
        self.conn.commit()


    def merge_lesson(self):
        pass #todo build method to fuse lessons



if __name__ == "__main__":
    import functions
    from tkinter import filedialog
    import C_selection

    db = Database("")
    db.add_vocable("dtest", "stest", "kommtest")
    db.add_vocable("dtest2", "stest", "kommtest")
    db.add_vocable("dtest2", "stest2", "kommtest")
    db.add_vocable("dtest2", "stest2", "kommtest2")
    entry = db.find_vocable("dtest2", "", "")
    print(entry[0])
    db.add_answer("Andreas", "testanswer", "01-05-2020", "Richtig")
    #db.delete_vocable(entry[0][0])
    db.add_vocable("new last", "stest2", "kommtest2")
    entry = db.find_vocable("new", "", "")
    db.delete_vocable(entry[0][0])
    db.add_vocable("new last", "stest2", "kommtest2")
    db.add_lesson("Andreas", "Testlektion", range(10))


    selector = C_selection.C_selection()
    #path = filedialog.askopenfilename()
    #print(path)
    path = "C:/Users/Stefan/Desktop/Vokabeltrainer/Vokabeln bis 21 v1a.json"
    path, vocables, selector = functions.LoadData(path, selector)
    db2 = Database(path[:-4] + "db")
    for vocable in vocables:
        db2.add_vocable(", ".join(vocable.content["deutsch"]), ", ".join(vocable.content["spanisch"]), vocable.content["kommentar"])
        vocID = db2.find_vocable(", ".join(vocable.content["deutsch"]), ", ".join(vocable.content["spanisch"]), vocable.content["kommentar"])
        for user in vocable.content["answers"]:
            db2.add_lesson(user, "Alles", range(len(vocables)))
            try:
                print("updating table of " + user + " at vocID " + str(vocID) + " to show a delay of " + str(vocable.content["answers"][user]["delay"][-1]))
                db2.add_lesson_delay(user, "Alles", vocID[0][0], vocable.content["answers"][user]["delay"][-1], vocable.content["answers"][user]["NextTime"])
            except:
                if user != "gemeinsam":
                    print("Error during setting of NExtTime")
            #print("userloop working on " + user)
            for idx in range(len(vocable.content["answers"][user]["delay"])):
                try:
                    db2.add_answer(user,
                               ", ".join(vocable.content["answers"][user]["answer"][idx]),
                               vocable.content["answers"][user]["datetime"][idx],
                               vocable.content["answers"][user]["correctness"][idx]
                               )
                except:
                    print("corrupted data on Answer: " + ", ".join(vocable.content["deutsch"]) + ", " + user)
                #print(", ".join(vocable.content["deutsch"]) + ", " + user)
                #print(vocable.content["answers"][user]["correctness"][idx])