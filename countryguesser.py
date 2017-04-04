# La idea es coger una IP sacada de alguna parte, pasarla a decimal (de base 256)
# y consultar en la base de datos el rango en el que está y así devolver el país para poder
# hacer un block por country

import csv
import sys

ipFile = sys.argv[1]
ipDict = []


def fileParser():
    with open(ipFile) as ipF:
        r = ipF.read()
        return r.splitlines()


# OUT: Lista de diccionarios de entries ['ipStart', 'ipEnd', 'countryAcronym', 'countryName']
def csvToDict():
    with open('IP2LOCATION-LITE-DB1.CSV', 'r') as f:
        dReader = csv.DictReader(f)
        headers = dReader.fieldnames
        for line in dReader:
            entry = {headers[0]: int(line[headers[0]]),  # ipStart
                     headers[1]: int(line[headers[1]]),   # ipEnd
                     headers[2]: line[headers[2]],        # countryAcronym
                     headers[3]: line[headers[3]]}        # countryName

            ipDict.append(entry)


def ipToDecimal(base256IP):
    splitIP = [int(x) for x in base256IP.split('.')]
    decimalIP = (splitIP[0] * (256**3) +
                 (splitIP[1] * (256 ** 2)) +
                 (splitIP[2] * (256 ** 1)) +
                 (splitIP[3] * (256 ** 0)))
    return decimalIP


def isIPinRange(decimalIP, dictEntry):
    return (decimalIP >= dictEntry['ipStart']) and (decimalIP <= dictEntry['ipEnd'])


csvToDict()

for i in fileParser():
    for d in ipDict:
        if isIPinRange(ipToDecimal(i), d):
            print("The IP {} corresponds to {} ({})".format(i, d['countryName'], d['countryAcronym']))
