"""
This module define evaluation metrics.
"""

import numpy as np
from munkres import Munkres
from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score
from sklearn.metrics.cluster import contingency_matrix
from sklearn.metrics import confusion_matrix
from scipy.optimize import linear_sum_assignment


def clf_accuracy(labels, outputs) -> float:
    """
    Compute the classification accuracy, given the outputs and labels for all images.

    Args:
        outputs (np.ndarray): dimension (batch_size,)
        labels (np.ndarray): dimension (batch_size,) where each element is a value in [0, 1, 2, ..., L]

    Returns (float): accuracy in [0,1]
    """
    outputs = np.argmax(outputs, axis=1)
    return np.sum(outputs == labels) / float(labels.size)


def nmi(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    compute normliazed mutual information score
    Args:
        y_true: shape is (n_smaples,)
        y_pred: shape is (n_samples,)
    """
    return normalized_mutual_info_score(y_true, y_pred)


def ari(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    compute adjusted normliazed mutual information score
    Args:
        y_true: shape is (n_smaples,)
        y_pred: shape is (n_samples,)
    """
    return adjusted_rand_score(y_true, y_pred)


def purity_score(y_true: np.ndarray, y_pred: np.ndarray):
    """
    Args:
        y_true: shape is (n_smaples,)
        y_pred: shape is (n_samples,)
    """
    # compute contingency matrix (also called confusion matrix)
    cont_matrix = contingency_matrix(y_true, y_pred)
    return np.sum(np.amax(cont_matrix, axis=0)) / np.sum(cont_matrix)


def cluster_acc(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate clustering accuracy. Require scikit-learn installed
    Args
        y_true: with shape (n_samples,)
        y_pred: with shape (n_samples,)
    """
    y_true = y_true.astype(np.int64)
    y_pred = np.argmax(y_pred, axis=1)
    assert y_pred.size == y_true.size
    D = max(y_pred.max(), y_true.max()) + 1
    w = np.zeros((D, D), dtype=np.int64)
    for i in range(y_pred.size):
        w[y_pred[i], y_true[i]] += 1
    ind = linear_sum_assignment(w.max() - w)
    ind = np.array([ind[0], ind[1]]).T
    return sum([w[i, j] for i, j in ind]) * 1.0 / y_pred.size


metrics = {
    'accuracy': cluster_acc,
    "nmi": nmi,
    "ari": ari,
    "purity": purity_score
}