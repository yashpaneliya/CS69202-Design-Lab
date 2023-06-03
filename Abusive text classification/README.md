# Abusive Text Classification

## Problem Statement

This assignment is divided into 3 parts on the basis pf the machine learning model used for classification of abusive text. The first part is the implementation of the model using the KNN algorithm. The second part is the implementation of the model using the LSTM Neural Network. The third part is the implementation of the model using mBert and MURiL.

## Dataset

The dataset contains text messages in Hindi language with labels. The labels are 0 and 1. 0 represents non-abusive text and 1 represents abusive text.

Size of dataset: (20184, 2)

## Data Preprocessing

- Created a set of stop words in Hindi languages from several resources.
- Removed the stop words from the dataset sentences
- Removed punctuation marks from sentences
- Converted emojis to text equivalent representation using emot library
- Removed digits from text

## Part 1: [KNN](/Abusive%20text%20classification/Task_1.ipynb)

- Used the preprocessed data to tokenize and calculate tf-idf values using
TfIdfVectorizer
- Split dataset into 80:20 split for training and testing
- Fitted the train data and tested on test data

## Part 2: [LSTM](/Abusive%20text%20classification/Task_2.ipynb)

- Created a class for LSTM architecture with the following layers, activation function, and dimensions
    ```
    LSTM(
        (embedding): Embedding(29941, 300)
        (lstm): LSTM(300, 600, num_layers=2, batch_first=True, dropout=0.3)
        (fc): Linear(in_features=600, out_features=1, bias=True)
        (dropout): Dropout(p=0.3, inplace=False)
        (sig): Sigmoid()
    )
    ```
- Created vectorized dataset using `word_tokenizer()`
- Padded all the sentences to a maximum length
- Split the dataset into an 80:20 ratio
- Trained the model with the below hyper-parameters
    ```
    vocab_size = len(vocab)
    embedding_dim = 300
    hidden_dim = 600
    num_layers = 2
    epochs = 10
    lr = 0.001
    ```
- Also embedded the logic of early stopping by maintaining a counter.

## Part 3: [mBert and MURiL](/Abusive%20text%20classification/Task_3.ipynb)

- Tokenized and encoded the dataset using hugging face's
“bert-base-multilingual-cased” and “google/muril-base-cased” tokenizer.
- Fine-tuned prebuilt model for the same mBert and MURiL architecture

## Results

| Model | Accuracy | Macro F1 Score |
| --- | --- | --- |
| KNN (k=18) | 64 | 62 |
| LSTM | 78.30 | 78.09 |
| mBert | 82.44 | 82.17 |
| MURiL | 85.29 | 84.98 |