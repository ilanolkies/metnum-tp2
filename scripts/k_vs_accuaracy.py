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

def get_instances(df):
  text_train = df[df.type == 'train']["review"]
  label_train = df[df.type == 'train']["label"]

  text_test = df[df.type == 'test']["review"]
  label_test = df[df.type == 'test']["label"]

  print("Cantidad de instancias de entrenamiento = {}".format(len(text_train)))
  print("Cantidad de instancias de test = {}".format(len(text_test)))

  print("Class balance : {} pos {} neg".format(
    (label_train == 'pos').sum() / label_train.shape[0],
    (label_train == 'neg').sum() / label_train.shape[0]
  ))

  vectorizer = CountVectorizer(max_df=0.70, min_df=0.1, max_features=5000)

  vectorizer.fit(text_train)

  X_train, y_train = vectorizer.transform(text_train), (label_train == 'pos').values
  X_test, y_test = vectorizer.transform(text_test), (label_test == 'pos').values

  return X_train, y_train, X_test, y_test

if __name__ == '__main__':
  '''
  Obteniendo parametros para test
  '''
  its = np.logspace(1, 100)
  if len(sys.argv) > 3:
    its = np.logspace(float(sys.argv[1]), float(sys.argv[2]), num = int(sys.argv[3]))
  elif len(sys.argv) > 1:
    its = np.logspace(float(sys.argv[1]), float(sys.argv[2]))

  its = [int(i) for i in its]

  alpha = int(sys.argv[4]) if len(sys.argv) > 4 else 0

  '''
  Obteniendo datasets
  '''
  df = pd.read_csv("data/imdb_small.csv")

  #recortando data set para preubas chiquitas
  df = df[:100]

  '''
  Vectorizacion
  '''
  X_train, y_train, X_test, y_test = get_instances(df)

  '''
  Procesando PCA
  '''
  if (alpha > 0):
    pca = PCA(alpha)
    pca.fit(X_train.toarray())
    X_train = pca.transform(X_train)
    X_test = pca.transform(X_test)


  accs = []
  '''
  El experimetno, iterando en k
  '''
  for k in its:
    print('K: {0}'.format(k))
    # Entrenamos KNN
    clf = KNNClassifier(k)
    clf.fit(X_train, y_train)

    # Testeamos
    y_pred = clf.predict(X_test).reshape(-1)

    acc = accuracy_score(y_test, y_pred)
    accs.append(acc)

  fig, ax = plt.subplots()
  ax.plot(its, accs)

  _title = 'k vs. accuaracy' if alpha == 0 else 'k vs. accuaracy - Alpha = {0}'.format(alpha)
  ax.set(xlabel='k', ylabel='accuaracy',
        title=_title)
  ax.grid()

  fig.savefig("results/k_vs_accuaracy_{0}.png".format(time.strftime("%Y%m%d-%H%M%S")))
  plt.show()
