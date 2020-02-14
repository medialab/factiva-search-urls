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
from tqdm import tqdm


dic_homepage = {"The Observer": "www.theguardian.com/observer",
                "People": "people.com",
                "Sunday Mail": "www.dailyrecord.co.uk/",
                "Scottish Daily Record": "www.dailyrecord.co.uk/",
                "Daily Record (Scotland)": "www.dailyrecord.co.uk/",
                "Israel Business Arena": "en.globes.co.il/en/",
                "The Times": "www.thetimes.co.uk/",
                "The Sunday Times": "www.thetimes.co.uk/?sunday",
                "Financial Times Deutschland": "www.ft.com",
                "Financial Times": "www.ft.com",
                "London Evening Standard Online": "www.standard.co.uk/",
                "Evening Standard": "www.standard.co.uk/",
                "Sunday People": "www.mirror.co.uk/",
                "The Sun": "www.thesun.co.uk/",
                "The Daily Express": "www.express.co.uk/",
                "The Daily Mirror": "www.mirror.co.uk/",
                "i": "inews.co.uk/",
                "Mail Online": "www.dailymail.co.uk",
                "Evening Standard Online": "www.standard.co.uk/",
                "The Mail on Sunday": "www.dailymail.co.uk/mailonsunday",
                "Financial Times (FT.Com)": "www.ft.com/",
                "The Guardian": "www.theguardian.com/international",
                "thetimes.co.uk": "www.thetimes.co.uk/",
                "Metro": "metro.co.uk/",
                "Irish Daily Mail": "www.dailymail.co.uk/news/republic-of-ireland",
                "sundaytimes.co.uk": "www.thetimes.co.uk/?sunday",
                "Daily Star": "www.dailystar.co.uk/",
                "El País": "elpais.com/",
                "London Evening Standard": "www.standard.co.uk/",
                "The Daily Telegraph" :"www.telegraph.co.uk/",
                "Mail on Sunday": "www.dailymail.co.uk/mailonsunday",
                "Daily Mail": "www.dailymail.co.uk",
                "Daily Record": "www.dailyrecord.co.uk/",
                "Irish Mail on Sunday": "www.irishmirror.ie/all-about/mail-on-sunday",
                "The Evening Standard": "www.standard.co.uk/",
                "The Express": "www.express.co.uk/",
                "Mirror": "www.mirror.co.uk/",
                "Scottish Daily Mail": "www.dailymail.co.uk/travel/destinationshub/scotland.html"
                }
# site:domain.com/path ("titre article 1" OR "titre article 2")
filepath = "factiva_EN_final.csv"
# filepath = "small_extract.csv"
media = set()
csv_HP = []

with open("article_with_AN_EN.csv", "w", newline="", encoding="utf-8") as new_csv:
    with open(filepath, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        csv_writer = csv.writer(new_csv, delimiter=",")

        first_row = ["title", "date", "media", "homepage", "AN"]
        csv_writer.writerow(first_row)

        next(csv_reader)  # let the first line
        for line in tqdm(csv_reader, total=770967):
            # media.add(line[22])
            try:
                newline = []
                AN = line[13].split(" ")[1]
                newline.extend([line[2], line[7], line[22], dic_homepage[line[22]], AN])
                csv_writer.writerow(newline)
            except:
                print("could not find",line[22],"in the dictionnary")

print(csv_writer)

print(media)
