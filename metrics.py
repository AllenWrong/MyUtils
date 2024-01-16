from torchmetrics import AUROC, Accuracy, Precision, Recall, F1Score
from enum import Enum


class Metrics(Enum):
    acc = 0
    auc = 1
    precision = 2
    recall = 3
    f1 = 4


def get_metric_dict(num_classes, metrics):
    """
    Args:
        num_classes: number of classes
        metrics_dict: `{Metrics.acc: None, Metrics.auc: None,....}`
    Return:
        `{Metrics.acc: Accuracy(num_classes=num_classes, average='macro'),...}`
    """
    task_type = 'binary' if num_classes == 2 else 'multiclass'
    metrics_dict = {}

    for key in metrics:
        if key == Metrics.acc:
            metrics_dict[key] = Accuracy(task=task_type, average='macro', num_classes=num_classes)
        elif key == Metrics.auc:
            metrics_dict[key] = AUROC(num_classes=num_classes, task=task_type)
        elif key == Metrics.precision:
            metrics_dict[key] = Precision(num_classes=num_classes, average='macro', task=task_type)
        elif key == Metrics.recall:
            metrics_dict[key] = Recall(num_classes=num_classes, average='macro', task=task_type)
        elif key == Metrics.f1:
            metrics_dict[key] = F1Score(num_classes=num_classes, average='macro', task=task_type)
        else:
            raise ValueError(f"unsupported metric name {key.name}")

    return metrics_dict


metrics = get_metric_dict(3, [Metrics.acc, Metrics.auc, Metrics.precision, Metrics.recall, Metrics.f1])
