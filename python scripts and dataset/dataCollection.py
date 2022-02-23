import requests   #for web scraping
import time       #for loading speed and waiting to get URLs
import re         #for regex
import math       #for square roots (pre processing)
import csv        #to write to csv
import datetime   #for the file name

import machineLearning    #this is my other python file

#requests for apify to get the urls and parses XML data for the search terms
def getURLs():
    #requests for apify get the urls
    urlToRun = 'https://api.apify.com/v2/actor-tasks/8XV69VRuwOTKN5I6g/runs?token=JL8aicxsRfkBtp2apSr79t2y9'
    response = requests.post(urlToRun)
    print('response to running actor: '+response.text)

    #waits 10 minutes (long enough for data to be collected)
    time.sleep(600)

    #gets the XML results from most recent web scrape
    urlForXML = 'https://api.apify.com/v2/actor-tasks/8XV69VRuwOTKN5I6g/runs/last/dataset/items?token=JL8aicxsRfkBtp2apSr79t2y9&format=xml'
    response = requests.get(urlForXML)
    resText = response.text

    #removes unnecessary data that wont be used
    resText = resText.replace('\n', '')
    resText = re.sub('<paidResults>.*?</paidResults>', '', resText)
    resText = re.sub('<relatedQueries>.*?</relatedQueries>', '', resText)

    #divides XML into an array of each page of results
    items = re.findall('<item>(.*?)</item>', resText)

    #appends the position (calculated from page number and url number) and url
    preparedData = []
    for i in range (len(items)):
        pageNum = int(re.findall('<page>(.*?)</page>', items[i])[0]) - 1

        #takes out the url searchQuery tag with the google search URL 
        currentPage = re.sub('<searchQuery>.*?</searchQuery>', '', items[i])
        urlsOnPage = re.findall('<organicResults>.*?<url>(.*?)</url>.*?</organicResults>', currentPage)

        for j in range (len(urlsOnPage)):
            preparedData.append([(pageNum * 100) + (j+1), urlsOnPage[j]])
    
    print('urls returned')
    return preparedData

#funtion to check security
def isSecure (url):
    urlParts = url.split(':')
    urlProtocol = urlParts[0]
    if(urlProtocol == 'https'):
        return True
    elif(urlProtocol == 'http'):
        return False
    else:
        return None

#function to check the robots.txt file
def isRobotsCorrect (url):
    #constructs the url where the robots file is usually located
    urlParts = url.split('/')
    robotsUrl = urlParts[0]+'//'+urlParts[2]+'/robots.txt'

    #requests the robots file
    try:
        response = requests.get(robotsUrl, verify = False, timeout=25)
    except:
        return None
    else:
        if(response.status_code == 200):
            lines = response.text.lower().split('\n')
            if(lines[0] == 'user-agent: *' and lines[1] == 'disallow: /'):
                return False
            else:
                return True
        else:
            return None

#function that checks the page loading speed
def loadingSpeed(url): 
    totalTime = 0
    for i in range (0, 3):
        #makes the request
        try:
            start = time.time()
            response = requests.get(url, verify = False, timeout=25)
            stop = time.time()
            totalTime += (stop-start)
        except:
            return None

    return round(totalTime/3, 3)

#function that finds the number of key words in the header/title/webpage
def numkeyWords(url):
    try:
        response = requests.get(url, verify = False, timeout=25)
    except:
        return None
    else:
        #gets the html and makes it lowercase
        html = response.text.lower()

        #removes all new lines
        html = html.replace('\n', '')

        #removes script and style tags (and everything between them)
        html = re.sub('<script.*?>.*?</script.*?>', '', html)
        html = re.sub('<style.*?>.*?</style.*?>', '', html)

        #finds all title/h1 tags of the form <title [any no. of chars]> [any no. of chars] </title [any no. of chars]>
        #and returns the inner part
        titles = re.findall('<title.*?>(.*?)</title.*?>', html)
        headers = re.findall('<h1.*?>(.*?)</h1.*?>', html)

        #gets number of spesific tags before they are removed
        noTags = findTags(html)

        #removes all tags
        html = re.sub('<.*?>', '', html)

        #seperates all titles/headers into lists of individual words
        titleWords = []
        for i in range (len(titles)):
            titleWords += titles[i].split(' ')
        
        headerWords = []
        for i in range (len(headers)):
            headerWords += headers[i].split(' ')
        
        #splits into an array of words
        htmlWords = html.split(' ')
        
        #creates and return the output array including number of keywords, lengths of texts and number of spesific tags
        output = [checkAgainstKeyWords(titleWords), checkAgainstKeyWords(headerWords), checkAgainstKeyWords(htmlWords), len(htmlWords), len(headerWords)]
        output += noTags
        return output

