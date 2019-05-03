'''
ECE 568 Webapp Project
Team#1

Written by: Yuhang Zhou  yz853
2019/5/1
'''
import numpy as np
import matplotlib.pyplot as plt
import csv
import torch
import torch.utils.data
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch.optim as optim


def svm_model(company, training_length):
    price = []
    volume = []
    ma = []  # Moving Average
    with open('dataset/{}.csv'.format(company)) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            price.append(float(row[4]))
            volume.append(float(row[5]))
    
    #price = np.array(price)
    #volume = np.array(volume)
    x = []
    y = []
    for i in range(training_length, len(price)-training_length):
        tmp = []
        tmp.append(price[i])
        tmp.append(volume[i])
        tmp_ma = 0.0
        for j in range(i - training_length, i):
            tmp_ma += price[j]
        tmp_ma = tmp_ma / training_length
        tmp.append(tmp_ma)
        x.append(tmp)  # trainning data
        y.append(price[i + training_length])

    x = np.array(x)
    y = np.array(y).reshape(-1, 1)
    x0 = x[0]
    y0 = y[0]
    x = (x / x0)-1
    y = (y / y0) - 1
    x = x[:, np.newaxis,:]
    y=y[:, np.newaxis,:]

    x = torch.from_numpy(x).float()
    y = torch.from_numpy(y).float()
    x_nonbatch = x
    y_nonbatch = y

    print(x.shape)
    print(y.shape)

    device = torch.device('cpu')
    batch_size = 128
    D_in = 3
    H1 = 10
    H2 = 5
    D_out = 1

    train = torch.utils.data.TensorDataset(x, y)
    train_loader = torch.utils.data.DataLoader(
        train, batch_size=batch_size, shuffle=False)
    learning_rate = 0.01
    weight_decay = 0.001

    model = nn.Sequential(
        
        
        nn.Linear(D_in, H1),
        nn.Linear(H1, H2),
        nn.Linear(H2, D_out),
        
        
    ).to(device)

    #loss_fn = nn.CrossEntropyLoss(size_average=True, reduction='mean')
    loss_fn = nn.MSELoss(size_average=True)

    optimizer = torch.optim.SGD(
        model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    for i in range(100):
        for t, (x, y) in enumerate(train_loader):
            x, y = Variable(x), Variable(y)
            y_pred = model(x)
            #print(y_pred.shape)
            #print(y.shape)
            loss = loss_fn(y_pred, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        if i % 1 == 0:
            print("Epoch", i, " Loss:", loss.item())


    y_pred = model(x_nonbatch)
    y_pred = np.array(y_pred.data).reshape(-1)
    y = np.array(y_nonbatch.data).reshape(-1)
    y = (y + 1) * y0
    y_pred=(y_pred+1)*y0

    fig = plt.figure()
    plt.title('Training Model')
    plt.plot(y_pred, c='cornflowerblue', label='Prediction')
    plt.plot(y, c='darkorange', label='Real Price')
    plt.legend(loc=2)
    fig.savefig('static/images/svm_model.png')

    x_test = []
    x_test_price = []

    for i in range(len(price)-training_length,len(price)):
        tmp = []
        tmp.append(price[i])
        tmp.append(volume[i])
        tmp_ma = 0.0
        for j in range(i - training_length, i):
            tmp_ma += price[j]
        tmp_ma = tmp_ma / training_length
        tmp.append(tmp_ma)
        x_test.append(tmp)  # trainning data
        

    x_test = np.array(x_test)
    x_test0 = x_test[0]
    x_test = (x_test / x_test0)-1
    x_test = torch.from_numpy(x_test).float()
    pred = model(x_test)
    pred = np.array(pred.data).reshape(-1)
    pred=(pred+1)*x_test0[0]

    for i in range(len(price) - training_length * 5, len(price)):
        x_test_price.append(price[i])
        
    x_test_price.append(pred[0])

    fig1 = plt.figure()
    plt.title('Prediction')
    
    plt.plot(range(len(x_test_price) - 1, len(x_test_price) + len(pred) - 1), pred, c='cornflowerblue', label='prediction')
    plt.plot(range(len(x_test_price)), x_test_price, c='darkorange', label='Real Price')
    plt.legend(loc=2)
    fig1.savefig('static/images/svm_pred.png')
    return pred


#pred=svm_model('goog',50)