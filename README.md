# Willkommen beim Grafikdeals - Grafikkartenpreis Scanner

Diese Code erlaub es die Webseiten verschiedener Händler nach Preisupdates und neuen Listings neuer Grafikkarten abzusuchen. 
Da ich mich entschieden habe das Projekt zu beenden möchte ich den Code veröffentlichen.


## Aufbau 
Besteht aus Crawlern, die auf die Webseite verschiedenster Händler angepasst wurden und einem Telegram Bot. Die Daten, die die 
Crawler sammeln werden zudem in einer MySQL Datenbank für z.B. die Einbindung in eine Webseite, oder eine weitere Datenverarbeitung
gespeichert. Die Verwendung einer MySQL Datendank ist in der aktuellen Version unerlässlich. Zudem benötigt der Code für die Webseiten 
einiger Händler einen Proxy.

## Ausführungshinweise
Um die Webseiter einiger Händler zu Crawlen ist die Installation von Chrome auf einer Maschine mit GUI, sowie die Nutzung eines passenden ChromeWebDrivers unerlässlich. Der Webdriver sollte in dem gleichen Verzeichnis wie die main.py Datei liegen.

# Nachwort
Ich möchte darauf hinweisen, dass im Code noch unbekannte Bugs liegen können und ich daher keine Verantwortung für die Verwendung des Codes übernehme. Der Code
ist für Menschen mit Erfahrung in Python Programmierung und einen verantwortungsvollen Umgang gedacht. 
