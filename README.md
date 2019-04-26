# KNN-Sentiment: TP2 de Métodos Numéricos

## Instrucciones

En `data/` están los datasets. Usaremos `imdb_small.csv` (6K de train, 6K de test).

En `src/` está el código de C++, en particular en `src/sentiment.cpp` está el entrypoint de pybind.

En `notebooks/` hay ejemplos del TP hechos usando sklearn, otros implementaciones propias en Python y finalmente una usando la implementación en C++.

Necesitamos bajar las librerías `pybind` y `eigen` ("numpy" de C++), para eso bajamos los submódulos en el primer paso.

Versión de Python: 3.6.5

```
## Con pyenv

```
curl https://pyenv.run | bash
```

Luego, sugiere agregar unas líneas al bashrc. Hacer eso, **REINICIAR LA CONSOLA** y luego...

```
pyenv install 3.6.5
pyenv global 3.6.5
pyenv virtualenv 3.6.5 tp2

# En el directorio del proyecto
pyenv activate tp2
pip install -r requirements.txt
```



0. Descomprimir datasets
```
cd data
tar -xvf data.tgz
```
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
cmake .
make
```
4. Correr jupyter lab
```
cd notebooks
jupyter lab
```
o  notebook
```
jupyter notebook
```
