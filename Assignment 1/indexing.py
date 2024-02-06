#-------------------------------------------------------------------------
# AUTHOR: Aden Letchworth
# FILENAME: indexing.py
# SPECIFICATION: Simple Data Processing for Document into TF-IDF Matrix
# FOR: CS 4250- Assignment #1
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#Importing some Python libraries
import csv
import math # for log function

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
  terms = []
  for doc in docs:
    for word in doc:
      if word not in terms:
        terms.append(word)
  return terms

terms = get_terms(documents)

#Building the document-term matrix by using the tf-idf weights.
#--> add your Python code here
def get_tf(terms, docs):
  tf = []
  for doc in docs:
      num_words = len(doc)
      tf_doc = [0] * len(terms)
      for i, term in enumerate(terms):
          tf_doc[i] = doc.count(term) / num_words if term in doc else 0
      tf.append(tf_doc)
  return tf

      

def get_idf(terms, docs):
  idf = []
  n = len(docs)
  for term in terms:
    count = 0
    for doc in docs:
      if term in doc:
        count += 1
    idf.append(math.log(n/count, 10) if count != 0 else 0) 
  return idf
      

def matmul(tf, idf):
  doc_term_matrix = []
  
  # Ensure the number of terms in TF matches the number of terms in IDF
  if len(tf[0]) != len(idf):
      return

  # Iterate over each document
  for doc in tf:
      doc_terms = []
      # Multiply each term's TF with its corresponding IDF
      for term_idx, tf_value in enumerate(doc):
          tfidf_value = tf_value * idf[term_idx]
          doc_terms.append(tfidf_value)
      doc_term_matrix.append(doc_terms)
  
  return doc_term_matrix

tf = get_tf(terms, documents)
idf = get_idf(terms, documents)

doc_term_matrix = matmul(tf, idf)

#Printing the document-term matrix.
#--> add your Python code here

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(f"{elem:.2f}" for elem in row))

print_matrix(doc_term_matrix)
