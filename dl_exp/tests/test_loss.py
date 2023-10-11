import numpy as np
from .. import metrics

y_true = np.random.rand(10, 1)
y_pred = np.random.rand(10, 1)


print("clf acc", metrics.clf_acc(y_true, y_pred))
print("acc", metrics.cluster_acc(y_true, y_pred))
print("purity", metrics.purity(y_true, y_pred))
print("nmi", metrics.nmi(y_true, y_pred))

