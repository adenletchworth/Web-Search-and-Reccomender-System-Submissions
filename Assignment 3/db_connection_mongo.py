#-------------------------------------------------------------------------
# AUTHOR: your name
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #3
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
import pymongo
import string # for string.punctuation
from collections import defaultdict # for defaultdict to cleanup the code during index portion

def connectDataBase():

    # Create a database connection object using pymongo
    # --> add your Python code here
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['Index']
    return db
    

def createDocument(col, docId, docText, docTitle, docDate, docCat):
    remove_punct_trans = str.maketrans('', '', string.punctuation)

    # Remove punctuation from the document text
    cleaned_docText = docText.translate(remove_punct_trans)

    # Create a dictionary indexed by term to count how many times each term appears in the document.
    term_freq = {}
    for term in cleaned_docText.split(' '):
        cleaned_term = term.lower()
        if cleaned_term:  
            term_freq[cleaned_term] = term_freq.get(cleaned_term, 0) + 1
    
    # Create a list of objects to include full term objects. [{"term", "count", "num_char"}]
    full_term_objects = [{"term": term, "count": term_freq[term], "num_char": len(term)} for term in term_freq]
    docNumChars = len(cleaned_docText.replace(' ', ''))

    # Produce a final document as a dictionary including all the required document fields
    document = {
        'docId': docId,
        'docText': docText,
        'docTitle': docTitle,
        'docDate': docDate,
        'docCat': docCat,
        'docNumChars': docNumChars,
        'terms': full_term_objects
    }

    # Insert the document into the collection
    col.insert_one(document)

def deleteDocument(col, docId):
    col.delete_one({'docId':docId})


def updateDocument(col, docId, docText, docTitle, docDate, docCat):
    col.update_one({'docId':docId}, {'$set': {'docText':docText, 'docTitle':docTitle, 'docDate':docDate, 'docCat':docCat}})

def getIndex(col):
    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
    index = defaultdict(list)
    documents = col.find({'terms': {'$exists': True}})
    for doc in documents:
        for term_data in doc['terms']:
            index[term_data['term']].append(f"{doc['docTitle']}:{term_data['count']}")
    return dict(index)