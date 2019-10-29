import sys
sys.path.append("notebooks/")

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sentiment import PCA, KNNClassifier
import matplotlib
import matplotlib.pyplot as plt
import time
import argparse

# para un dataset `df`
# obtiene instancias de train y test
# crea el modelo de bolsa de palabras
# y poda los datos desde el `min_df` al `max_df`
def get_instances(df, max_df=0.90, min_df=0.01):
  text_train = df[df.type == 'train']["review"]
  label_train = df[df.type == 'train']["label"]

  text_test = df[df.type == 'test']["review"]
  label_test = df[df.type == 'test']["label"]

  vectorizer = CountVectorizer(max_df=max_df, min_df=min_df, max_features=5000)

  vectorizer.fit(text_train)

  X_train, y_train = vectorizer.transform(text_train), (label_train == 'pos').values
  X_test, y_test = vectorizer.transform(text_test), (label_test == 'pos').values

  return X_train, y_train, X_test, y_test

def main(args):
  # datasets de train y test
  df = pd.read_csv("data/imdb_small.csv")

  x_poda_frec = np.arange(args.from, args.to, args.step)
  y_poda_frec = []

  for i in x_poda_frec:
    X_train, y_train, X_test, y_test = get_instances(df, i)

    k = 10
    alpha = 50

    #pca
    pca = PCA(alpha)
    pca.fit(X_train.toarray())
    X_train_aux = pca.transform(X_train)
    X_test_aux = pca.transform(X_test)

    #knn
    clf = KNNClassifier(k)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    y_poda_frec.append(acc)

  fig, ax1 = plt.subplots()

  plt.plot(x_poda_frec, y_poda_frec, label='k = 10, alpha = 50'.format(k_range[i]))
  plt.xlabel('max_df')
  plt.ylabel('accuaracy')
  plt.legend()
  plt.savefig('results/max_df_accuaracy-{}'.format(time.strftime("%Y%m%d-%H%M%S")))
  plt.show()

def positive_integer(value):
  ivalue = int(value)
  if ivalue < 0:
    raise argparse.ArgumentTypeError("%s Valor inválido, tiene que ser un numero natural." % value)
  return ivalue

if __name__ == '__main__':
  description = 'Acuraccy.'

  parser = argparse.ArgumentParser(description=description)

  parser.add_argument(
    '--from',
    type=positive_integer,
    default=40,
    help='Valor minimo de poda de no frecuentes'
  )
  parser.add_argument(
    '--to',
    type=positive_integer,
    default=200,
    help='Valor maximo de poda de no frecuentes'
  )
  parser.add_argument(
    '--step',
    type=positive_integer,
    default=10,
    help='Salto de poda de no frecuentes'
  )
  args = parser.parse_args()

  main(args)
