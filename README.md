# Git-Updates

Das Python Skript kann benutzt werden um automatisch alle Git Repositories in einem Ordner zu updaten. Man kann pullen, pushen, committen, cleanen und sich den letzten Commit anzeigen lassen.

Für die Benutzung werden Python >= 3.7, Git >= 1.7 und [GitPython](https://gitpython.readthedocs.io/en/stable/intro.html#installing-gitpython) benötigt.

## Verwendung

Das Skript muss standardmäßig im selben Ordner wie die Repositories liegen. Falls es in einem anderen Ordner liegen soll, kann der `dir` Parameter in der vorletzten Zeile angepasst werden um auf den Ordner mit den Repositories zu zeigen.

Die Korrekturen werden in einem separaten Order im Repository erwartet, welcher standardmäßig `Korrekturen` heißt. Die Korrekturen müssen alle mit einem vorgegebenen Präfix benannt sein, standardmäßig `korrektur_`, die Dateiendung ist egal. Beides kann ebenfalls in der vorletzten Zeile durch die Parameter `correction_dir` und `correction_file_prefix` angepasst werden.

Das Skript kann mit `python3` oder `python ` gestartet werden. Die Commands können etnweder direkt als Argument übergeben werden. Falls kein Argument übergeben wurde, oder es nicht erkannt wurde, kann man es nachträglich angeben.

Alle Outputs werden zusätzlich als Log in einem Ordner `_logs` gespeichert.

## pull

Hiermit können alle Repositories gepullt werden.

````
python git_updates.py pull
````

Folgende Outputs können ausgegeben werden:
- *Already up to date*
- *x file changed, y insertion(+), z deletions(-)*
- *Error: Conflict with committed files*
- *Error: Conflict with local files*
- *Error: No branch seems to be specified*

## commit

Hiermit kann eine Korrektur für eine Übung gestaged und committet werden. In dem Beispiel unten werden alle Dateien `Korrekturen/korrektur_03.*` committet. Als Commit-Message wird "Korrektur Übung XX" oder "Update Korrektur Übung XX" genommen.

````
python git_updates.py commit 03
````

Folgende Outputs können ausgegeben werden:

- *Committed korrektur_03.txt, korrektur_03.pdf*
- *Committed update for korrektur_03.txt, korrektur_03.pdf*
- *Already committed korrektur_03.txt, korrektur_03.pdf*
- *Already up to date: korrektur_03.txt, korrektur_03.pdf*
- *Nothing to commit was found*
- *Error: No folder named Korrekturen was found*

## push

Hiermit können alle Commits gepusht werden. 

````
python git_updates.py push
````

Folgende Outputs können ausgegeben werden:

- *Successful push*
- *Nothing to push*
- *Error: Conflicting changes*
- *Error: No branch seems to be specified*

## clean

Hiermit können alle nicht committeten Änderungen gelöscht werden, damit keine Konflikte beim Pullen und Pushen auftreten. Bevor die Änderungen gelöscht werden muss man die Aktion noch mit  `yes` bestätigen.

````
python git_updates.py clean
````

Folgende Outputs können ausgegeben werden:

- *Already clean*
- *Deleted untracked files*
- *Restored files*
- *Restored files and deleted untracked files*
- *Error: Merge in progress*
- *Error: No branch seems to be specified*

## show

Hiermit kann Zeitpunkt, Autor*in und Commit-Message des letzten Commits angezeigt werden. Das kann hilfreich sein um zu gucken, ob auch alle rechtzeitig abgegeben haben.

````
python git_updates.py show
````

Folgende Outputs können ausgegeben werden:

- *Mon Dec 6 21:53:10 2021, Sonja Studentin: LaTeX ergänzt*
- *No commits yet*

