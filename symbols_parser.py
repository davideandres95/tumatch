import csv
with open('nasdaq_symbols.csv', newline='') as csvfile:
    f = open("securities.sql", "w")
    f.write("BEGIN TRANSACTION;"
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for i, row in enumerate(spamreader):
        symbol = row[0].split(',')[0]
        f.write("INSERT INTO 'security' ('name') VALUES ('{}');\n".format(symbol))
    f.write("COMMIT;")
    f.close()
