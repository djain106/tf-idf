#Coded by Daksh Jain
"""
This code uses the term frequency vector of a document and compares it with a query's term frequency vector and returns the closest document vectors in a query search
"""

import math
#Constants
TERM_VECTOR = 0
FILENAME = 1
URL = 2
AUTHOR = 3
TITLE = 4

def makeDocument(tfVector,filename='',url='',author='',title=''):
    """
    makeDocument takes up to five parameters and returns an ordered list of Term Frequency Vector, the file name, the url, the name of the author, and the title.
    If no parameters are given, an empty string is returned.
    Input: Up to five parameters, tfVector, filename, url, author, title
    Output: Input returned as a list
    """
    return [tfVector,filename,url,author,title]

def makeDocsFromFileList(listOfFileNames):
    """
    makeDocsFromFileList takes a list of file names as its parameter and returns a list of multiple document objects for each file
    Input: One parameter, A list of file names
    Output: A list of the file's document objects
    """
    documentList = []
    for fileName in listOfFileNames:
        documentList.append(makeDocFromFile(fileName))
    return documentList

def makeDocFromFile1(fileName):
    """
    makeDocFromFile takes a file name, opens it, reads the preamble containing the url, author, and title for that file. Then it gets the word list from the file, creates a Term Frequency Vector for the file, and creates a document object representation of the file.
    Input: One parameter, a file name
    Output: Document Object for a file
    """
    file = openFile(fileName)
    url = file.readline().replace('\n','')
    author = file.readline().replace('\n','')
    title = file.readline().replace('\n','')
    words = getWordListFromFile(file)
    tfv = makeTermFrequencyVector(words)
    return makeDocument(tfv, fileName, url, author, title)

def getWordListFromFile1(file):
     """
     getWordListFromFile reads a file into a string, removing dashes and punctuation, splitting the string into words based on white space, puts all letters in lowercase, and returns the resulting word list.
     Input: One parameter, an open file object
     Output: A word list
     """
     words = file.read()
     words = removeDashes(words)
     words = removePunctuation(words)
     return words.lower().split()

def openFile(fileName):
    """
    openFile takes a local file name as a parameter and returns the file object for that file
    Input: a file name
    Output: a file object
    """
    file = open(fileName, "r")
    return file #No Test Required

def removePunctuation(inputstring):
    """
    removePunctuation removes all punctuation and special characters from a string, except sashes.
    Input: One parameter, a string
    Output: A string without punctuation
    """
    for elt in "!'#$%&()*+,./:;<=>?@[\]^_`{|}~":
        inputstring = inputstring.replace(elt,'')
    return inputstring

def removeDashes(inputstring):
    """
    removeDashes removes all dashes except for hyphens(dashes not surrounded by alphanumeric characters)
    Input: One parameter, a string
    Output: a string not containing dashes
    """
    for elt in ['-\n ',' -\n','-\n','\n-','--', '- ', ' -']:
        inputstring = inputstring.replace(elt, '')
    return inputstring

def makeTermFrequencyVector(listOfWords):
    """
    makeTermFrequencyVector takes a list of words and returns a dictionary that represents the term frequency vector of that word list. The words represent the keys and values represent how frequently the words occur in the document.
    Input: One parameter, a list of words
    Output:  A dictionary (Term Frequency Vector)
    """
    if not listOfWords:
        return {}
    frequencyDictionary = {}
    for word in listOfWords:
        if word in frequencyDictionary:
            frequencyDictionary[word] += 1
        else:
            frequencyDictionary[word] = 1
    return frequencyDictionary

def extendVectors(tfv1,tfv2):
    """
    extendVectors takes two dictionary and modifies them to be the same length by adding values of zero to words that occur in one dictionary but not the other.
    Input: Two parameters, two dictionaries with varied lengths
    Output: Two dictionaries with the same lengths
    """
    for word in tfv1:
        if not(word in tfv2):
            tfv2[word] = 0
    for word in tfv2:
        if not(word in tfv1):
            tfv1[word] = 0

def extendAllVectors(listOfDocuments):
    """
    extendAllVectors takes a list of documents and extends each term frequency vector to the same length by giving zero values to words that occur in the overall vocabulary of the all the documents but not the specific document that is given.
    Input: One parameter, a list of documents
    Output: List of documents with extended term frequency vectors
    """
    for elt in listOfDocuments:
        extendVectors(listOfDocuments[0][TERM_VECTOR],elt[TERM_VECTOR])
    for index in range(len(listOfDocuments)):
        extendVectors(listOfDocuments[0][TERM_VECTOR],listOfDocuments[index][TERM_VECTOR])
    return listOfDocuments

