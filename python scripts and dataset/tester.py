import csv
import datetime
import requests
import time
import math

def preProcess(dataset):
    #key: [loading speed, keywords in title, ...h1, ...webpage, length of h1, ...webpage, num a tags, ...video tags, ...image tags]
    means = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    deviationSums = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    sdeviations = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    rowCount = 0
    colCount = 0
    endOfRow = False
    endOfData = False

    del dataset[0][1]
    while(not(endOfData)):
        currentVal = dataset[rowCount][colCount]

        if(currentVal == None):
            del dataset[rowCount]
            if(rowCount == len(dataset)):
                endOfData = True
                break
            else:
                colCount = 0
                del dataset[rowCount][1]
        else:
            if(colCount == 1 or colCount == 2):
                if(currentVal == True):
                    dataset[rowCount][colCount] = 1
                elif(currentVal == False):
                    dataset[rowCount][colCount] = 0
                else:
                    dataset[rowCount][colCount] = 0
            if(colCount > 2):
                means[colCount-3] += dataset[rowCount][colCount]
        colCount += 1
        if(colCount == len(dataset[rowCount])):
            rowCount += 1
            if(rowCount == len(dataset)):
                endOfData = True
            else:
                colCount = 0
                del dataset[rowCount][1]
                
    #divides by number of rows to get means
    numRows = len(dataset)
    numCols = len(dataset[0])
    for i in range (len(means)):
        means[i] = means[i]/numRows
        
    #since I need to use the mean values, I need to for loop through the numerical data again
    for i in range (numRows):
        for j in range (numCols - 3):
            deviationSums[j] += ((means[j] - dataset[i][j+3]) ** 2)

    #calculating S.Ds 
    for i in range (len(deviationSums)):
        sdeviations[i] = math.sqrt(deviationSums[i]/numRows)
            
    #standardization
    for i in range(numRows):
        for j in range (numCols - 3):
            if(not(sdeviations[j] == 0)):
                dataset[i][j+3] = (dataset[i][j+3] - means[j])/sdeviations[j]
            else:
                dataset[i][j+3] = 0

            dataset[i][j+3] = round(dataset[i][j+3], 5)
    
    print('preproccessed')
    return dataset


def preProc(dataset):
    means = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0]

    rowCount = 0
    colCount = 0
    endOfRow = False
    endOfData = False

    while(not(endOfData)):
        print('rc: '+str(rowCount))
        colCount = 0
        endOfRow = False
        del dataset[rowCount][1]

        while(not(endOfRow)):
            print('cc: '+str(colCount))
            currentVal = dataset[rowCount][colCount]

            if(currentVal == None):
                del dataset[rowCount]
                colCount = 0
                del dataset[rowCount][1]
            else:
                if(colCount == 1 or colCount == 2):
                    if(currentVal == True):
                        dataset[rowCount][colCount] = 1
                    elif(currentVal == False):
                        dataset[rowCount][colCount] = 0
                    else:
                        print('error with a boolean, set to 0: '+currentVal)
                        dataset[rowCount][colCount] = 0
                if(colCount > 2):
                    means[colCount-3] += dataset[rowCount][colCount]
                if(colCount == len(dataset[rowCount])-1):
                    endOfRow = True
                colCount += 1
        rowCount += 1

        if(rowCount == len(dataset)-2):
            endOfData = True
        
    print(dataset)

def workingPreProc(dataset):
    means = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0]

    rowCount = 0
    colCount = 0
    endOfRow = False
    endOfData = False

    del dataset[0][1]
    while(not(endOfData)):
        print('rc: '+str(rowCount)+', cc: '+str(colCount))
        currentVal = dataset[rowCount][colCount]

        if(currentVal == None):
            del dataset[rowCount]
            if(rowCount == len(dataset)):
                endOfData = True
                break
            else:
                colCount = 0
                del dataset[rowCount][1]
        else:
            if(colCount == 1 or colCount == 2):
                if(currentVal == True):
                    dataset[rowCount][colCount] = 1
                elif(currentVal == False):
                    dataset[rowCount][colCount] = 0
                else:
                    print('error with a boolean, set to 0: '+currentVal)
                    dataset[rowCount][colCount] = 0
            if(colCount > 2):
                means[colCount-3] += dataset[rowCount][colCount]
        colCount += 1
        #print('if this: '+str(colCount)+', and this: '+str(len(dataset[rowCount]))+', are equal so help me god')
        if(colCount == len(dataset[rowCount])):
            rowCount += 1
            if(rowCount == len(dataset)):
                endOfData = True
            else:
                colCount = 0
                del dataset[rowCount][1]
                #print('if this: '+str(rowCount)+', and this: '+str(len(dataset))+', are equal so help me god')
            
        
    print(dataset)



dataset = [[1, 'https://google.com', True, False, 0, 2, 1, 4, 5, 6, 6, 8, 9], 
           [2, 'https://example.com', False, False, 0, 1, 3, 0, 5, 8, None, 8, 9], 
           [3, 'http://test.com', True, False, 0, 2, 1, 1, 1, 6, 7, 10, 7]]

#print(preProcess(dataset))
print(preProcess(dataset))