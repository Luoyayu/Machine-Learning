import numpy as np
import matplotlib.pylab as plt

m = 20
st = -100
ed = 100
# np.random.seed()
X = np.random.randint(st, ed, m)
y = np.random.randint(st, ed, m)
print('横坐标:', X, '\n纵坐标:', y,)
plt.subplot(121)
plt.scatter(X, y, c='grey')

K = int(input('输入聚类个数: '))
shuffled_index = np.random.permutation(m)
muX, muy, C, d = [], [], np.zeros((K, m)), np.zeros((m, K))
# 初始化向量，簇划分，簇内距离
mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
for k in range(K):
    nx, ny = X[shuffled_index[k]], y[shuffled_index[k]]
    muX.append(nx)
    muy.append(ny)
    plt.plot(nx, ny, mark[k])
    print('{}th: ({}, {})'.format(k+1, nx, ny))
plt.show()
__ = K * 239  # 迭代次数


def norm2(x1, y1, x2, y2):
    return (x1-x2)**2+(y1-y2)**2


for _ in range(__):
    d = np.zeros((m, K))
    C = [[] for i in range(K)]
    for i in range(m):
        for k in range(K):
            d[i][k] = norm2(X[i], y[i], muX[k], muy[k])  # 第 i 个点到簇中心 k 的距离
    c = np.argmin(d, axis=1)
    for i in range(m):
        C[c[i]].append(i)
    for idx, Cidx in enumerate(C):
        muX[idx], muy[idx] = np.sum(X[C[idx]])/len(Cidx), np.sum(y[C[idx]])/len(Cidx)

plt.subplot(122)
for k in range(K):
    plt.scatter(X[C[k]], y[C[k]], mark[k])
plt.show()