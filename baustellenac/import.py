

import csv

fn = "/Users/cs/Dropbox/@PROJECTS/Offenes Aachen/BaustellenAC/liste.csv"
with open(fn, 'rb') as f:
    reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        if row[0]=="": 
            continue
        traeger, traeger2, titel, von_str, von_hnr, bis_str, bis_hnr, beschreibung, start_genau, ende_genau, start_text, ende_text, foo, bar = row
        print ende_text


