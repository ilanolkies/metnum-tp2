from sklearn import datasets
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml
from sklearn.feature_extraction.text import CountVectorizer
import os

def get_instances(df, max_df=0.90, min_df=0.1):
  text_train = df[df.type == 'train']["review"]
  label_train = df[df.type == 'train']["label"]

  text_test = df[df.type == 'test']["review"]
  label_test = df[df.type == 'test']["label"]

  vectorizer = CountVectorizer(max_df=max_df, min_df=min_df, max_features=5000)

  vectorizer.fit(text_train)

  X_train, y_train = vectorizer.transform(text_train), (label_train == 'pos').values
  X_test, y_test = vectorizer.transform(text_test), (label_test == 'pos').values

  return X_train, y_train, X_test, y_test

# datasets de train y test
df = pd.read_csv("data/imdb_small.csv")

X_train, y_train, X_test, y_test = get_instances(df)

M = (X_train - X_train.mean(axis=0))

cov_matrix = M.T @ M / (M.shape[0]-1)

w, V = np.linalg.eig(cov_matrix)

# A veces aparecen números complejos acá. Los descartamos
w = np.real(w)
V = np.real(V)

np.savetxt('results/predict_eigen_v.txt', w)
np.savetxt('results/predict_eigen_W.txt', V)
