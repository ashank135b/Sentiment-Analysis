import numpy as np
import pandas as pd
import pickle
import re
from collections import Counter
from nltk.corpus import stopwords

s = set(stopwords.words('english'))

with open("storefeatures.txt", "rb") as file:
    features = pickle.load(file)

pos_val = features[0]
neg_val = features[1]

pos_count, prob_pos, pos_data_count = pos_val[0], pos_val[1], pos_val[2]
neg_count, prob_neg, neg_data_count = neg_val[0], neg_val[1], neg_val[2]


def make_class_prediction(text, counts, class_prob):
    prediction = 1
    text_count = Counter(re.split("\s+", text))
    # print(text_count)
    for word in text_count:
        if word not in s and word.isalpha():
            prediction *= text_count.get(word) * (counts.get(word, 0) + 1) / (sum(counts.values()))
    return prediction * class_prob


print(make_class_prediction("happy", neg_count, prob_neg), make_class_prediction("happy", pos_count, prob_pos))


def predict(text):
    neg_pred = make_class_prediction(text, neg_count, prob_neg)
    pos_pred = make_class_prediction(text, pos_count, prob_pos)
    if neg_pred > pos_pred:
        return -1
    else:
        return 1