def checkAgainstKeyWords(arrToCheck):
    keyWords = ['short', 'term', 'short-term', 'lets', 'let', 'lettings', 'holiday', 'corporate', 'rentals', 'rental', 
                'bnb', 'bnbs', 'accommodation', 'medium-term', 'medium', 'serviced', 'property', 'properties']
    noMatches = 0
    for i in range(len(arrToCheck)):
        for j in range(len(keyWords)):
            if(arrToCheck[i] == keyWords[j]):
                noMatches += 1
    return noMatches

#function to find spesific tags
def findTags(html):
    noATags = len(re.findall('<a', html))
    noVideoTags = len(re.findall('<video', html))
    noImgTags = len(re.findall('<img', html))

    return [noATags, noVideoTags, noImgTags]

#main web scraping function
def webScrape (urlData):
    for i in range (len(urlData)):
        if(i%5 == 0):
            print('web scraped: '+str(i))


        #defines a temporary variable for the current url
        currentUrl = urlData[i][1]

        #checks and appends security
        currentUrlSecurity = isSecure(currentUrl)
        urlData[i].append(currentUrlSecurity)

        #checks and appends whether the robots.txt file is not on disallow all
        currentRobotsInitiated = isRobotsCorrect(currentUrl)
        urlData[i].append(currentRobotsInitiated)

        #finds and appends the loading speed
        speed = loadingSpeed(currentUrl)
        urlData[i].append(speed)

        #finds and appends number of keywords in title and h1 tags as well as in the whole webpage
        currentKeywordsData = numkeyWords(currentUrl)
        if(not(currentKeywordsData == None)):
            urlData[i] += currentKeywordsData
        else:
            urlData[i] += [None, None, None, None, None, None, None, None]

    #for testing
    print('urls webscraped')
    return urlData

def preProcess(dataset):
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
                    dataset[rowCount][colCount] = 1.00
                elif(currentVal == False):
                    dataset[rowCount][colCount] = 0.00
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

#starts the data collection and writes the results to csv
def writeToCSV():
    #gets data
    data = preProcess(webScrape(getURLs()))

    #concatinates the file name
    theTime = datetime.datetime.now()
    theDate = theTime.strftime("%x")
    theDate = theDate.replace('/', '-')
    fileName = 'Dataset-'+theDate+'.csv'

    #creates the file
    with open(fileName, 'w', newline='') as theFile:
        csvWriter = csv.writer(theFile)

        #first row is metadata [no. of rows, no. of columns]
        csvWriter.writerow([len(data), len(data[0])])

        #writes the rest of the data
        csvWriter.writerows(data)
        print('csv written')

#calls the first function that starts the process
writeToCSV()

#Runs my machine learning algorithm
machineLearning.run()





















    #test data
    #data = [[1, 1, 0, 0.321, 2, 1, 3, 2, 1, 0, 0, 0], [3, 1, 1, 0.123, 1, 1, 1, 1, 1, 1, 1, 2], [4, 0, 0, 0.432, 4, 3, 2, 1, 3, 2, 1, 2]]



#output key:
#[pos, url, secure, robots, speed, keywords in title, ...h1, ...webpage, length of h1, ...webpage, num a tags, ...video tags, ...image tags]


#creating a test dataset
urlTestData = [[1, 'https://google.com', True, False, 0.321, 2, 1, 3, 2, 1, 0, 0, 0],
               [2, 'http://example.com/', False, None, 0.898, 8, 1, 2, 8, 4, 5, 3, 4],
               [3, 'https://bbc.co.uk/', True, True, 0.123, 1, 1, 1, 1, 1, 1, 1, 2], 
               [4, 'https://www.rightmove.co.uk/property-to-rent/Bristol/short-term-lets.html', False, False, 0.432, 4, 3, 2, 1, 3, 2, 1, 2],
               [5, 'https://www.gumtree.com/property-to-rent/bristol/short+let', False, True, 0.456, 7, 8, 7, None, 5, 4, 3, 2]]
