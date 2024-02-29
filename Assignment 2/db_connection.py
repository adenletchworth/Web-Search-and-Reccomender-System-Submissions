#-------------------------------------------------------------------------
# AUTHOR: Aden Letchworth
# FILENAME: db_connection.py
# SPECIFICATION: Sample code for connecting to a database and performing operations
# FOR: CS 4250- Assignment #1
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
import psycopg2
import string # To make checking punctuation easier
from collections import defaultdict

def createTables(conn):
    try:
        cursor = conn.cursor()
        query =  """
        CREATE TABLE IF NOT EXISTS CATEGORIES(
            id_cat integer PRIMARY KEY, 
            name varchar
        );
        """
        
        cursor.execute(query)
        
        query = """
        CREATE TABLE IF NOT EXISTS DOCUMENTS (
            doc_number integer PRIMARY KEY, 
            num_chars integer, 
            date date, 
            id_cat integer REFERENCES CATEGORIES (id_cat), 
            doc_text varchar, 
            title varchar
        );
        """
        
        cursor.execute(query)
        
        query = """
        CREATE TABLE IF NOT EXISTS TERMS (
            term varchar PRIMARY KEY, 
            num_chars integer
        );
        """
        
        cursor.execute(query)
        
        query = """
        CREATE TABLE IF NOT EXISTS DOCUMENT_TERMS (
            doc_number integer REFERENCES DOCUMENTS (doc_number), 
            term varchar REFERENCES TERMS (term), 
            num_occurrences integer,
            PRIMARY KEY (doc_number, term)
        );
        """
        cursor.execute(query)
        conn.commit()
        cursor.close()
    except:
        print("Error: Unable to create tables")

def connectDataBase():
    try:
        conn = psycopg2.connect(
            dbname="test",
            user="postgres",
            password="tannaz",
            host="localhost",
            port="5432"
        )
        createTables(conn)
        return conn
    except:
        print("Error: Unable to connect to the database")

def createCategory(cur, catId, catName):
    try:
        query = "INSERT INTO CATEGORIES (id_cat, name) VALUES (%s, %s)"
        cur.execute(query, (catId, catName))
    except:
        print("Error: Unable to create category")


def createDocument(cur, docId, docText, docTitle, docDate, docCat):
    # 1 Get the category id based on the informed category name
    # --> add your Python code here
    
    try:
        query = "SELECT id_cat FROM CATEGORIES WHERE name = %s"
        cur.execute(query, (docCat, ))
        category = cur.fetchall()[0][0]
    except:
        print("Error: Unable to get category id")

    # 2 Insert the document in the database. For num_chars, discard the spaces and punctuation marks.
    # --> add your Python code here
    
    calculate_num_chars = lambda text: sum(1 for c in text if c not in string.punctuation and not c.isspace())
    try:
        query = "INSERT INTO DOCUMENTS (doc_number, doc_text, title, date, num_chars, id_cat) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(query, (docId, docText, docTitle, docDate, calculate_num_chars(docText), category))
    except:
        print("Error: Unable to insert Document")
        
    # 3 Update the potential new terms.
    # 3.1 Find all terms that belong to the document. Use space " " as the delimiter character for terms and Remember to lowercase terms and remove punctuation marks.
    # 3.2 For each term identified, check if the term already exists in the database
    # 3.3 In case the term does not exist, insert it into the database
    # --> add your Python code here
    try:
        trans_table = str.maketrans('', '', string.punctuation)
        terms = [term.translate(trans_table).lower() for term in docText.split()] 
        set_terms = set(terms)
        
        

        query = "SELECT term FROM TERMS WHERE term IN %s"
        cur.execute(query, (tuple(set_terms), ))

        existing_terms = [row[0] for row in cur.fetchall()]
        unique_terms = [term for term in set_terms if term not in existing_terms]
        
        for term in unique_terms:
            query = "INSERT INTO TERMS (term, num_chars) VALUES (%s, %s)"
            cur.execute(query, (term, len(term), ))
    except:
        print("Error: Unable to add terms")

    # 4 Update the index
    # 4.1 Find all terms that belong to the document
    # 4.2 Create a data structure the stores how many times (count) each term appears in the document
    # 4.3 Insert the term and its corresponding count into the database
    # --> add your Python code here
    try:
        term_frequency = {term:0 for term in terms}
        for term in terms:
            term_frequency[term] = term_frequency.get(term, 0) + 1
        for term, frequency in term_frequency.items():
            query = "INSERT INTO DOCUMENT_TERMS (doc_number, term, num_occurrences) VALUES (%s, %s, %s)"
            cur.execute(query, (docId, term, frequency, ))
    except:
        print("Error: Unable to insert term frequency")
        
def deleteDocument(cur, docId):
    
    # 1 Query the index based on the document to identify terms
    # 1.1 For each term identified, delete its occurrences in the index for that document
    # 1.2 Check if there are no more occurrences of the term in another document. If this happens, delete the term from the database.
    # --> add your Python code here
    
    try:
        cur.execute("SELECT term FROM DOCUMENT_TERMS WHERE doc_number = %s", (docId,))
        doc_terms = cur.fetchall()
        
        for term_tuple in doc_terms:
            term = term_tuple[0]  
            cur.execute("DELETE FROM DOCUMENT_TERMS WHERE doc_number = %s AND term = %s", (docId, term, ))
            cur.execute("SELECT COUNT(*) FROM DOCUMENT_TERMS WHERE term = %s", (term,))
            if cur.fetchone()[0] == 0:
                cur.execute("DELETE FROM TERMS WHERE term = %s", (term,))

        cur.execute("DELETE FROM DOCUMENTS WHERE doc_number = %s", (docId,))
    except:
        print("Error: Unable to delete document")   
    # 2 Delete the document from the database
    # --> add your Python code here

def updateDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Delete the document
    deleteDocument(cur, docId)

    # 2 Create the document with the same id
    # --> add your Python code here
    createDocument(cur=cur, docId=docId, docText=docText, docTitle=docTitle, docDate=docDate, docCat=docCat)

def getIndex(cur):
    index = defaultdict(list)
    query = "SELECT * FROM DOCUMENT_TERMS ORDER BY term"
    cur.execute(query)
    doc_terms = cur.fetchall()
    
    for docId, term, count in doc_terms:
        cur.execute('SELECT title FROM DOCUMENTS WHERE doc_number = %s', (docId,))
        title = cur.fetchone()[0]
        
        index[term].append(title + ":" + str(count))

    return dict(index)

    
    
    
    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here