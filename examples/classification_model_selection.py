import pandas as pd
from river.linear_model import LogisticRegression
from sail.imla.river.naive_bayes import BernoulliNB
from sklearn.preprocessing import StandardScaler
import time
import ray
import numpy as np
from sklearn.metrics import accuracy_score
from sail.model_selector.holdout_best_model import HoldoutBestModelSelector


ray.init(local_mode=True)

scaler = StandardScaler()

sgd = LogisticRegression()
bnb = BernoulliNB()

offline_model = HoldoutBestModelSelector(estimators=[sgd, bnb],
                                         metrics=accuracy_score)

# Ingestion
for index in range(2):
    csv_file = "../datasets/agrawal_gen_2000.csv"
    X = pd.read_csv(csv_file,
                    names=["x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "y"])

    y = X['y'].values
    X.drop("y", axis=1, inplace=True)
    X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
    y = y.reshape(len(y), 1)
    X = X.to_numpy()


    start = time.time()
    offline_model.partial_fit(X, y, np.unique(y))
    delta = time.time() - start
    print(f"({delta:.3f} seconds)")

print(offline_model.best_model_index)
print(offline_model.get_best_model())
