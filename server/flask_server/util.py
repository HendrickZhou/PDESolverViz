import deepxde as dde
from deepxde.callbacks import Callback
import numpy as np

class TrainLossCallback(Callback):
    """
    call back of training loss

    self.period: saving interval on epoch
    handler is the outside callback that get executed on period
    """
    def __init__(self, handler, period = 5):
        super(TrainLossCallback, self).__init__()
        self.period = period
        self.handler = handler
        self.epoch_time = 0
        self.cur_epoch = 0

    def on_epoch_end(self):
        self.cur_epoch += 1
        self.epoch_time += 1
        if self.epoch_time < self.period:
            return
        self.epoch_time = 0
        train_loss = np.sum(self.model.train_state.loss_train)
        self.handler([str(self.cur_epoch),str(train_loss)])

    

