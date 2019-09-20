# Estas dos líneas permiten que python encuentre la librería sentiment en notebooks/
import sys
sys.path.append("notebooks/")
import pandas as pd
from sklearn.metrics import accuracy_score

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python evaluate.py archivo_predicciones archivo_labels")
        exit(-1)

    path_pred = sys.argv[1]
    path_true = sys.argv[2]

    df_pred = pd.read_csv(path_pred, index_col=0)
    df_true = pd.read_csv(path_true, index_col=0)

    acc = accuracy_score(df_true["label"], df_pred["label"])

    print("Accuracy: {}".format(acc))
