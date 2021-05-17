"""
读取前端传入的网络配置信息，包括结构，超参数，初始化方法
默认使用FNN(Feed-forward Neural Network)
"""
import deepxde as dde

class NetConfig:
    """
    AUTO mode:

    layers:         [5, 2, 1] list or np.array
    activation:     "elu"
                    "relu": tf.nn.relu,
                    "selu": tf.nn.selu,
                    "sigmoid": tf.nn.sigmoid,
                    "sin": tf.sin,
                    "swish": swish,
                    "tanh": tf.nn.tanh
    initializer:    "zeros": tf.zeros_initializer(),
                    (stacked)"He normal": tf.variance_scaling_initializer(scale=2.0),
                    (stacked)"He uniform": tf.variance_scaling_initializer(scale=2.0, distribution="uniform"),
                    (stacked)"LeCun normal": tf.variance_scaling_initializer(),
                    (stacked)"LeCun uniform": tf.variance_scaling_initializer(distribution="uniform"),
                    "Glorot normal": tf.glorot_normal_initializer(),
                    "Glorot uniform": tf.glorot_uniform_initializer(),
                    "Orthogonal": tf.orthogonal_initializer(),
    regularizer:    "l1"
                    "l2"
                    "l1+l2"
                    None
    batch_norm:     "before"
                    "after"
                    None
    dropout:        float in (0,1)
                    0
    """
    def __init__(self, json_f):
        self.parse_json(json_f)
    
    def parse_json(self, json_f):
        pass
        

    def net_arch_config(self, layers, activation, initializer, regularizer, batch_norm, dropout):
        self.net = dde.maps.FNN(layers, 
                        activation, 
                        kernel_initializer = initializer, 
                        regularization=regularizer,
                        dropout_rate=dropout,
                        batch_normalization=batch_norm,
                        kernel_constraint=None,
                        use_bias=True)

    def compile_config(self, optimizer, lr, loss, metrics):
        pass

    def dynamic_config(self, epochs):
        pass

