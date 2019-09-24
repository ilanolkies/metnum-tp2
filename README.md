# KNN-Sentiment: TP2 de Métodos Numéricos

## Instrucciones


### Clonar Repo

NO HACER FORK! 

Primero, crearse un repo en algún otro lugar. Luego, clonar este repo de la siguiente manera:

```
git clone git@github.com:finiteautomata/metnum-tp2-20192c.git
```

Cambiar el repositorio al que hayamos creado

```
git remote remove origin
git remote add origin <nuestra-nueva-url-de-git>
```

Listo. Ya pueden disfrutar del TP2

### Datos

En `data/` tenemos que descomprimir el dataset de IMDB, que lo pueden [bajar de acá](https://campus.exactas.uba.ar/pluginfile.php/143556/course/section/19842/imdb.tar.gz)

### Otros directorios

En `src/` está el código de C++, en particular en `src/sentiment.cpp` está el entrypoint de pybind.

En `notebooks/` hay ejemplos para correr partes del TP usando sklearn y usando la implementación en C++.

### Submódulos y librerías necesarias
Necesitamos bajar las librerías `pybind` y `eigen` (el "numpy" de C++), para eso bajamos los submódulos como primer paso.

Versión de Python >= 3.6.5

1. Bajar submódulos
```
git submodule init
git submodule update
```
2. Instalar dependencias
```
pip install -r requirements.txt
```

3. Compilar
```
mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make clean && make && make install
```
4. Correr jupyter notebooks
```
jupyter lab
```

## Creación de un entorno virtual de python

### Con pyenv

```
curl https://pyenv.run | bash
```

Luego, se sugiere agregar unas líneas al bashrc. Hacer eso, **REINICIAR LA CONSOLA** y luego...

```
pyenv install 3.6.5
pyenv global 3.6.5
pyenv virtualenv 3.6.5 tp2
```

En el directorio del proyecto

```
pyenv activate tp2
```

### Directamente con python3
```
python3 -m venv tp2
source tp2/bin/activate
```

### Con Conda
```
conda create --name tp2 python=3.6.5
conda activate tp2
```

## Instalación de las depencias
```
pip install -r requirements.txt
```

## Correr notebooks de jupyter

```
cd notebooks
jupyter lab
```
o  notebook
```
jupyter notebook
```


## Compilación
Ejecutar la primera celda del notebook `knn.ipynb` o seguir los siguientes pasos:


- Compilar el código C++ en un módulo de python
```
mkdir build
cd build
rm -rf *
cmake -DPYTHON_EXECUTABLE="$(which python)" -DCMAKE_BUILD_TYPE=Release ..
```
- Al ejecutar el siguiente comando se compila e instala la librería en el directorio `notebooks`
```
make install
```

## Prueba de clasificación

1. Compilar la librería

```
cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make clean && make && make install
```

2. Correr clasificación sobre sample

```
python bin/classify.py data/test_sample.csv data/test_sample.out
```

3. Correr evaluación

```
python bin/evaluate.py data/test_sample.out data/test_sample.true
```


