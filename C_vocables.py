from datetime import datetime as dt
import datetime as dtt
from database import Database
from VT_logger import logger, exceptionHandling

class C_vocables:
    def __init__(self, VocabelEntry):
        self.content = VocabelEntry

    def AddDelay(self, user, delay, mode, path):
        db = Database(path)
        TimeToAskAgain = dt.today() + dtt.timedelta(days=delay)
        if mode == "nach Fälligkeit":
            db.set_lesson_delay(user, 'Alles', self.content['vocID'], delay, TimeToAskAgain.strftime("%Y-%m-%d"))
            self.content['NextTime'] = TimeToAskAgain.strftime("%Y-%m-%d")
            logger.info('Setting the new NextTime to ' + TimeToAskAgain.strftime("%Y-%m-%d"))

    def report(self):
        print(self.content)

    def EnterResults(self, Answers, correctness, user, path):
        db = Database(path)
        logger.info('Saving Answer to Database..')
        answer_datetime = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        db.add_answer(user, self.content['vocID'], ', '.join(Answers), answer_datetime, correctness)
        return answer_datetime