def computeSimilarity(weight1,weight2):
    """
    computeSumularity takes two weight vectors, which are represented by dictionaries, and returns a float computed as the cosine distance between the two tf-idf vectors represented by the dictionaries.
    Input: Two parameters, two weight vectors
    Output: A float (the cosine distance)
    """
    normSum1, normSum2, totalVal = 0, 0, 0
    for word in weight1:
        normSum1 += (weight1[word])**2
        normSum2 += (weight2[word])**2
        totalVal += weight1[word]*weight2[word]
    norm1 = normSum1**(1/2)
    norm2 = normSum2**(1/2)
    if norm1 == 0 or norm2 == 0: #Need this case because you cannot divide by 0
        return 0
    return float((totalVal)/(norm1*norm2))

def computeIDFforEachTerm(documentList):
    """
    computeIDFforEachTerm takes a document list and computes the IDF for each term.
    Input: One parameter, a document list
    Output: A dictionary containing the IDF for each term
    """
    IDFVector = {}
    NumOfDocs = len(documentList)
    for term in documentList[0][TERM_VECTOR]:
        idfFactor = 0
        for document in documentList:
            if document[TERM_VECTOR][term] != 0:
                idfFactor+=1
        IDFVector[term] = math.log(NumOfDocs/idfFactor,10)
    return IDFVector

def applyIDFtoVector(docTFV,idfVector):
    """
    applyIDFtoVector takes a document’s term frequency vector and the idf factor vector for all documents, and then converts the term frequency vector to an tf-idf vector.
    Input: One parameter, a document’s term frequency vector
    Output: tf-idf vector or weight vector
    """
    for term in idfVector:
        docTFV[term] = docTFV[term]*idfVector[term]

def getQueryWordListFromUser():
    """
    getQueryWordListFromUser prompts the user for a query and returns a list of all the words in the query.
    Input: None given to the function (from the user, either a set of words or a single line)
    Output: A list of the words
    """
    query = input('What would you like to search for?\n')
    return query.lower().split()

def makeQueryTFVector(listOfQuery):
    """
    makeQueryTFVector takes a list of words and returns a dictionary representing its term frequency vector.
    Input: One parameter, a list of words
    Output: A dictionary representation of its term frequency vector
    """
    return makeTermFrequencyVector(listOfQuery)

def makeDocDistanceTuples(documentList, tfvQuery): #Find out what the 2nd and 3rd parameter should be set to and how?
    """
    makeDocDistanceTuples takes the dictionary storing the weight frequency vector for a user query and also a document list and returns a list of tuples of the form (document,distance) where distance is a computed distance between the document and the user query based on their weight frequency vectors.
    Input: Two parameters, dictionary of a weight frequency vector for a user query and a document list storing the weight vectors of each document
    Output: list of tuples that includes the document and its computed distance
    """
    docTupleList = []
    for document in documentList:
        docTupleList.append((document,computeSimilarity(document[0],tfvQuery)))
    return docTupleList

def getNclosestDocs(numOfDocs,listOfDocumentTuples):
    """
    getNclosestDocs takes a number that indicates the desired number of reported closely related documents to the query and a list of tuples, and returns the indicated number of top closest related documents.
    Input: Two parameters, An integer of desired number of closest documents and a list of tuples in the format (document, distance)
    Output: a list containing the desired number of closest documents
    """
    sortedDocumentTuples = mergeSortTuples(listOfDocumentTuples)
    returnList = []
    for tuple in sortedDocumentTuples:
        returnList.append(tuple[0])
    return returnList[:numOfDocs]

