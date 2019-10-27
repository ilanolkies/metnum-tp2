# Scripts

Los scripts se corren desde la carpeta root en el entorno de `pyenv`.

Los resultados se guardan en la carpeta `results` con el nombre del script y la hora de ejecución.

## K vs. Accuaracy

```
python scripts/k_vs_accuaracy.py FROM TO NUM ALPHA
```

- `START`: parámetro `start` de `np.logspace` -- no usar sin `STOP`
- `STOP`: parámetro `stop` de `np.logspace`
- `NUM`: cantidad de muestras a tomar -- deafult: 50
- `ALPHA`: parametro alpha para PCA -- default: sin PCA

> `np.logspace`: https://docs.scipy.org/doc/numpy/reference/generated/numpy.logspace.html
