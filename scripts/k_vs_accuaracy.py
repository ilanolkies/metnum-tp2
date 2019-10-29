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

def evaluate_knn(k_range, X_train, y_train, X_test, y_test, reps):
  accs = []

  # kNN
  for k in k_range:
    t = 0

    for i in range(reps):
      clf = KNNClassifier(k)
      clf.fit(X_train, y_train)
      y_pred = clf.predict(X_test)
      t += accuracy_score(y_test, y_pred)

    accs.append(t/reps)

  return accs

def main(args):
  # datasets de train y test
  df = pd.read_csv("data/imdb_small.csv")

  #recortando data set para pruebas chiquitas
  if(args.elem > 0):
    df = df[:args.elem]

  X_train, y_train, X_test, y_test = get_instances(df)

  alpha = args.alpha_Start

  # rango de k
  k_range = np.arange(args.k_Start, args.k_Stop, args.k_Step)

  # rango de alpha
  alpha_range = np.arange(alpha, args.alpha_Stop, args.alpha_Step)

  # resultados de accuaracies para cada alpha
  results = []

  if (alpha > 0):
    # PCA
    
    for alpha in alpha_range:
      pca = PCA(alpha)
      #print("fit")
      pca.fit(X_train.toarray())
      #print("trainx")
      X_train_aux = pca.transform(X_train)
      #print("train_test")
      X_test_aux = pca.transform(X_test)

      # resultados de accuaracy con cada k
      accs = evaluate_knn(k_range, X_train_aux, y_train, X_test_aux, y_test, args.reps)
      results.append(accs)
  else:
    # resultados de accuaracy con cada k
    accs = evaluate_knn(k_range, X_train, y_train, X_test, y_test, args.reps)
    results.append(accs)

  if (alpha > 0):
    for i, result in enumerate(results):

      plt.plot(k_range, result, label='alpha = {0}'.format(alpha_range[i]))
  else:
    plt.plot(k_range, results[0], label='sin pca')

  plt.xlabel('k')
  plt.ylabel('accuaracy')
  plt.legend()
  plt.savefig('results/k_vs_accuaracy-{}'.format(time.strftime("%Y%m%d-%H%M%S")))
  plt.show()

  '''
  fig, ax = plt.subplots()
  ax.plot(its, accs)

  _title = 'k vs. accuracy' if alpha == 0 else 'k vs. accuracy - Alpha = {0}'.format(alpha)
  ax.set(xlabel='k', ylabel='accuracy',title='title=_title')
  ax.grid()

  fig.savefig("results/k_vs_accuaracy_{0}.png".format(time.strftime("%Y%m%d-%H%M%S")))
  plt.show()
  '''

def positive_integer(value):
  ivalue = int(value)
  if ivalue < 0:
    raise argparse.ArgumentTypeError("%s Valor inválido, tiene que ser un numero natural." % value)
  return ivalue

if __name__ == '__main__':
  description = 'Acuraccy.'

  parser = argparse.ArgumentParser(description=description)

  parser.add_argument(
    '--k_Start',
    type=positive_integer,
    default=1,
    help='Valor minimo de k'
  )
  parser.add_argument(
    '--k_Stop',
    type=positive_integer,
    default=50,
    help='Valor maximo de k'
  )
  parser.add_argument(
    '--k_Step',
    type=positive_integer,
    default=10,
    help='Salto de k'
  )
  parser.add_argument(
    '--alpha_Start',
    type=positive_integer,
    default=0,
    help='Valor minimo de alpha'
  )
  parser.add_argument(
    '--alpha_Stop',
    type=positive_integer,
    default=50,
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
    default=1000,
    help='Poda bruta de comentarios'
  )
  parser.add_argument(
    '--reps',
    type=positive_integer,
    default=10,
    help='Repeticiones de kNN'
  )
  args = parser.parse_args()

  assert args.k_Start > 0
  #assert args.k_Stop < args.elem
  assert args.k_Start <= args.k_Stop

  main(args)
