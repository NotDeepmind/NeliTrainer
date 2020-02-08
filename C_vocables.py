from datetime import datetime as dt
import datetime as dtt

class C_vocables:
    def __init__(self, VocabelEntry):
        self.content = VocabelEntry

    def AddDelay(self, user, delay, mode):
        TimeToAskAgain = dt.today() + dtt.timedelta(days=delay)
        if mode == "nach Fälligkeit":
            self.content["answers"][user]["NextTime"] = TimeToAskAgain.strftime("%Y-%m-%d")
        self.content["answers"][user]["delay"].append(delay)

    def report(self):
        print(self.content)

    def EnterResults(self, Answers, IntCorrects, user):
        if user in self.content["answers"]:
            pass
        else:
            self.content["answers"][user] = {}
            self.content["answers"][user]["datetime"] = []
            self.content["answers"][user]["answer"] = []
            self.content["answers"][user]["delay"] = []
            self.content["answers"][user]["correctness"] = []
        self.content["answers"][user]["datetime"].append(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.content["answers"][user]["answer"].append(Answers)
        if IntCorrects == len(Answers):
            self.content["answers"][user]["correctness"].append("Richtig")
        else:
            self.content["answers"][user]["correctness"].append("Falsch")

