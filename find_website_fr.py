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


dic_homepage = {"La Voix du Nord": "www.lavoixdunord.fr",
                "Le Figaro": "www.lefigaro.fr",
                "La Montagne": "www.lamontagne.fr",
                "Les Echos": "www.lesechos.fr",
                "Le Courrier de l'Ouest": "www.ouest-france.fr",
                "La Dépêche du Midi": "www.ladepeche.fr",
                "Le Télégramme": "www.letelegramme.fr",
                "Le Figaro Magazine": "https:/www.lefigaro.fr/lefigaromagazine",
                "La Nouvelle République du Centre Ouest": "www.lanouvellerepublique.fr",
                "Les Echos Business": "business.lesechos.fr",
                "Sud Ouest": "www.sudouest.fr",
                "Le Républicain Lorrain": "www.republicain-lorrain.fr",
                "Les Echos Executives": "business.lesechos.fr",
                "M, le magazine du Monde": "www.lemonde.fr/m-le-mag",
                "La Croix": "www.la-croix.com",
                "Les Echos Business.fr": "business.lesechos.fr",
                "Capitalfinance.fr": "capitalfinance.lesechos.fr",
                "Le Cercle Les Echos": "inurl:lesechos.fr/idees-debats/cercle",
                "Capital Finance": "capitalfinance.lesechos.fr",
                "Les Echos Week-End": "weekend.lesechos.fr",
                "Le Progrès": "www.leprogres.fr",
                "Midi Libre": "www.midilibre.fr/actu",
                "Les Echos.fr": "www.lesechos.fr/",
                "La Provence": "www.laprovence.com",
                "La Nouvelle République Dimanche": "www.lanouvellerepublique.fr",
                "Ouest France": "www.ouest-france.fr",
                "L'Est Républicain": "www.estrepublicain.fr",
                "Le Figaro Premium": "plus.lefigaro.fr/tag/figaro-premium",
                "Enjeux Les Echos": "www.lesechos.fr"
                }
# site:domain.com/path ("titre article 1" OR "titre article 2")
filepath = "factiva_fr_final.csv"
# filepath = "small_extract.csv"
media = set()
csv_HP = []

with open('article_with_AN_FR.csv', 'w', newline='', encoding="utf-8") as new_csv:
    with open(filepath, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        csv_writer = csv.writer(new_csv, delimiter=",")

        first_row = ["title", "date", "media", "homepage", "AN"]
        csv_writer.writerow(first_row)

        next(csv_reader) #let the first line
        for line in tqdm(csv_reader, total=770967):
            try:
                newline = []
                AN = line[15].split(" ")[1]
                newline.extend([line[3], line[8], line[25], dic_homepage[line[25]],  AN])
                csv_writer.writerow(newline)
            except:
                print("could not find",line[25],"in the dictionnary")

print(csv_writer)
