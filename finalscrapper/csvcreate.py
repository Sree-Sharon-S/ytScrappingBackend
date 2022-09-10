from pathlib import Path
import csv

lis = [[4,5], ["True", "False"]]

def csvWriter(lis):
    Path("finalscrapper\\temp\\yt.csv").touch()
    file_to_write = open("finalscrapper\\temp\\yt.csv", 'w', encoding="utf-8")
    pen = csv.writer(file_to_write)
    pen.writerow(["No","Video Links","Thumbnails","Title","Likes","Comments","Views","Download"])
    for record in lis:
        pen.writerow(record)
    file_to_write.close()

