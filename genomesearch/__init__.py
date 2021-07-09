

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv
import sys
import random
import flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ab4164a8b981dc470c608ddca8f1b767'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finalizedWheatData.db'
db = SQLAlchemy(app)

from genomesearch import routes
from genomesearch.models import Genome

def initDatabase():
    dataDictionary = dict()
    keysArray = []

    with open('alldata.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        lineCount = 0
        for row in csvreader:
            outputArray = []
            i = 1
            while i < len(row):

                if row[i] != '':
                    outputArray.append(row[i])
                i += 1

            outputArray.insert(0, row[0])
            if lineCount == 0:
                keysArray = outputArray
            else:
                if row[0] not in dataDictionary:
                    dataDictionary[row[0]] = outputArray

            lineCount += 1
    print("FIRST")
    counter = 0
    seen = {}
    print(len(dataDictionary))
    for key in dataDictionary:

        if counter != 0:
            tempSNPId = dataDictionary[key][0]
            tempName = dataDictionary[key][1]
            tempChrom = dataDictionary[key][2]
            tempcM = dataDictionary[key][3]
            tempAAFreq = dataDictionary[key][4]
            tempABFreq = dataDictionary[key][5]
            tempBBFreq = dataDictionary[key][6]
            tempSNP = dataDictionary[key][7]
            tempAlleleA = dataDictionary[key][8]
            tempAlleleB = dataDictionary[key][9]
            tempSourceSeq = dataDictionary[key][10]
            i = 11
            tempSamples = ""
            while i < len(dataDictionary[key]):
                keysArray[i]
                dataDictionary[key][i]
                tempSamples += keysArray[i] + dataDictionary[key][i] + ", "
                i += 1
            if len(tempSamples) != 0:
                tempSamples = tempSamples[:-2]
            if tempSNPId not in seen:
                currentGenome = Genome(
                    SNPId=tempSNPId, 
                    name=tempName, 
                    chrom = tempChrom,
                    cM=tempcM, 
                    AAFreq = tempAAFreq,
                    ABFreq = tempABFreq,
                    BBFreq = tempBBFreq,
                    SNP = tempSNP,
                    alleleA = tempAlleleA,
                    alleleB = tempAlleleB,
                    sourceSeq = tempSourceSeq,
                    samples=tempSamples
                    )
                seen[tempSNPId] = 0
            db.session.add(currentGenome)
            if counter % 1000 == 0:
                print(f"Processed {counter} rows from {csvfile} . . . ")
        counter += 1
    db.session.commit()


db.create_all()

if Genome.query.all() == []:
    initDatabase()
