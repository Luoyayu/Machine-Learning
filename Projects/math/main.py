from matplotlib import pylab as plt
import numpy as np

x = np.arange(-1, 1, 0.001)
f_x = x * x * x + x * x
f_x_1 = 3 * x * x + 2 * x
f_x_2 = 6 * x + 2

plt.plot(x, f_x, label="fx")
plt.plot(x, f_x_1, label="fx^(1)")
plt.plot(x, f_x_2, label="fx^(2)")
plt.plot([0 for _ in np.arange(-10, 15, 0.001)], np.arange(-10, 15, 0.001), 'r')
plt.plot(x, [0 for _ in x], 'r')
plt.ylim((-1, 1))
plt.legend()
plt.show()
