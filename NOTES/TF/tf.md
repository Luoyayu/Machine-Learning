# TF

tf.constant
tf.pad
tf.gather

## TF cal

tf.cumsum
tf.matmul

## TF config

tf.enable_eager_execution()

# TFP

import tensorflow_probility as tfp

## TFD

import tfp.distributions as tfd

### Bernoulli 伯努利分布

tfd.Bernoulli

```python
__init__(
    logits=None, # sigmoid(logits)
    probs=None, # logits probs 二选一
    dtype=tf.int32,
    validate_args=False,
    allow_nan_stats=True,
    name='Bernoulli'
)
```
tfd.Bernoulli(
    # probs=tf.constant([0.2, 0.8])
    # probs=[0.2, 0.8]
).sample(20) 

#### Methods






