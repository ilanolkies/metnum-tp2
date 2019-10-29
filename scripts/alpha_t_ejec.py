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

  #recortando data set para pruebas chiquitas
  if(args.elem > 0):
    df = df[:args.elem]

  X_train, y_train, X_test, y_test = get_instances(df)

  k = args.k

  # rango de alpha
  alpha_range = np.arange(args.alpha_Start, args.alpha_Stop, args.alpha_Step)

  y_alpha = []
  y_time = []

  for alpha in alpha_range:
    t0 = time.time()
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

    y_alpha.append(acc)

  fig, ax1 = plt.subplots()

  color = 'tab:red'
  ax1.set_xlabel('Alpha')
  ax1.set_ylabel('Accuaracy', color=color)
  ax1.plot(alpha_range, y_alpha, color=color)
  ax1.tick_params(axis='y', labelcolor=color)
  plt.xticks(rotation=90)
  ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

  color = 'tab:blue'
  ax2.set_ylabel('Tiempo de ejec.', color=color)  # we already handled the x-label with ax1
  ax2.plot(alpha_range, y_time, color=color)
  ax2.tick_params(axis='y', labelcolor=color)

  fig.tight_layout()  # otherwise the right y-label is slightly clipped

  fig.savefig("results/epsilon_vs_error_2_{0}.png".format(time.strftime("%Y%m%d-%H%M%S")))
  plt.show()

  plt.clf()

def positive_integer(value):
  ivalue = int(value)
  if ivalue < 0:
    raise argparse.ArgumentTypeError("%s Valor inválido, tiene que ser un numero natural." % value)
  return ivalue

if __name__ == '__main__':
  description = 'Acuraccy.'

  parser = argparse.ArgumentParser(description=description)

  parser.add_argument(
    '--k',
    type=positive_integer,
    default=40,
    help='Valor minimo de k'
  )
  parser.add_argument(
    '--alpha_Start',
    type=positive_integer,
    default=50,
    help='Valor minimo de alpha'
  )
  parser.add_argument(
    '--alpha_Stop',
    type=positive_integer,
    default=200,
    help='Valor maximo de alpha'
  )
  parser.add_argument(
    '--alpha_Step',
    type=positive_integer,
    default=10,
    help='Salto de alpha'
  )
  parser.add_argument(
    '--elem',
    type=int,
    default=12000,
    help='Poda bruta de comentarios'
  )
  args = parser.parse_args()

  main(args)
