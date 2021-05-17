"""
方程的转译

由前端传回text文本，翻译并转化成tensorflow/python的公式

+ - * / ** 

sin(x)
"""
import ast
import types

from astunparse import unparse

import deepxde as dde
from deepxde.backend import tf
import numpy as np

class Translator:
    builtins = ["sin", "cos", "pi", "exp", "norm"]
    mapping = {"sin":"tf", "cos":"tf", "pi":"np", "exp":"np","norm":"np.linalg.norm(x, axis=1, keepdims=True)"}

# class DirichletTranslator(Translator):
#     pass

# class NeumannTranslator(Translator):
#     pass

class PoissonTranslator(Translator):
    """
    syms_text: "x, y, z", in string splitted by ','
    f_text: expression

    + - * / **

    builtins:
    sin, cos,
    pi
    todo: e, log, integral,derivate

    u(x,y) = "sin(x**2) - 1/ pi * 3**(y)"

    sin -> tf.sin
    pi -> np.pi
    """

    def __init__(self, syms_text, f_text):
        self.syms = [sym.strip() for sym in syms_text.split(',')]
        self.f_ast = ast.parse(f_text)

        self.dims = len(self.syms)
        super().__init__()

    def translate(self):
        """
        walk through the ast tree, replace the ast tree leaf
        """
        new_ast = ast.fix_missing_locations(ReplaceBuiltin(self.mapping, self.builtins, self.syms).visit(self.f_ast))
        print(ast.dump(new_ast))
        expr_code = unparse(new_ast)
        print(expr_code)

        if self.dims == 1:
            code = """
def create_1d_poisson_function(X, u):
    du_xx = dde.grad.hessian(u, X)
    return du_xx - {}
            """.format(expr_code.strip())
            exec(code, globals())
            self.poisson = create_1d_poisson_function

        elif self.dims == 2:
            code = """
def create_2d_poisson_function(X, u):
    du_xx = dde.grad.hessian(u, X, i=0, j=0)
    du_yy = dde.grad.hessian(u, X, i=1, j=1)
    return du_xx + du_yy - {}
            """.format(expr_code.strip())
            exec(code, globals())
            self.poisson = create_2d_poisson_function
        else:
            print("Not support yet")
            code = """ """


class ReplaceBuiltin(ast.NodeTransformer):
    def __init__(self, mapping, builtins, syms):
        self.mapping = mapping
        self.builtins = builtins
        self.syms = syms
        super().__init__()

    def visit_Name(self, node):
        if node.id in self.builtins:
            return ast.Attribute(
                value=ast.Name(id=self.mapping[node.id], ctx=ast.Load()),
                attr=node.id,
                ctx=node.ctx
            )
        elif node.id in self.syms:
            return node
        else:
            print(node.id)
            print("unknow Vars!!!!!!!!!!")
            return None


if __name__=="__main__":
    p = PoissonTranslator("x, y","sin(x**2) - 1/ pi * 3**(y)")
    p.translate()