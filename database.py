import sqlite3
from datetime import datetime as dt
from VT_logger import logger
import random

class Database:
    def __init__(self, path):
        if path == "":
            path = "database2.db"
        self.path = path
        self.conn = sqlite3.connect(path)
        self.c = self.conn.cursor()
        self.c.execute("SELECT name "
                       "FROM sqlite_master "
                       "WHERE type='table' AND name='vocables'")
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
                           last_stop integer
                           )""")
            self.conn.commit()

    def convert_JSON(self, vocables):
        logger.info("Converting from JSON to MySQL DB")
        for user in vocables[0].content["answers"]:
            logger.debug("Creating Data for user: " + user)
            self.add_lesson(user, "Alles", range(1, 1+len(vocables)), vocables[0].content[user]["last_stop"])
        logger.debug("finished creation of user tables")
        user_answers = {}
        for vocable in vocables:
            logger.debug("Adding Vocable: " + ", ".join(vocable.content["deutsch"]))
            self.add_vocable(", ".join(vocable.content["deutsch"]),
                             ", ".join(vocable.content["spanisch"]),
                             vocable.content["kommentar"])
            logger.debug("Finding vocID of the vocable")
            vocID = self.find_vocable(", ".join(vocable.content["deutsch"]),
                                      ", ".join(vocable.content["spanisch"]),
                                      vocable.content["kommentar"])
            logger.debug("Found! VocID: " + str(vocID))
            for user in vocable.content["answers"]:
                if "NextTime" in vocable.content["answers"][user]:
                    for idx in range(len(vocable.content["answers"][user]["delay"])):
                        index = -1 - idx  # start checking for delay > 0 in reverse order
                        if vocable.content["answers"][user]["delay"][index] > 0:
                            logger.debug("updating table of " + user + " at vocID " + str(vocID)
                                         + " to show a delay of "
                                         + str(vocable.content["answers"][user]["delay"][index]))
                            self.set_lesson_delay(user,
                                                  "Alles",
                                                  vocID[0][0],
                                                  vocable.content["answers"][user]["delay"][index],
                                                  vocable.content["answers"][user]["NextTime"])
                            break
                        logger.debug("Did not find a delay > 0 on vocID " + str(vocID[0][0]) + " for user " + user)
                # logger.debug("Adding previous answers to the DB")
                for idx in range(len(vocable.content["answers"][user]["delay"])):
                    if user not in user_answers:
                        user_answers[user]=[]
                    try:
                        user_answers[user].append((vocID[0][0],
                                   ", ".join(vocable.content["answers"][user]["answer"][idx]),
                                   vocable.content["answers"][user]["datetime"][idx],
                                   vocable.content["answers"][user]["correctness"][idx]))
                    except:
                        logger.warning("corrupted data on Answer: "
                                       + ", ".join(vocable.content["deutsch"]) + ", " + user)
        for user in vocables[0].content["answers"]:
            self._check_user(user)
            self.c.executemany("INSERT INTO {}_answertable "
                               "VALUES (?, ?, ?, ?)".format(user),
                               user_answers[user])


### Answer Tables

    def _check_user(self, user):
        self.c.execute("SELECT name "
                       "FROM sqlite_master "
                       "WHERE type='table' AND name='{}_answertable'".format(user))
        if len(self.c.fetchall()) == 0:
            self.c.execute("""CREATE TABLE {}_answertable (
                            vocID integer,
                            answer text,
                            datetime integer,
                            correctness text
                            )""".format(user))
            self.conn.commit()

    def add_answer(self, user, vocID, answer, datetime, correctness):
        self._check_user(user)
        self.c.execute("INSERT INTO {}_answertable "
                       "VALUES (:vocID, :answer, :datetime, :correctness)".format(user),
                       {'answer': answer, 'datetime': datetime, 'correctness': correctness, "vocID": str(vocID)})
        self.conn.commit()

    def read_answer_by_vocID(self, user, vocID):
        self.c.execute("SELECT * "
                       "FROM {}_answertable "
                       "WHERE vocID = :vocID".format(user),
                       {'vocID': vocID})
        return self.c.fetchall()

    def set_answer_Tippfehler(self, user, datetime):
        self.c.execute("UPDATE {}_answertable "
                       "SET answer = 'Tippfehler', correctness = 'Richtig' "
                       "WHERE datetime = :datetime".format(user),
                       {'datetime': datetime})
        self.conn.commit()

### Vocable Table

    def add_vocable(self, deutsch, spanisch, kommentar):
        self.c.execute("SELECT * "
                       "FROM vocables "
                       "WHERE deutsch=:deutsch AND spanisch=:spanisch AND kommentar=:kommentar",
                       {'deutsch': deutsch,
                        'spanisch': spanisch,
                        'kommentar': kommentar})
        if len(self.c.fetchall()) == 0:
            self.c.execute("INSERT INTO vocables (deutsch, spanisch, kommentar) "
                           "VALUES (:deutsch, :spanisch, :kommentar)",
                           {'deutsch': deutsch,
                            'spanisch': spanisch,
                            'kommentar': kommentar})
            self.conn.commit()

    def find_vocable(self, deutsch, spanisch, kommentar):
        if not deutsch:
            deutsch = "%"
        if not spanisch:
            spanisch = "%"
        if not kommentar:
            kommentar = "%"
        self.c.execute("SELECT * "
                       "FROM vocables "
                       "WHERE deutsch LIKE :deutsch AND spanisch LIKE :spanisch AND kommentar LIKE :kommentar",
                       {'deutsch': "%" + deutsch + "%",
                        'spanisch': "%" + spanisch + "%",
                        'kommentar': "%" + kommentar + "%"})
        return self.c.fetchall()

    def read_vocable_byID(self, ID):
        self.c.execute("SELECT * "
                       "FROM vocables "
                       "WHERE vocID=:vocID",
                       {'vocID': ID})
        return self.c.fetchall()

    def delete_vocable(self, ID):
        self.c.execute("DELETE FROM vocables "
                       "WHERE vocID = :ID",
                       {'ID': ID})
        self.conn.commit()

    def set_vocable(self, vocID, deutsch, spanisch, kommentar):
        self.c.execute("UPDATE vocables "
                       "SET deutsch = :deutsch, spanisch = :spanisch, kommentar = :kommentar "
                       "WHERE vocID = :vocID",
                       {'deutsch': deutsch,
                        'spanisch': spanisch,
                        'kommentar': kommentar,
                        'vocID': vocID})
        self.conn.commit()

### Lessons Table (all lessons)

    def add_lesson(self, user, lesson, IDs, last_stop):
        self.c.execute("SELECT name "
                       "FROM sqlite_master "
                       "WHERE type='table' AND name='{}_lesson_{}'".format(user, lesson))
        if len(self.c.fetchall()) == 0:
            self.c.execute("""CREATE TABLE {}_lesson_{} (
                           vocIDref integer,
                           delay integer,
                           next_time text
                           )""".format(user, lesson))
            self.conn.commit()
            self.c.execute("INSERT INTO lessons "
                           "VALUES (:user, :lesson, :last_stop)",
                           {"last_stop": last_stop, "user": user, "lesson": lesson})
        else:
            print("The lesson you tried to create exists already!")
            return False
        new_entries = []
        [new_entries.append((ID, 1, dt.now().strftime("%Y-%m-%d"))) for ID in IDs]
        self.c.executemany("INSERT INTO {}_lesson_{} "
                           "VALUES (?, ?, ?)".format(user, lesson),
                           new_entries)

    def set_lessons_last_stop(self, user, lesson, last_stop):
        self.c.execute("UPDATE lessons "
                       "SET last_stop= ? "
                       "WHERE user = ? and name = ?",
                       (last_stop, user, lesson))
        self.conn.commit()

### Individual lesson tables

    def add_lessons_entry(self, user, lesson, vocID, NextTime):
        """ new lesson entries should be placed in random locations.
        To do that quickly, a random entry is replaced by the new one, and the old one is added to the end of the table
        This is done to prevent all new entries to cluster at the end of a table"""
        all_IDs = self.read_lesson_vocIDs(user, lesson)
        new_entry_loc = random.randint(1, len(all_IDs))
        old_entry = self.read_lessons_entry_byVocID(user, lesson, new_entry_loc)
        self.c.execute("UPDATE {}_lesson_{} "
                       "SET vocIDref = :vocID, delay = 1, next_time = :NextTime "
                       "WHERE rowid = :new_entry_loc".format(user, lesson),
                       {"new_entry_loc": new_entry_loc,
                        'vocID': vocID,
                        'NextTime': NextTime})
        self.c.execute("INSERT INTO {}_lesson_{} "
                       "(vocIDref, delay, next_time) "
                       "VALUES (:vocID, :delay, :NextTime)".format(user, lesson),
                       {"vocID": old_entry[0][0],
                        "delay": old_entry[0][1],
                        "NextTime": old_entry[0][2]})
        self.conn.commit()
        logger.debug("Added new entry in user's lesson table")


    def read_lesson_vocIDs(self, user, lesson):
        self.c.execute("SELECT vocIDref "
                       "FROM {}_lesson_{} "
                       "WHERE vocIDref > 0".format(user, lesson))
        return self.c.fetchall()

    def read_lessons_entry_byVocID(self, user, lesson, ID):
        self.c.execute("SELECT * "
                       "FROM {}_lesson_{} "
                       "WHERE vocIDref = :ID".format(user, lesson),
                       {'ID': ID})
        return self.c.fetchall()

    def read_lesson_last_stop(self, user, lesson):
        return self.c.execute("SELECT last_stop "
                              "FROM lessons "
                              "WHERE user=:user AND name=:lesson",
                              {'user': user, 'lesson': lesson}).fetchall()

    def set_lesson_delay(self, user, lesson, rowid, delay, next_time):
        self.c.execute("UPDATE {}_lesson_{} "
                       "SET delay = :delay , next_time = :next_time "
                       "WHERE rowid = {}".format(user, lesson, str(rowid)),
                       {'delay': delay, 'next_time': next_time})
        self.conn.commit()

    def delete_lesson_entry_byVocID(self, user, lesson, ID):
        self.c.execute("DELETE FROM {}_lesson_{} "
                       "WHERE vocIDref = :ID".format(user, lesson),
                       {'ID': ID})
        self.conn.commit()







if __name__ == "__main__":
    path = "test.db"
    db = Database(path)
    db.set_answer_Tippfehler('Christa', 'today')
    db.add_answer("Christa", 4, "unique", "today", "Falsch")
    db.add_lesson('Andreas', 'Alles',[1,2,3,4,5], 2)
    db.set_lessons_last_stop('Andreas', 'Alles', 4)
    db.add_vocable("deutsch", "spanisch", "kommentar")
    db.set_vocable(1, "new", "new2", "new3")
    db.add_lessons_entry("Andreas", "Alles", 5, "tomorrow")
