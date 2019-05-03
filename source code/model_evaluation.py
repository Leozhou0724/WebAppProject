'''
ECE 568 Webapp Project
Team#1

Written by: Jiachen Ding  jd1287
2019/5/1
'''
# -*- coding: utf-8 -*-

from sklearn.metrics import explained_variance_score, mean_absolute_error, mean_squared_error, median_absolute_error, \
    r2_score


def model_evaluation(y_true, y_pred):
    metrics = _cal_metrics(y_true, y_pred)
    for (k, v) in metrics.items():
        print(k + ": " + str(v))


def _cal_metrics(y_true, y_pred):
    re = _calc_re(y_true, y_pred)
    metrics = {
        "explained_variance_score":
            explained_variance_score(y_true, y_pred),
        "mean_absolute_error":
            mean_absolute_error(y_true, y_pred),
        "mean_squared_error":
            mean_squared_error(y_true, y_pred),
        "median_absolute_error":
            median_absolute_error(y_true, y_pred),
        "r2_score":
            r2_score(y_true, y_pred),
        "sum_relative_error":
            re[0],
        "mean_relative_error":
            re[1],
    }

    return metrics


def _calc_re(y_true, y_pred):
    return [((y_true - y_pred) / y_pred).sum().values, ((y_true - y_pred) / y_pred).mean().values]


if __name__ == '__main__':
    pass
