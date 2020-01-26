def ChangeManagement (deutsch, spanisch, kommentar, vokabeln):
    ID = 0
    found = []
    for entry in vokabeln:
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

        ID += 1

    return found