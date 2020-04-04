import sqlite3

class Database:
    def __init__(self, path):
        if path == "":
            path = "database.db"
        self.conn = sqlite3.connect(path)
        self.c = self.conn.cursor()
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vocables'")
        #print(len(self.c.fetchall()))
        if len(self.c.fetchall()) == 0:
            self.c.execute("""CREATE TABLE vocables (
                           deutsch text,
                           spanisch text,
                           kommentar text
                           )""")
            self.conn.commit()

        # self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lessons'")
        # if len(self.c.fetchall()) == 0:
        #     self.c.execute("""CREATE TABLE vocables (
        #                    user text,
        #                    name text,
        #                    ids text,
        #                    last_stop integer
        #                    )""")
        #     self.conn.commit()


    def _check_user(self, user):
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='answertable_{}'".format(user))
        if len(self.c.fetchall()) == 0:
            self.c.execute("""CREATE TABLE answertable_{} (
                            answer text,
                            datetime integer,
                            correctness text
                            )""".format(user))
            self.conn.commit()

    def add_answer(self, user, answer, datetime, correctness):
        self._check_user(user)
        self.c.execute("INSERT INTO answertable_{} VALUES (:answer, :datetime, :correctness)".format(user), {'answer': answer, 'datetime': datetime, 'correctness': correctness})

    def add_vocable(self, deutsch, spanisch, kommentar):
        self.c.execute("SELECT * FROM vocables WHERE deutsch=:deutsch AND spanisch=:spanisch AND kommentar=:kommentar", {'deutsch': deutsch, 'spanisch': spanisch, 'kommentar': kommentar})
        if len(self.c.fetchall()) == 0:
            self.c.execute("INSERT INTO vocables VALUES (:deutsch, :spanisch, :kommentar)", {'deutsch': deutsch, 'spanisch': spanisch, 'kommentar': kommentar})
            self.conn.commit()

    def find_vocable(self, deutsch, spanisch, kommentar):
        if not deutsch:
            deutsch = "%"
        if not spanisch:
            spanisch = "%"
        if not kommentar:
            kommentar = "%"
        self.c.execute("SELECT rowid, * FROM vocables WHERE deutsch LIKE :deutsch AND spanisch LIKE :spanisch AND kommentar LIKE :kommentar", {'deutsch': "%" + deutsch + "%", 'spanisch': "%" + spanisch + "%",
                                                                                                                                        'kommentar': "%" + kommentar + "%"})
        return self.c.fetchall()



if __name__ == "__main__":
    db = Database("")
    db.add_vocable("dtest2", "stest2", "kommtest2")
    print(db.find_vocable("dtest2", "", ""))
    db.add_answer("Andreas", "testanswer", "01-05-2020", "Richtig")