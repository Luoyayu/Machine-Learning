# The Learning Problem

![屏幕快照 2018-05-07 下午10.41.55](/Users/hu-osx/Documents/Machine-Learning/ML 基石/屏幕快照 2018-05-07 下午10.41.55.png)

目标习得$g\ in\ \mathcal{H}$ 

特征 $\mathbf{x}=(x_1, x_2,x_3,…,x_d)$ 

感知机模型(perceptron) 

$\begin{align*} \displaystyle {\color{red} h}(\mathbf{x})&=\mathrm{sign}((\sum_{i=1}^d\mathbf{\color{red}{w_i}}x_i)-\mathrm{{\color{red} {threshold}}}) \\ &=\mathrm{sign}((\sum_{i=1}^d\mathbf{\color{red}{w_i}}x_i)+\color{blue}{\underset{\mathbf{w}_0}{\underbrace{(\mathrm{-threshold})}} \cdot \underset{\mathbf{x}_0}{\underbrace{(+1)}}) } \\ &=\mathrm{sign}((\sum_{i=0}^d\mathbf{\color{red}{w_i}}x_i)) \\ &=\mathrm{sign}(\mathrm{\color{red}{w^T}}\mathbf{x})\end{align*}$ 



# LEARNING TO ANSWER YES\NO

- 