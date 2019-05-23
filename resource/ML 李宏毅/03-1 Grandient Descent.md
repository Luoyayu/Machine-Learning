$\theta^*=\underset{\lambda}{arg \min} \ L(\theta)$ 	L: loss function  ,$\theta$: parameters

$\displaystyle \triangledown  L(\theta)= \begin{bmatrix}  \frac{\partial L(\theta_1)}{ \partial \theta_1} \\ \frac{\partial L(\theta_2)}{ \partial \theta_2} \\ ...\end{bmatrix}_{gradient}$

$\theta^n_i=\theta^{n-1}_i - \eta \triangledown L(\theta^{n-1}_i)$ 

Gradient : Loss 的等高綫的法綫方向

## Tips

1.  ### Tuning learning rate

    ​	No. of parameters updates to Loss change can be visualized

    #### Adaptive Learning Rates

    *   at the beginning far from the destination we use large learning rate
    *   several epochs close to the destination so we reduce the learning rate
    *   **Giveing different parameters different learning rate**

    #### Adagrad

    *   Divide the lr of each para by the RMS(均方根) of its previous derivatives

        $\displaystyle para_i^{t+1}\leftarrow para_i^t-\frac{\eta^t}{\sigma^t}g^t$, 		$\displaystyle g^t=\frac{\partial L(\theta^t)}{\partial \theta}$	 

        $\sigma^t$: $RMS$ of the previous derivatives of  $para_i$ 

        $\displaystyle \sigma^t=\sqrt{\frac{1}{t+1}\sum_{i=0}^t(g^i)^2}$ 

        $\displaystyle para_i^{t+1}\leftarrow para_i^t-\frac{\eta^tg^t}{\sqrt{\frac{1}{t+1}\displaystyle  \sum_{i=0}^t(g^i)^2}}$ 

        Let $\displaystyle \eta^t=\frac{\eta}{t+1}$ , we can simplify to: 

        $\displaystyle para_i^{t+1}\leftarrow para_i^t-\frac{\eta}{\sqrt{\displaystyle  \sum_{i=0}^t(g^i)^2}}g^t$ 

        Adagrad造成反差的效果，跨參數 best step sis : 一次微分/二次微分

        **$\sigma^t \approx $ *second derivative*** 

2.  ### Stochastic(隨機) Gradient Descent 

    Pick an example $x^n$ ,calculate loss function $L^n$ with $x^n$ then update that parameter

3.  ### Feature Scaling

    E.g. $y = b + w_1x_1 + w_2x_2$

    to make different features have the same scaling

    ![FeatureScaling](http://hexo-1253425814.cossh.myqcloud.com/FeatureScaling.png)

    diferent parameter effects differently on $y$

    ![對比](http://hexo-1253425814.cossh.myqcloud.com/%E5%B0%8D%E6%AF%94.png)

    *feature scaling* better to update parameters

    **One Ways :** for each dimension $i$: calculate mean $m_i$ and standard deviation $\sigma_i$

    E.g.  $\displaystyle x_i^r \leftarrow \frac{x_i^r-m_i}{\sigma_i}$ 

## Theory

#### 	Why gradient descent works?

##### 		Taylor Series 泰勒展开拟合原函数

​			$\displaystyle h(x)=\sum_{k=0}^\infty\frac{h^{(k)(x_0)}}{k!}(x-x_0)^k$ 

​				 $=h(x_0)+h'(x_0)(x-x_0)+\frac{h''(x_0)}{2!}(x-x_0)^2+ ···$

​			where $x$ is close to $x_0$ $h(x)\approx h(x_0)+h'(x_0)(x-x_0)$ 

##### 		Multivariable Taylor Series

###### 			Back to the Formal Dervation

​			$\displaystyle h(x)\approx h(x_0,y_0)+\frac{\partial h(x_0,y_0)}{\partial x}(x-x_0)+\frac{\partial h(x_0,y_0)}{\partial y}(y-y_0)$ 

​			$\displaystyle \left\{\begin{align*}L(\theta)&\approx s+u(\theta_1-a)+v(\theta_2-b) \\ s&=L(a,b) \\ u&=\frac{\partial L(a,b)}{\partial \theta_1} \\ v &= \frac{\partial L(a,b)}{\partial \theta_2} \end{align*}\right.$

​			Find $\theta_1$ and $\theta_2$ *minimizing* $L(\theta)$ 

​			$L(\theta)\approx u(\theta_1-a)+v(\theta_2-b)$ 

​			if in small Red Cirle: $(\theta_1-a)^2+(\theta_2-b)\leq d^2$ 

​			Let $\Delta \theta_1,\Delta \theta_2 = (\theta_1-a), (\theta_2-b)$ 

​			$L(\theta)=s+(u,v) \cdot (\Delta \theta_1,\Delta \theta_2) $

​			So to minimize L(\theta) we can choose $(u,v)$相反方向的长度为圆半径的向量

​			$\eta$ is lr also the factor make (u,v) to 反向小圆半径

​			$\begin{bmatrix} \Delta \theta_1 \\ \Delta \theta_2 \end{bmatrix}=-\eta \begin{bmatrix} u \\ v\end{bmatrix}$ 

​			$\begin{bmatrix} \theta_1 \\ \theta_2 \end{bmatrix}=\begin{bmatrix} a \\ b \end{bmatrix}-\eta \begin{bmatrix} u \\ v\end{bmatrix}$ 

​			This is gradient descent.

​			Not satisfied if the red circle is not small enough.

## More Limitation of Gradient descent

​		we will stuck at local minima or saddle point.

​		if we define eps $\approx 1e^{-6}$, we will stuck very slow at the plateau.s
