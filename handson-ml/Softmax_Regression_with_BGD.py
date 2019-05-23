# ============================================================ #
# implement Softmax Regression based BGD with Earning Stopping #
# TODO: [X] data clean                                         #
# TODO: [X] One hot encoding                                   #
# TODO: [X] Softmax function                                   #
# TODO: [X] Ridge Regression                                   #
# TODO: [X] Training models                                    #
# TODO: [X] Validating models                                  #
# TODO: [X] Earning Stopping                                   #
# ============================================================ #

from sklearn.datasets import load_iris
import numpy as np

np.random.seed(42)
raw_data = load_iris()
# print(raw_data.keys())
X = raw_data['data'][:, (2, 3)]  # petal length and width
y = raw_data['target']

# add x_0=1
X = np.c_[np.ones([len(X), 1]), X]  # ones->shape (len(X), 1)

# ============================================================
# split train set and test set
test_ratio, validation_ratio, tot_size = 0.2, 0.2, len(X)
test_size, validation_size = int(tot_size * test_ratio), int(tot_size * validation_ratio)
train_size = tot_size - test_size - validation_size

random_idx = np.random.permutation(tot_size)
X_train = X[random_idx[:train_size]]
y_train = y[random_idx[:train_size]]

X_valid = X[random_idx[train_size:-test_size]]
y_valid = y[random_idx[train_size:-test_size]]

X_test = X[random_idx[-test_size:]]
y_test = y[random_idx[-test_size:]]


# ============================================================
# y = {0, 1, 2}
# we have three class, so let do onehot for them
# if n_class=2 it's y look like [0, 1, 0]

def de_one_hot(Y):
    n_classes = Y.max() + 1
    m = len(Y)
    y_one_hot = np.zeros((m, n_classes))
    y_one_hot[np.arange(m), Y] = 1
    return y_one_hot


y_train = de_one_hot(y_train)
y_valid = de_one_hot(y_valid)
y_test = de_one_hot(y_test)

# ============================================================
# Softmax function

def softmax(sx):
    """
    :param sx: All classes softmax score matrix
    :return p: ever class probability
    """
    exps = np.exp(sx)
    sum_exps = np.sum(exps, axis=1, keepdims=True)
    return exps / sum_exps


# ============================================================
# define number of in/output

n_inputs = X_train.shape[1]
n_outputs = len(np.unique(y))
# Theta :(3 * 3) 3 class, 3 features

# ============================================================
# training and validating model

eta = 0.01
n_iterations = 5001
m = len(X_train)
epsilon = 1e-7  # avoid getting nan value when cal log(pk)

Thetas = np.random.randn(n_inputs, n_outputs)

for iteration in range(n_iterations):
    sk = X_train.dot(Thetas)
    pk = softmax(sk)
    log_loss = -np.mean(np.sum(y_train * np.log(pk + epsilon), axis=1))
    error = pk - y_train
    if not iteration % 500:
        print(iteration, log_loss)
    gradients = 1 / m * X_train.T.dot(error)
    Thetas = Thetas - eta * gradients

vsk = X_valid.dot(Thetas)  # validating set sk
vpk = softmax(vsk)  # softmax sk then output pk
vy_predict = de_one_hot(np.argmax(vpk, axis=1))  # 输出的是(1, -1) 转换成(-1, 3)
print(np.mean(vy_predict == y_valid))  # compare with validation set
# 0.9555555555555556

# ============================================================
# try l2 penalty to regularize and validating model

Thetas = np.random.randn(n_inputs, n_outputs)
alpha = 0.1  # hyperparameter control l2 penalty
for iteration in range(n_iterations):
    sk = X_train.dot(Thetas)
    pk = softmax(sk)
    xcross_loss = -np.mean(np.sum(y_train * np.log(pk + epsilon), axis=1))  # cal Cross entropy loss
    l2_loss = xcross_loss + alpha * 0.5 * np.sum(np.square(Thetas[1:]))  # cal l2 loss
    error = pk - y_train
    if not iteration % 500:
        print(iteration, l2_loss)
    gradients = 1 / m * X_train.T.dot(error) + np.r_[np.zeros([1, n_outputs]), alpha * Thetas[1:]]
    Thetas -= gradients * eta

vsk = X_valid.dot(Thetas)  # validating set sk
vpk = softmax(vsk)  # softmax sk then output pk
vy_predict = de_one_hot(np.argmax(vpk, axis=1))  # 输出的是(1, -1)转换成(-1, 3)
print(np.mean(vy_predict == y_valid))  # compare with validation set
# 0.9777777777777777

# ============================================================
# Earning Stopping

best_loss = np.infty
Thetas = np.random.randn(n_inputs, n_outputs)

for iteration in range(n_iterations):
    sk = X_train.dot(Thetas)
    pk = softmax(sk)
    xcross_loss = -np.mean(np.sum(y_train * np.log(pk + epsilon), axis=1))  # cal Cross entropy loss
    l2_loss = xcross_loss + alpha * 0.5 * np.sum(np.square(Thetas[1:]))  # cal l2 loss
    error = pk - y_train
    gradients = 1 / m * X_train.T.dot(error) + np.r_[np.zeros([1, n_outputs]), alpha * Thetas[1:]]
    Thetas -= gradients * eta

    if not iteration % 500:
        print(iteration, l2_loss)
    if l2_loss < best_loss:
        best_loss = l2_loss
    else:
        print(iteration - 1, best_loss)
        print('Earning Stopping!')
        break

vsk = X_valid.dot(Thetas)  # validating set sk
vpk = softmax(vsk)  # softmax sk then output pk
vy_predict = de_one_hot(np.argmax(vpk, axis=1))  # 输出的是(1, -1)转换成(-1, 3)
print(np.mean(vy_predict == y_valid))  # compare with validation set
# 0.9555555555555556

# ============================================================
# Test in test set

tsk = X_test.dot(Thetas)
tpk = softmax(tsk)
ty_predict = de_one_hot(np.argmax(tpk, axis=1))
print(np.mean(ty_predict == y_test))
# 0.9777777777777777

# ============================================================
# END