def displayResults(queryList,documentList,numOfDocs):
    """
    displayResults takes a list of query words, a document list, and number of results and prints the query
I   Input:a list of query words, a document list, and number of results
    Output: the desired number of documents in a list going from most relevance to least relevance down the list
    """
    tfvQuery = makeQueryTFVector(queryList)
    docListWeights, queryWeight = weightVectors(documentList, tfvQuery)
    tupleList = makeDocDistanceTuples(docListWeights, queryWeight)
    print(tupleList)
    documentList = getNclosestDocs(numOfDocs, tupleList)
    querySearch = ' '.join(queryList)
    print('User query:', querySearch)
    count = 1
    print('Closest Documents:','\n')
    for doc in documentList:
        print('Result',count,end=' ')
        print('Cosine Similarity:',float(tupleList[count-1][1]))
        print('File Name:',doc[FILENAME])
        print('url:',doc[URL])
        print('Author:', doc[AUTHOR])
        print('Title:', doc[TITLE],'\n')
        count+=1


def processUserRequest(documentList):
    """
    processUserRequest takes a list of documents, a query word list from the user, and a number of closest related documents to return. It retrieves from the user and processes the query, returning the correct number of closest related documents. It also prints the results from the search for the user to see.
    Input: a list of documents, a query word list from the user, and a number of desired results
    Output: returns the correct number of closest related documents

    """
    queryWordList = getQueryWordListFromUser()
    numOfDocs = int(input('How many documents to retrieve?\n'))
    return displayResults(queryWordList,documentList,numOfDocs)

##################
#HELPER FUNCTIONS#
##################
def weightVectors(documentList,tfvQuery):
    """
    weightVectors takes a list of documents and the term frequency vector for the query and returns the weight vectors of all the vectors of the documents and the query by computing idf of each term and then carrying out the tf-idf calculations
    Input: a document list storing all the term frequency vectors of each document and the query's term frequency vector
    Output: the document list containing all the weight vectors of the documents and the weight vector of the query
    """
    documentList = extendAllVectors(documentList)
    idfVector = computeIDFforEachTerm(documentList)
    documentList.append([tfvQuery])
    documentList = extendAllVectors(documentList)
    documentList[-1:] = []
    for document in documentList:
        applyIDFtoVector(document[TERM_VECTOR],idfVector)
    applyIDFtoVector(tfvQuery,idfVector)
    return documentList, tfvQuery

def merge(alist,blist):
    """
    merge returns the sorted list of distance values for the tuples, but in decreasing magnitude instead of increasing
    Input: two lists of tuples
    Output: a combined list of tuples with decreasing magnitude in the distance
    """
    finalList = []
    indexA, indexB = 0,0
    while indexA < len(alist) and indexB < len(blist):
        if alist[indexA][1] > blist[indexB][1]:
            finalList.append(alist[indexA])
            indexA+=1
        else:
            finalList.append(blist[indexB])
            indexB+=1
    finalList += alist[indexA:] + blist[indexB:]
    return finalList

def mergeSortTuples(alist):
    """
    mergeSortTuples takes a list of tuples storing the (document, distance) and returns the ordered list of all the tuples
    Input: list of document tuples with (document, distance)
    Output: the sorted list of tuples in decreasing order
    """
    if len(alist) < 2:
        return alist
    else:
        mid = len(alist)//2
        return merge(mergeSortTuples(alist[:mid]),mergeSortTuples(alist[mid:]))

import os
def getAllTextFiles():
    """Returns a list of text files from the current directory"""
    return list(filter(lambda f:f[-4:] == '.txt',os.listdir(os.getcwd())))


def getWordListFromFile(fileObject):
    """Read all words in a file, remove punctuation, fix dashes etc.return -- list of strings"""
    strlist = []
    line = myReadLine(fileObject)
    while(line):
        line = removeDashes(line)
        line = removePunctuation(line)
        strlist.extend(line.lower().split())
        line = myReadLine(fileObject)
    return strlist

def myReadLine(file):
    try:
        s = file.readline()
        return s
    except UnicodeDecodeError:
        print('skipped unicode error')
        return ' '

def makeDocFromFile(fileName):
    dfile = openFile(fileName)
    url = myReadLine(dfile) #dfile.readline()
    author =  myReadLine(dfile) #dfile.readline()
    title =  myReadLine(dfile) #dfile.readline()
    wordList = getWordListFromFile(dfile)
    dfile.close()

    termVector = makeTermFrequencyVector(wordList)
    doc = makeDocument(termVector,fileName,url,author,title)
    return doc




files = getAllTextFiles()
documents = makeDocsFromFileList(files)
for num in range(1,8):
    print('-'*8+' SEARCH# '+str(num)+' ' +'-'*8)
    processUserRequest(documents)
    print()
    print()
