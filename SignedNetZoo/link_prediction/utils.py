import numpy as np


def confusion_matrix(y_true, y_pred, pos_label=1):
    """
    Function to return a confusion matrix given a set of predictions
    and ground truths.

    Args:
        y_true : List of ground truths
        y_pred : List of predictions
        pos_label : value to consider as positive. Default: 1

    Returns:
        dict with true positives, true negatives, false positives and false negatives
    """
    cm = {'TP': 0, 'FP': 0, 'FN': 0, 'TN': 0}
    for true, pred in zip(y_true, y_pred):
        if true == pred == 1:
            cm['TP'] += 1
        elif true == pred == -1:
            cm['TN'] += 1
        elif true == -pred == -1:
            cm['FP'] += 1
        elif true == -pred == 1:
            cm['FN'] += 1
    return cm
