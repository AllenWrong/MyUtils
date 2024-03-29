from sklearn.metrics import normalized_mutual_info_score, accuracy_score
from scipy.optimize import linear_sum_assignment
import numpy as np


def clf_acc(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """return clf acc

    Args:
        y_true (np.ndarray): 
        y_pred (np.ndarray):

    Returns:
        float: acc value
    """
    return accuracy_score(y_true, y_pred)


def cluster_acc(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """return cluster acc

    Args:
        y_true (np.ndarray): 
        y_pred (np.ndarray):

    Returns:
        float: acc value
    """
    y_true = y_true.reshape(-1)
    y_pred = y_pred.reshape(-1)

    y_true = y_true.astype(np.int64)
    assert y_pred.size == y_true.size
    D = max(y_pred.max(), y_true.max()) + 1
    w = np.zeros((D, D), dtype=np.int64)
    for i in range(y_pred.size):
        w[y_pred[i], y_true[i]] += 1
    u = linear_sum_assignment(w.max() - w)
    ind = np.concatenate([u[0].reshape(u[0].shape[0], 1), u[1].reshape([u[0].shape[0], 1])], axis=1)
    return sum([w[i, j] for i, j in ind]) * 1.0 / y_pred.size


def purity(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """purity

    Args:
        y_true (np.ndarray): 
        y_pred (np.ndarray): 

    Returns:
        float: pur value
    """
    y_true = y_true.reshape(-1)
    y_pred = y_pred.reshape(-1)
    
    y_voted_labels = np.zeros(y_true.shape)
    labels = np.unique(y_true)
    ordered_labels = np.arange(labels.shape[0])
    for k in range(labels.shape[0]):
        y_true[y_true == labels[k]] = ordered_labels[k]
    labels = np.unique(y_true)
    bins = np.concatenate((labels, [np.max(labels)+1]), axis=0)

    for cluster in np.unique(y_pred):
        hist, _ = np.histogram(y_true[y_pred == cluster], bins=bins)
        winner = np.argmax(hist)
        y_voted_labels[y_pred == cluster] = winner

    return accuracy_score(y_true, y_voted_labels)


def nmi(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """nmi

    Args:
        y_true (np.ndarray): 
        y_pred (np.ndarray): 

    Returns:
        float: nmi value
    """
    y_true = y_true.reshape(-1)
    y_pred = y_pred.reshape(-1)
    return normalized_mutual_info_score(y_true, y_pred)
