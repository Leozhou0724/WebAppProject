import numpy as np
import matplotlib.pyplot as plt
import csv

def bayes_model(company, training_length):
    price = []
    with open('dataset/{}.csv'.format(company)) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            price.append(float(row[4]))
    
    y_train = []
    for i in range(len(price) - training_length,len(price) ):
        y_train.append(price[i])
    y_train = np.array(y_train)
    x_train = np.linspace(0, 0.9, 0.9 * training_length + training_length/10)
    #print(x_train)
    x_test = np.linspace(0, 1, training_length * 10 + 1)
    X_train=np.empty([training_length,training_length])
    for i in range(training_length):
        for j in range(training_length):   
            X_train[i][j]=x_train[i]**j
    X_test=np.empty([training_length*10+1,training_length])
    for i in range(training_length*10+1):
        for j in range(training_length):   
            X_test[i][j] = x_test[i]**j
    alpha=0.01
    beta=2

    #Inverse of S
    S_inv=alpha*np.eye(training_length)+beta*np.matmul(X_train.T,X_train)
    S=np.linalg.inv(S_inv)
    mean=beta*np.matmul(S,np.matmul(X_train.T,y_train))
    #result
    y=np.matmul(X_test,mean)
    #Varience
    y_var=1/beta+np.sum(np.matmul(X_test,S)*X_test,axis=1)
    y_std=np.sqrt(y_var)

    #print("Training data: ",y_train)
    print(len(y))
    pred_start=int(0.9 * training_length * 10)
    pred = y[pred_start:len(y)]
    print(pred)


    fig=plt.figure(figsize=(12,8))
    plt.scatter(x_train,y_train,edgecolor="b", s=50, label="Training data")
    plt.plot(x_test,y,c="r", label="Prediction curve")
    plt.fill_between(x_test, y - y_std, y + y_std, color="pink", label="Standard Deviation", alpha=0.5)
    plt.legend(loc=2)
    fig.savefig("static\images\Bayes.png")
    return pred
#bayes_model('aaba',30)
    
    