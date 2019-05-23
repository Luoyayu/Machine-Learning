# 深入SVM

$\displaystyle \mathscr{L}(w,b,a)=\frac{1}{2}||\mathbf{w}||^2-$ $\displaystyle \sum_{i=1}^{m}\alpha^{(i)}(y^{(i)}(w^Tx^{(i)}+b)-1)$  

令$\displaystyle \theta(m)=\underset{\alpha^{(i)}\geq0}{\mathrm{max}}$ $\mathscr{L}(w,b,a)$ 

目标函数: $\displaystyle \mathrm{max}\frac{1}{||w||}$ $\ s.t.\ y^{(i)}(w^Tx^{(i)}+b)\geq1$

等价于:    $\mathrm{min}\frac{1}{2}||w||^2$ $\ s.t.\ y^{(i)}(w^Tx^{(i)}+b)\geq1$ 

目标: $\underset{w,b}{\mathrm{min}\ \theta(w)}$ $=\underset{w,b}{\mathrm{min}}\underset{\alpha^{(i)}\geq0}{\mathrm{max}}\mathscr{L}(w,b,a)=p^\ast$ 

此时目标的dual problem为 $\displaystyle \underset{\alpha^{(i)}\geq0}{\mathrm{max}} \underset{w,b}{\mathrm{min}} \mathscr{L}(w,b,a)=d^\ast$ 

$d^\ast\leq p^\ast$ 当在**KKT**条件下取等号, 故原问题的不等约束为在$\alpha^{(i)}$下求极大, 再在$w,b$下求极小

对偶问题为在$w,b$ 下求极小, 再在$\alpha^{(i)} $下求极大

第一步求极小 由凸函数性质可知, 极值点一定在导数为0的地方, 

对$\displaystyle \mathscr{L}(w,b,a)=\frac{1}{2}||\mathbf{w}||^2-$ $\displaystyle \sum_{i=1}^{m}\alpha^{(i)}(y^{(i)}(w^Tx^{(i)}+b)-1)$  在$w,b$处求偏导得

$\begin{align*} \bigtriangledown _\mathbf{w}\mathscr{L}&=\mathbf{w}-\sum_{i=1}^m\alpha^{(i)}t^{(i)}x^{(i)}=0 \\ \frac{\partial }{\partial b}\mathscr{L}&=-\sum_{i=1}^m\alpha^{(i)}t^{(i)}=0 \end{align*}$





 