import os
import json
from datetime import datetime as dt
import datetime as dtt

TestData = []
NextTime = dt.today() + dtt.timedelta(1)
TestData.append({
        "spanisch": ["sTest1-1R"], "deutsch": ["dTest1-1R"], "kommentar": "Erster Eintrag",
        "Andreas": {"last_stop": 8}, "Christa": {"last_stop": 2},
        "answers": {
            "Andreas": {"datetime": [""], "answer": [""], "delay": [100], "correctness": ["Richtig"], "NextTime": NextTime.strftime("%Y-%m-%d")},
            "Christa": {"datetime": [""], "answer": [""], "delay": [100], "correctness": ["Richtig"], "NextTime": NextTime.strftime("%Y-%m-%d")}
        }
    })
NextTime = dt.today() + dtt.timedelta(7)
TestData.append({
        "spanisch": ["sTest3-1R-A", "sTest3-1R-B", "sTest3-1R-C"], "deutsch": ["dTest1-3R"], "kommentar": "testKommentar",
        "answers": {
            "Andreas": {"datetime": [""], "answer": [""], "delay": [100], "correctness": ["Richtig"], "NextTime": NextTime.strftime("%Y-%m-%d")},
            "Christa": {"datetime": [""], "answer": [""], "delay": [100], "correctness": ["Richtig"], "NextTime": NextTime.strftime("%Y-%m-%d")}
        }
    })
NextTime = dt.today() + dtt.timedelta(30)
TestData.append({
        "spanisch": ["sTest1-2R"], "deutsch": ["dTest2-1R-A", "dTest2-1R-B"], "kommentar": "",
        "answers": {
            "Andreas": {"datetime": [""], "answer": [""], "delay": [100], "correctness": ["Richtig"], "NextTime": NextTime.strftime("%Y-%m-%d")},
            "Christa": {"datetime": [""], "answer": [""], "delay": [100], "correctness": ["Richtig"], "NextTime": NextTime.strftime("%Y-%m-%d")}
        }
    })
NextTime = dt.today() + dtt.timedelta(360)
TestData.append({
        "spanisch": ["sTest4-4R-A", "sTest4-4R-B", "sTest4-4R-C", "sTest4-4R-D"], "deutsch": ["dTest4-4R-A", "dTest4-4R-B", "dTest4-4R-C", "dTest4-4R-D"], "kommentar": "",
        "answers": {
            "Andreas": {"datetime": [""], "answer": [""], "delay": [100], "correctness": ["Richtig"], "NextTime": NextTime.strftime("%Y-%m-%d")},
            "Christa": {"datetime": [""], "answer": [""], "delay": [100], "correctness": ["Richtig"], "NextTime": NextTime.strftime("%Y-%m-%d")}
        }
    })
NextTime = dt.today() + dtt.timedelta(0)
TestData.append({
        "spanisch": ["sTest1-1F"], "deutsch": ["dTest1-1F"], "kommentar": "erste fällig",
        "answers": {
            "Andreas": {"datetime": [""], "answer": [""], "delay": [1], "correctness": ["Richtig"], "NextTime": NextTime.strftime("%Y-%m-%d")},
            "Christa": {"datetime": [""], "answer": [""], "delay": [1], "correctness": ["Richtig"], "NextTime": NextTime.strftime("%Y-%m-%d")}
        }
    })
NextTime = dt.today() + dtt.timedelta(-1)
TestData.append({
        "spanisch": ["sTest3-1F-A", "sTest3-1F-B", "sTest3-1F-C"], "deutsch": ["dTest1-3F"], "kommentar": "testKommentar",
        "answers": {
            "Andreas": {"datetime": [""], "answer": [""], "delay": [5], "correctness": ["Richtig"], "NextTime": NextTime.strftime("%Y-%m-%d")},
            "Christa": {"datetime": [""], "answer": [""], "delay": [5], "correctness": ["Richtig"], "NextTime": NextTime.strftime("%Y-%m-%d")}
        }
    })
NextTime = dt.today() + dtt.timedelta(-7)
NextTime2 = dt.today() + dtt.timedelta(+7)
TestData.append({
        "spanisch": ["sTest1-2F"], "deutsch": ["dTest2-1F-A", "dTest2-1F-B"], "kommentar": "nur fällig bei Andreas",
        "answers": {
            "Andreas": {"datetime": [""], "answer": [""], "delay": [7], "correctness": ["Richtig"], "NextTime": NextTime.strftime("%Y-%m-%d")},
            "Christa": {"datetime": [""], "answer": [""], "delay": [7], "correctness": ["Richtig"], "NextTime": NextTime2.strftime("%Y-%m-%d")}
        }
    })
NextTime = dt.today() + dtt.timedelta(-30)
TestData.append({
        "spanisch": ["sTest4-4F-A", "sTest4-4F-B", "sTest4-4F-C", "sTest4-4F-D"], "deutsch": ["dTest4-4F-A", "dTest4-4F-B", "dTest4-4F-C", "dTest4-4F-D"], "kommentar": "",
        "answers": {
            "Andreas": {"datetime": [""], "answer": [""], "delay": [30], "correctness": ["Richtig"], "NextTime": NextTime.strftime("%Y-%m-%d")},
            "Christa": {"datetime": [""], "answer": [""], "delay": [30], "correctness": ["Richtig"], "NextTime": NextTime.strftime("%Y-%m-%d")}
        }
    })
with open(os.path.dirname(os.path.abspath(__file__)) + "\Testdata.json", 'w') as fp:
    json.dump(TestData, fp, indent=4, ensure_ascii=False)
