预计在 TF2.0 版本正式发布的TF动态图计算

from tf.contrib import eager as tfe # Eager模式
开启响应式(imperative)计算
例如:
```python
tf.enable_eager_execution()
x = [[2.]]
print(tf.matmul(x, x))
```

输出 `
<tf.Tensor: id=3, shape=(1, 1), dtype=float32, numpy=array([[4.]], dtype=float32)> `
相当于debug模式，免去了开启会话

-----------------------------------

```python
import tensorflow as tf
import tensorflow_probability as tfp

tf.enable_eager_execution() 
rv0 = tfp.distributions.Bernoulli(probs=0.5, dtype=tf.int32)
rv0.sample(20)
```

输出 `
<tf.Tensor: id=29, shape=(20,), dtype=int32, numpy=array([1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1], dtype=int32)> `

---------------------
# tf.pad

```python
tf.pad(
    tensor,
    paddings, # (tensor shape [n, 2]) -> like tf.constant([[2, 2], [2, 2]])
    # 向四方向扩展
    mode = 'CONSTANT' or 'REFLECT' or 'SYMMETRIC',
    name = None,
    constant_values = 0
)
```

---------------------

# tf.gather
```python
tf.gather(
    params,
    indices,
    validate_indices=None,
    name=None,
    axis=0
)
```

根据indices从params中收集切片

```python
tf.gather(
    params = tf.constant([0, 1, 2, 3, 4, 5]), 
    indices = tf.constant([2, 0, 2, 5])
)
```
输出
`<tf.Tensor: id=400, shape=(4,), dtype=int32, numpy=array([2, 0, 2, 5], dtype=int32)>
`


