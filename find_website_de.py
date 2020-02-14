# coding=utf-8

# =============================================================================
# Website Finder
# =============================================================================
#
# A function returning the homepage of the website of a media
#


import re
import json
import csv
import sys

from tqdm import tqdm

csv.field_size_limit(sys.maxsize)


dic_homepage = {"Hannoversche Allgemeine Zeitung Online": "www.haz.de",
                "Nürnberger Nachrichten": "www.nordbayern.de",
                "ZEIT Campus": "www.zeit.de/campus",
                "Handelsblatt Live App": "www.handelsblatt.com",
                "Süddeutsche Zeitung": "www.sueddeutsche.de",
                "BILD Dresden": "www.bild.de/regional/dresden/dresden-regional",
                "bild.de": "www.bild.de",
                "BILD Leipzig": "www.bild.de/regional/leipzig/leipzig-regional",
                "Der Spiegel": "www.spiegel.de",
                "BILD Köln": "www.bild.de/regional/koeln/koeln-regional",
                "Hannoversche Allgemeine Zeitung": "www.haz.de",
                "BILD Plus": "www.bild.de/bild-plus/bildplus-startseite",
                "BILD Hannover": "www.bild.de/regional/hannover",
                "DIE ZEIT": "www.zeit.de/",
                "Kölner Stadtanzeiger": "www.ksta.de",
                "Kölner Stadt-Anzeiger": "www.ksta.de",
                "Spiegel Plus": "www.spiegel.de/plus",
                "Frankfurter Rundschau": "www.fr.de",
                "Handelsblatt Online": "www.handelsblatt.com",
                "BILD Thüringen": "www.bild.de/regional/",
                "Focus": "www.focus.de/",
                "WELT online": "www.welt.de/",
                "Rheinische Post Online": "rp-online.de/",
                "Die Welt": "www.welt.de/",
                "BILD Mecklenburg-Vorpommern": "www.bild.de/regional/mecklenburg-vorpommern/",
                "Südwest Presse": "www.swp.de/",
                "S��dwest Presse": "www.swp.de/",
                "BILD am Sonntag": "www.bild.de/bild-am-sonntag/",
                "BILD Stuttgart": "www.bild.de/regional/stuttgart/stuttgart-regional/",
                "BILD Sachsen-Anhalt": "www.bild.de/regional/sachsen-anhalt/sachsen-anhalt/",
                "BILD Düsseldorf": "www.bild.de/regional/duesseldorf/duesseldorf-regional/",
                "BILD Frankfurt": "www.bild.de/regional/frankfurt/frankfurt-regional/",
                "Stern": "www.stern.de/",
                "BILD Rhein-Neckar": "www.bild.de/",
                "BILD Magdeburg": "www.bild.de/",
                "BILD Halle": "www.bild.de/",
                "BILD Ruhrgebiet": "www.bild.de/regional/ruhrgebiet/ruhrgebiet-regional/",
                "Focus Online": "www.focus.de/",
                "BILD Mainz-Wiesbaden": "www.bild.de/",
                "BILD Saarland": "www.bild.de/",
                "Rheinische Post": "rp-online.de/",
                "taz - die tageszeitung": "taz.de/",
                "BILD Rhein-Main": "www.bild.de/",
                "Welt am Sonntag": "www.welt.de/weltamsonntag/",
                "Spiegel Online": "www.spiegel.de/",
                "Handelsblatt": "www.handelsblatt.com/",
                "BILD Berlin-Brandenburg": "www.bild.de/",
                "BILD München": "www.bild.de/",
                "Süddeutsche Zeitung Online": "www.sueddeutsche.de/",
                "ZEIT online": "www.zeit.de/",
                "ZEIT Magazin": "www.zeit.de/zeit-magazin/",
                "BILD Hamburg": "www.bild.de/",
                "BILD": "www.bild.de/"
                }
# site:domain.com/path ("titre article 1" OR "titre article 2")
websites_excluded = {"Audio Video Foto Bild",
"ZEIT Hamburg",
"ZEIT Schweiz",
"Handelsblatt 10",
"ZEIT Österreich",
"ZEIT im Osten",
"Handelsblatt Magazin",
"ZEITmagazin",
"WirtschaftsWoche Online",
"ZEIT Geschichte",
"ZEIT Wissen"}

entries = set()

# filepath = "small_extract.csv"
filepath = "factiva_DE_final.csv"

media = set()
csv_HP = []

with open("article_with_AN_DE.csv", "w", newline="", encoding="utf-8") as new_csv:
    with open(filepath, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        csv_writer = csv.writer(new_csv, delimiter=",")

        first_row = ["title", "date", "media", "homepage", "AN"]
        csv_writer.writerow(first_row)

        next(csv_reader)  # let the first line
        for line in tqdm(csv_reader, total=770967):
            # media.add(line[24])
            if(line[24] not in websites_excluded and line[3]+line[8] not in entries):
                try:
                    newline = []
                    AN = line[15].split(" ")[1]
                    newline.extend(
                        [line[3], line[8], line[24], dic_homepage[line[24]],  AN])
                    csv_writer.writerow(newline)
                    entries.add(line[3]+line[8])
                except:
                    print("could add this article to csv: ", line[24])
