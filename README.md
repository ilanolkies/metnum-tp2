# KNN-Sentiment: TP2 de Métodos Numéricos

## Instrucciones

En `data/` están los datasets. Usaremos `imdb_small.csv` (6K de train, 6K de test).

En `src/` está el código de C++, en particular en `src/sentiment.cpp` está el entrypoint de pybind.

En `notebooks/` hay ejemplos para correr partes del TP usando sklearn y usando la implementación en C++.

Necesitamos bajar las librerías `pybind` y `eigen` (el "numpy" de C++), para eso bajamos los submódulos como primer paso.

Versión de Python >= 3.6.5


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
