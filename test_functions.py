import unittest
import functions
import os


exec(open("./CreateTestData.py").read())
TestData = [
    {
        "spanisch": [
            "sTest1-1R"
        ],
        "deutsch": [
            "dTest1-1R"
        ],
        "kommentar": "testKommentar",
        "answers": {
            "Andreas": {
                "datetime": [
                    ""
                ],
                "answer": [
                    ""
                ],
                "delay": [
                    100
                ],
                "correctness": [
                    "Richtig"
                ],
                "NextTime": "2020-05-09"
            },
            "Christa": {
                "datetime": [
                    ""
                ],
                "answer": [
                    ""
                ],
                "delay": [
                    100
                ],
                "correctness": [
                    "Richtig"
                ],
                "NextTime": "2020-05-09"
            }
        }
    },
    {
        "spanisch": [
            "sTest3-1R-A",
            "sTest3-1R-B",
            "sTest3-1R-C"
        ],
        "deutsch": [
            "dTest1-3R"
        ],
        "kommentar": "testKommentar",
        "answers": {
            "Andreas": {
                "datetime": [
                    ""
                ],
                "answer": [
                    ""
                ],
                "delay": [
                    100
                ],
                "correctness": [
                    "Richtig"
                ],
                "NextTime": "2020-02-09"
            },
            "Christa": {
                "datetime": [
                    ""
                ],
                "answer": [
                    ""
                ],
                "delay": [
                    100
                ],
                "correctness": [
                    "Richtig"
                ],
                "NextTime": "2020-02-09"
            }
        }
    },
    {
        "spanisch": [
            "sTest1-2R"
        ],
        "deutsch": [
            "dTest2-1R-A",
            "dTest2-1R-B"
        ],
        "kommentar": "",
        "answers": {
            "Andreas": {
                "datetime": [
                    ""
                ],
                "answer": [
                    ""
                ],
                "delay": [
                    100
                ],
                "correctness": [
                    "Richtig"
                ],
                "NextTime": "2020-01-31"
            },
            "Christa": {
                "datetime": [
                    ""
                ],
                "answer": [
                    ""
                ],
                "delay": [
                    100
                ],
                "correctness": [
                    "Richtig"
                ],
                "NextTime": "2020-01-31"
            }
        }
    },
    {
        "spanisch": [
            "sTest4-4R-A",
            "sTest4-4R-B",
            "sTest4-4R-C",
            "sTest4-4R-D"
        ],
        "deutsch": [
            "dTest4-4R-A",
            "dTest4-4R-B",
            "dTest4-4R-C",
            "dTest4-4R-D"
        ],
        "kommentar": "",
        "answers": {
            "Andreas": {
                "datetime": [
                    ""
                ],
                "answer": [
                    ""
                ],
                "delay": [
                    100
                ],
                "correctness": [
                    "Richtig"
                ],
                "NextTime": "2020-02-04"
            },
            "Christa": {
                "datetime": [
                    ""
                ],
                "answer": [
                    ""
                ],
                "delay": [
                    100
                ],
                "correctness": [
                    "Richtig"
                ],
                "NextTime": "2020-02-04"
            }
        }
    },
    {
        "spanisch": [
            "sTest1-1F"
        ],
        "deutsch": [
            "dTest1-1F"
        ],
        "kommentar": "testKommentar",
        "answers": {
            "Andreas": {
                "datetime": [
                    ""
                ],
                "answer": [
                    ""
                ],
                "delay": [
                    100
                ],
                "correctness": [
                    "Richtig"
                ],
                "NextTime": "2020-01-30"
            },
            "Christa": {
                "datetime": [
                    ""
                ],
                "answer": [
                    ""
                ],
                "delay": [
                    100
                ],
                "correctness": [
                    "Richtig"
                ],
                "NextTime": "2020-01-31"
            }
        }
    },
    {
        "spanisch": [
            "sTest3-1F-A",
            "sTest3-1F-B",
            "sTest3-1F-C"
        ],
        "deutsch": [
            "dTest1-3F"
        ],
        "kommentar": "testKommentar",
        "answers": {
            "Andreas": {
                "datetime": [
                    ""
                ],
                "answer": [
                    ""
                ],
                "delay": [
                    100
                ],
                "correctness": [
                    "Richtig"
                ],
                "NextTime": "2020-01-29"
            },
            "Christa": {
                "datetime": [
                    ""
                ],
                "answer": [
                    ""
                ],
                "delay": [
                    100
                ],
                "correctness": [
                    "Richtig"
                ],
                "NextTime": "2020-01-29"
            }
        }
    },
    {
        "spanisch": [
            "sTest1-2F"
        ],
        "deutsch": [
            "dTest2-1F-A",
            "dTest2-1F-B"
        ],
        "kommentar": "",
        "answers": {
            "Andreas": {
                "datetime": [
                    ""
                ],
                "answer": [
                    ""
                ],
                "delay": [
                    100
                ],
                "correctness": [
                    "Richtig"
                ],
                "NextTime": "2020-01-23"
            },
            "Christa": {
                "datetime": [
                    ""
                ],
                "answer": [
                    ""
                ],
                "delay": [
                    100
                ],
                "correctness": [
                    "Richtig"
                ],
                "NextTime": "2020-01-23"
            }
        }
    },
    {
        "spanisch": [
            "sTest4-4F-A",
            "sTest4-4F-B",
            "sTest4-4F-C",
            "sTest4-4F-D"
        ],
        "deutsch": [
            "dTest4-4F-A",
            "dTest4-4F-B",
            "dTest4-4F-C",
            "dTest4-4F-D"
        ],
        "kommentar": "",
        "answers": {
            "Andreas": {
                "datetime": [
                    ""
                ],
                "answer": [
                    ""
                ],
                "delay": [
                    100
                ],
                "correctness": [
                    "Richtig"
                ],
                "NextTime": "2019-02-04"
            },
            "Christa": {
                "datetime": [
                    ""
                ],
                "answer": [
                    ""
                ],
                "delay": [
                    100
                ],
                "correctness": [
                    "Richtig"
                ],
                "NextTime": "2019-02-04"
            }
        }
    }
]

class MyTestCase(unittest.TestCase):
    def test_SelectLecture(self):
        path, ReadData = functions.SelectLecture(os.path.dirname(os.path.abspath(__file__)) + "\Testdata.json")
        for id in range(len(TestData)):
            self.assertEqual(TestData[id], ReadData[id].content)


if __name__ == '__main__':
    unittest.main()
