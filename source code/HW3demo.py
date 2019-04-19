# HW3
# Yuhang Zhou
# yz853
import numpy as np
import matplotlib.pyplot as plt
import csv
import os


def pred(x):
    data = []
    # read data from cvs file
    datan = 'Data'+str(x)
    with open("demodata.csv", 'r') as f:
        reader = csv.reader(f)
        fieldnames = next(reader)
        csv_reader = csv.DictReader(f, fieldnames=fieldnames)
        for row in csv_reader:
            d = {}
            for k, v in row.items():
                d[k] = float(v)
            data.append(d[datan])

    # choose which dataset as the training data

    x_train = np.linspace(0, 0.9, 10)
    y_train = []
    for i in range(10):
        y_train.append(data[i])
    y_train = np.array(y_train)
    x_test = np.linspace(0, 1, 101)

    # φ(x), set M=9
    X_train = np.empty([10, 10])
    for i in range(10):
        for j in range(10):
            X_train[i][j] = x_train[i]**j
    X_test = np.empty([101, 10])
    for i in range(101):
        for j in range(10):
            X_test[i][j] = x_test[i]**j

    alpha = 0.001
    beta = 2

    # Inverse of S
    S_inv = alpha*np.eye(10)+beta*np.matmul(X_train.T, X_train)
    S = np.linalg.inv(S_inv)
    mean = beta*np.matmul(S, np.matmul(X_train.T, y_train))
    # result
    y = np.matmul(X_test, mean)
    # Varience
    y_var = 1/beta+np.sum(np.matmul(X_test, S)*X_test, axis=1)
    y_std = np.sqrt(y_var)

    #print("Training data: ",y_train)

    fig = plt.figure(figsize=(12, 8))
    plt.scatter(x_train, y_train, edgecolor="b", s=50, label="Training data")
    plt.plot(x_test, y, c="r", label="Prediction curve")
    plt.fill_between(x_test, y - y_std, y + y_std, color="pink",
                     label="Standard Deviation", alpha=0.5)
    plt.legend(loc=2)
    fig_dict = "static\images\predict.png"
    fig.savefig("static\images\predict.png")
    #fig.savefig("predict.png")
    # plt.show()
    return y[100],fig_dict

