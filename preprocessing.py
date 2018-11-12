import pickle
import csv
import re
from collections import Counter
from nltk.corpus import stopwords
import warnings

warnings.filterwarnings("ignore")

with open("train.csv", 'r', encoding="ISO-8859-1") as file:
    data = list(csv.reader(file))
del data[0]

s = set(stopwords.words('english'))


def get_text(data, score):
    return " ".join([d[2].lower() for d in data if d[1] == str(score)])


negative_text = get_text(data, 0)
positive_text = get_text(data, 1)


def count_text(text):
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
    text = re.sub('@[^\s]+', 'USER', text)
    text = text.lower().replace("ё", "е")
    text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ', text)
    text = re.sub(' +', ' ', text)
    words = re.split("\s+", text)
    words = [word for word in words if word not in s and word != '']
    return Counter(words)


neg_count = count_text(negative_text)
pos_count = count_text(positive_text)


def get_y_count(score):
    return len([d for d in data if d[1] == str(score)])


pos_data_count = get_y_count(1)
neg_data_count = get_y_count(0)
prob_pos = pos_data_count / len(data)
prob_neg = neg_data_count / len(data)

pos_val = [pos_count, prob_pos, pos_data_count]
neg_val = [neg_count, prob_neg, neg_data_count]

features = [pos_val, neg_val]

with open("storefeatures.txt", "wb") as file:
    pickle.dump(features, file)
