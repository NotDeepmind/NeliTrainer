# NeliTrainer
Dies ist ein privater Vokabeltrainer.
Es wird ein Vokabular gepflegt, in dem Einträge vorgenommen sind für deutsche Übersetzung, spanische Übersetzung und Kommentare.
Dabei können beliebig viele deutsche Begriffe mit beliebig vielen spanischen verknüpft werden. Kommentare dienen dazu, ggfls. die Wörter zu verdeutlichen, beispielsweise kann "kurz" im metrischen oder im temporalen Kontext gemeint sein. Beim üben der Vokabeln kann die vorgegebene Sprache gewählt werden, in der jeweils anderen muss dann geantwortet werden. Dabei werden stets alle Begriffe einzeln abgefragt, nach dem Prüfen der Eingabe werden richtige Begriffe in grün und falsch eingegebene Begriffe in rot dargestellt.


Um mit dem Training zu beginnnen, muss zunächste eine Datenbank ausgewählt werden (beispielsweise die Example_Data.json auf diesem repository). Daraufhin muss einer von 3 Benutzern ausgewählt werden (Andreas, Christa, gemeinsam). Zusätzlich zur Wahl der Sprache kann aus 2 verschiedenen Modi gewählt und das Training begonnen werden.

Nach Reihenfolge: Hier muss zusätzlich eine maximale Anzahl von Vokabeln eingegeben werden. In diesem Modus wird die Liste aus Vokabeln einfach der Reihe nach abgefragt. Sobald die maximale Anzahl von Vokabeln beantwortet oder die Session vorzeitig beendet wurde, erscheint eine Übersicht über die Performance in der Session. Hier können alle falsch beantworteten Vokabeln erneut trainiert werden, und diese Schleife bei Bedarf so oft wiederholt werden bis sämtlich Vokabeln einmal richtig beantwortet wurden. Beim Speichern der Ergebnisse wird sich die Position in der Liste der Vokabeln gemerkt und bei der nächsten Session entsprechend in der Liste fortgesetzt. Ist das Ende der Vokabel-Liste erreicht, wird von vorne begonnen.

Nach Fälligkeit: In diesem Modus werden Vokabeln trainiert und nach dem beantworten einer Vokabel, wird vom Benutzer ein Intervall über die entsprechenden Buttons gewählt. Nach Ablauf des Intervalls gilt die Vokabel erneut als "fällig", beim jeweiligen Start des Modus' prüft das Programm alle Vokabeln auf Fälligkeit und fragt dann die Vokabeln des Tages ab. Daher kann in diesem Modus verstärkt die schwierigen Vokabeln gelernt werden, und zum allgemeinenen Vertiefen anschließend noch nach Reihenfolge gelernt werden.

Sonstige Features:
- Nach dem Beantworten einer Vokabel kann mit dem Button "Tippfehler" auch eine falsche Beantwortung für die abschließende Auswertung als richtig gespeichert werden.
- Während der Abfrage kann durch die Eingabe von "#" in einem der Antwort-Felder die Vokabel automatisch als vollständig richtig eingegeben werden. Das #-Symbol zählt als wären alle Antworten vollständig richtig.
- Die gegebenen Antworten, die Richtigkeit dieser Antworten sowie der Zeitpunkt und ggfls. das delay werden bei jeder Antwort gespeichert. Diese Daten werden in der aktuellen Version nur gesammelt und können zu einem späteren Zeitpunkt für eine Auswertung genutzt werden.
- Alle Einträge in der Datenbank können nach dem Laden des Files über den Button "Einträge ändern" angepasst oder vollständig gelöscht werden.
- Weitere Einträge können in Form einer TSV-Datei (tabulator-separated values) eingeladen werden. Die TSV kann mithilfe von üblichen 3rd Party Vokabularen aufgebaut werden, bspw. über PONS.de. Beim hinzufügen von Vokabeln wird standard-mäßig auf doppelte Einträge geprüft und nur einzigartige Einträge zugelassen.
- Falls gewünscht können die Vokabeln auch als TSV exportiert werden, um Kompatibilität mit anderen Programmen zu ermöglichen.
