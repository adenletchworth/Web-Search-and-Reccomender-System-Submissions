#-------------------------------------------------------------------------
# AUTHOR: Aden Letchworth
# FILENAME: indexing.py
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #1
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#Importing some Python libraries
import csv

documents = []
labels = []

#Reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0].lower()) # Small modification made here to ensure all words are lowercase
            labels.append(row[1])
            
#Add simple tokenization for easy data manipulation
def tokenize(docs):
    tokenized_docs = []
    for doc in docs:
        tokens = doc.split()
        tokenized_docs.append(tokens)
    return tokenized_docs

documents = tokenize(documents)

#Conducting stopword removal. Hint: use a set to define your stopwords.
#--> add your Python code here
stopWords = {'i', 'and', 'she', 'her', 'their', 'they'}

def filter(docs):
  filtered_docs = []
  for doc in docs:
    filtered_doc = []
    for word in doc:
      if word not in stopWords:
        filtered_doc.append(word)
    filtered_docs.append(filtered_doc)
  return filtered_docs

      
documents = filter(documents)

#Conducting stemming. Hint: use a dictionary to map word variations to their stem.
#--> add your Python code here
stemming = {'cats':'cat', 'dogs':'dog', 'loves':'love'}

def is_stemmed(word):
  return True if word not in stemming else False

def stem(docs):
  stemmed_docs = []
  for doc in docs:
    stemmed_doc = []
    for word in doc:
      if is_stemmed(word):
        stemmed_doc.append(word)
      else:
        stemmed_doc.append(stemming[word])
    stemmed_docs.append(stemmed_doc)
  return stemmed_docs

documents = stem(documents)

#Identifying the index terms.
#--> add your Python code here
def get_terms(docs):
  terms = set()
  for doc in docs:
    for word in doc:
      if word not in terms:
        terms.add(word)
  return terms

terms = get_terms(documents)

#Building the document-term matrix by using the tf-idf weights.
#--> add your Python code here
def get_tf(terms, docs):
  tf = []
  for doc in docs:
      num_words = len(doc)
      tf_dict = {}
      for term in terms:
          tf_dict[term] = doc.count(term) / num_words if term in doc else 0
      tf.append(tf_dict)
  return tf
      

def get_idf(terms, docs):
  return

def matmul(tf, idf):
  return 

tf = get_tf(terms, documents)
print(tf)
idf = get_idf(terms, documents)

doc_term_matrix = matmul(tf, idf)

#Printing the document-term matrix.
#--> add your Python code here