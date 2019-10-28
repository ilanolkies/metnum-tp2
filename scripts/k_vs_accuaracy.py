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

	vectorizer = CountVectorizer(max_df=0.90, min_df=0.1, max_features=5000)

	vectorizer.fit(text_train)

	X_train, y_train = vectorizer.transform(text_train), (label_train == 'pos').values
	X_test, y_test = vectorizer.transform(text_test), (label_test == 'pos').values



	return X_train, y_train, X_test, y_test



def main(args):


	#Genero el rango de elementos a utilizar
	its = np.arange(args.k_Start, args.k_Stop, args.k_Step)

	its = [int(i) for i in its]

	alpha = args.alpha_Start

	'''
	Obteniendo datasets
	'''
	df = pd.read_csv("data/imdb_small.csv")

	#recortando data set para pruebas chiquitas

	df = df[:args.elem]

	'''
	Vectorizacion
	'''
	print("vectorizacion")

	X_train, y_train, X_test, y_test = get_instances(df)
	
	'''
	Procesando PCA
	'''
	print("PCA")
	if (alpha > 0):
		pca = PCA(alpha)
		
		pca.fit(X_train.toarray())

		X_train = pca.transform(X_train)
		#print(X_train)
		X_test = pca.transform(X_test)
		#print(X_train)


	accs = []



	'''
	El experimento, iterando en k
	'''
	print("KNN")
	for k in its:
		#print('K: {0}'.format(k))
		
		#Entrenamos KNN
		print("Entrenamiento")
		clf = KNNClassifier(k)
		clf.fit(X_train, y_train)

		print("predict")
		y_pred = clf.predict(X_test)
		print("accuracy")
		acc = accuracy_score(y_test, y_pred)
		accs.append(acc)

	print("KNN finalizado")


	fig, ax = plt.subplots()
	ax.plot(its, accs)

	_title = 'k vs. accuracy' if alpha == 0 else 'k vs. accuracy - Alpha = {0}'.format(alpha)
	ax.set(xlabel='k', ylabel='accuracy',title='title=_title')
	ax.grid()

	fig.savefig("results/k_vs_accuaracy_{0}.png".format(time.strftime("%Y%m%d-%H%M%S")))
	plt.show()







def positive_integer(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s Valor inválido, tiene que ser un numero natural." % value)
    return ivalue



if __name__ == '__main__':
<<<<<<< HEAD

	description = 'Versión del laboratorio de AED III del juego cuatro en linea para el TP3.'
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('--k_Start',
						type=positive_integer,
						default=1,
						help='Valor minimo de K.')
	parser.add_argument('--k_Stop',
						type=positive_integer,
						default=50,
						help='Valor maximo de K.')
	parser.add_argument('--k_Step',
						type=positive_integer,
						default=10,
						help="Diferencia entre cada alpha")
	parser.add_argument('--alpha_Start',
						type=positive_integer,
						default=0,
						help="Valor minimo de alpha")
	parser.add_argument('--alpha_Stop',
						type=positive_integer,
						default=15,
						help="Valor maximo Alpha")
	parser.add_argument('--alpha_Step',
						type=int,
						default=21,
						help="Diferencia entre cada alpha.")
	parser.add_argument('--elem',
						type=positive_integer,
						default=100,
						help='Cantidad de elementos tomados de la base de datos')

	args = parser.parse_args()

	assert args.k_Start > 0 
	assert args.k_Stop < args.elem
	assert args.k_Start <= args.k_Stop


	main(args)

