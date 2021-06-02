from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import deepxde as dde
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
import numpy as np

def save_heatmap_data(model, geom):
    x = np.linspace(0, 2, 200)
    y = np.linspace(0, 2, 200)
    y_m, x_m = np.meshgrid(y, x)
    z = np.zeros((200, 200)) #(x,y)
    for xi, i in enumerate(x):
        for yi, j in enumerate(y):
            X = np.array([i, j])
            X = np.reshape(X, [1,2])
            if geom.inside([i,j]):
                z[xi,yi] = model.predict(X)
            else:
                z[xi,yi] = 0
    
    z_min, z_max = -np.abs(z).max(), np.abs(z).max()

    fig, ax = plt.subplots()
    c = ax.pcolormesh(x_m, y_m, z, cmap='RdBu', vmin=z_min, vmax=z_max)
    ax.set_title('2D')
    ax.axis([x_m.min(), x_m.max(), y_m.min(), y_m.max()])
    fig.colorbar(c, ax=ax)

    # shape = 
    # ax.add_collection()

    plt.show()


def main():
    def pde(x, y):
        dy_xx = dde.grad.hessian(y, x, i=0, j=0)
        dy_yy = dde.grad.hessian(y, x, i=1, j=1)
        return -dy_xx - dy_yy - 1

    def boundary(_, on_boundary):
        return on_boundary

    geom_r = dde.geometry.Rectangle([0,0],[1,1])
    geom_d = dde.geometry.Disk([1,1],1)
    geom = geom_r.union(geom_d)
    bc = dde.DirichletBC(geom, lambda x: 0, boundary)

    data = dde.data.PDE(geom, pde, bc, num_domain=1200, num_boundary=120, num_test=1500)
    net = dde.maps.FNN([2] + [50] * 4 + [1], "tanh", "Glorot uniform")
    model = dde.Model(data, net)

    model.compile("adam", lr=0.001)
    model.train(epochs=1000)
    model.compile("L-BFGS-B")
    losshistory, train_state = model.train()
    save_heatmap_data(model, geom)
    dde.saveplot(losshistory, train_state, issave=True, isplot=True)



if __name__ == "__main__":
    main()
