from glob import glob
import numpy
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from matplotlib import pyplot
import pickle
import joblib
import time

nparray = numpy.array
pyplot.style.use('dark_background')


file_names = glob("/home/robofei/Documents/DataAnalyse/ALL/*Passe.csv")

# print(file_names)

array_passe: nparray = []


for f in file_names:
    array_passe.append(
        numpy.genfromtxt(
            f,
            dtype=int,
            delimiter=";",
            skip_header=1
        )
    )

array_passe = numpy.concatenate(array_passe)

y: nparray = array_passe[:, 0]
X: nparray = array_passe[:, [1, 2, 3,  4, 4, 6, 7, 8]]

x_axis: nparray = range(1, 50, 1)
score_train: nparray = []
score_test: nparray = []

start: float = time.time()
for i in x_axis:

    [X_train, X_test, y_train, y_test] = train_test_split(
        X, y, test_size=.2, random_state=i
        )

    gradient: GradientBoostingRegressor = GradientBoostingRegressor(
        loss='ls',
        learning_rate=.4,
        n_estimators=5,
        subsample=.79,
        criterion='friedman_mse',
        min_samples_split=.01,
        min_samples_leaf=.07,
        min_weight_fraction_leaf=0,
        max_depth=10,
        min_impurity_decrease=0.0,
        min_impurity_split=None,
        init=None,
        random_state=5*i,
        max_features='auto',
        alpha=0.9,
        verbose=0,
        max_leaf_nodes=None,
        warm_start=False,
        presort='deprecated',
        validation_fraction=0.1,
        n_iter_no_change=None,
        tol=1e-4,
        ccp_alpha=0.0
    ).fit(X_train, y_train)

    score_test.append(gradient.score(X_test, y_test))
    score_train.append(gradient.score(X_train, y_train))

end: float = time.time()

print("Score test: ", numpy.mean(score_test))
print("Score train: ", numpy.mean(score_train))
print("Time of operation: {} ms".format(
    (end-start)*1e3/(numpy.size(x_axis)*numpy.size(y)))
      )

pyplot.plot(x_axis, score_test, 'c-', label='Test score')
pyplot.plot(x_axis, score_train, 'r-', label='Train score')
pyplot.xlabel('???')
pyplot.ylabel('score')
pyplot.legend(loc="upper right")
pyplot.grid()

pyplot.show()
