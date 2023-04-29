from pprint import pprint
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import classification_report, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.neighbors import KNeighborsClassifier

x = '' # reading command line argument: the argv array looks like this: ['testpy.py', 'abcd1234'] if cmd-line argument is abcd1234

for i in range(1,len(sys.argv)):
    x += sys.argv[i]
    x += ' '

# print(x)

df = pd.read_csv('./Design_Lab_class_train_data.tsv',sep = '\t')
df.rename(columns = {'hate_offensive':'label'}, inplace = True)
df.rename(columns = {'Her pussy so good like I left something':'text'}, inplace = True)

stop_set = set()
with open('./stopwords_en.txt', 'r', encoding='utf8') as file:
    for line in file:
        word = line.strip()  # remove newline character from the end of the line
        stop_set.add(word)  # add the word to the set
# print("No. of stop words: ", len(stop_set))

def remove_stopwords(text):
    tokens = word_tokenize(text)
    # print(tokens)
    filtered_tokens = [word for word in tokens if word not in stop_set]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

# removing punctuations
def remove_punctuations(text):
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    return text

# remove punctuation from text
df['Clean Text'] = df['text'].apply(remove_punctuations)

# remove digits from text
df['Clean Text'] = df['Clean Text'].str.replace('\d+',' ')

# remove stop words
df['Clean Text'] = df['Clean Text'].apply(remove_stopwords)

df['label'] = df['label'].replace(['hate_offensive', 'not_hate_offensive'], [0,1])

# Split dataset into training and validation sets
train_df, val_df = train_test_split(df, test_size=0.2)

# Convert text data to TF-IDF vectors
vectorizer = TfidfVectorizer(sublinear_tf=True, smooth_idf=True)

train_X = vectorizer.fit_transform(train_df['Clean Text'])
# val_X = vectorizer.transform(val_df['Clean Text'])

# Convert labels to NumPy arrays
train_y = np.array(train_df['label'])
val_y = np.array(val_df['label'])

# Train KNN model on the training set
k = 18 # number of neighbors
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(train_X, train_y)

tdf = pd.DataFrame(data=[x])
val_X = vectorizer.transform(tdf[0])
pred = knn.predict(val_X)

label_dict = {
    0:'hate_abusive',
    1:'not_hate_abusive'
}

# print(label_dict[pred[0]])
# print(pred[0])
resindex = pred[0]
# print(label_dict[resindex])

with open('res.txt','w') as f:
    f.write(label_dict[resindex])
f.close()

# import pickle
# knnPickle = open('knnpickle_file', 'wb') 
      
# # source, destination 
# pickle.dump(knn, knnPickle)  

# # close the file

# knnPickle.close()