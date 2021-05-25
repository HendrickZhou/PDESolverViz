"""
方程的转译

由前端传回text文本，翻译并转化成tensorflow/python的公式

+ - * / ** 

sin(x)
"""
import ast
import types
import abc

from astunparse import unparse

import deepxde as dde
from deepxde.backend import tf
import numpy as np

class Translator:
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
    builtins = ["sin", "cos", "pi", "exp", "norm"]
    mapping = {"sin":"tf", "cos":"tf", "pi":"np", "exp":"np","norm":"np.linalg.norm(x, axis=1, keepdims=True)"}
    
    def __init__(self, syms_text, f_text):
        self.syms = [sym.strip() for sym in syms_text.split(',')]
        self.f_ast = ast.parse(f_text)

        self.dims = len(self.syms)
        self.translate()
        self.gen_func()

    def translate(self):
        """
        walk through the ast tree, replace the ast tree leaf
        """
        new_ast = ast.fix_missing_locations(ReplaceBuiltin(self.mapping, self.builtins, self.syms).visit(self.f_ast))
        # print(ast.dump(new_ast))
        self.expr_code = unparse(new_ast)
        # print(self.expr_code)
    
    @abc.abstractmethod
    def gen_func(self):
        raise NotImplementedError("{}.gen_func not implemented".format(type(self).__name__))
    
    @abc.abstractmethod
    def get(self):
        raise NotImplementedError("{}.get not implemented".format(type(self).__name__))

class BCTranslator(Translator):
    """
    由于BC的条件在deepxde都只用规定右侧表达式，所以是一样的
    """
    def __init__(self, syms_text, f_text):
        super().__init__(syms_text, f_text)
    
    def gen_func(self):
        if self.dims == 1:
            code = """
def bc_func(X):
    {} = X[:,0:1]
    return {}
            """.format(self.syms[0], self.expr_code.strip())
            print(code)
            exec(code,globals())
            self.bc = bc_func
        elif self.dims == 2:
            code = """
def bc_func(X):
    {}, {} = X[:,0:1], X[:,1:2]
    return {}
            """.format(self.syms[0], self.syms[1], self.expr_code.strip())
            print(code)
            exec(code,globals())
            self.bc = bc_func
        elif self.dims == 3:
            code = """
def bc_func(X):
    {}, {}, {} = X[:,0:1], X[:,1:2], X[:,2:3]
    return {}
            """.format(self.syms[0], self.syms[1], self.syms[2], self.expr_code.strip())
            print(code)
            exec(code,globals())
            self.bc = bc_func

    def get(self):
        return self.bc

# class NeumannTranslator(Translator):
#     pass

class PoissonTranslator(Translator):

    def __init__(self, syms_text, f_text):
        super().__init__(syms_text, f_text)

    def gen_func(self):
        """
        walk through the ast tree, replace the ast tree leaf
        """
        # new_ast = ast.fix_missing_locations(ReplaceBuiltin(self.mapping, self.builtins, self.syms).visit(self.f_ast))
        # print(ast.dump(new_ast))
        # expr_code = unparse(new_ast)
        # print(expr_code)
        if self.dims == 1:
            code = """
def create_1d_poisson_function(X, u):
    du_xx = dde.grad.hessian(u, X)
    {} = X[:,0:1]
    return du_xx - {}
            """.format(self.syms[0], self.expr_code.strip())
            print(code)
            exec(code, globals())
            self.poisson = create_1d_poisson_function

        elif self.dims == 2:
            code = """
def create_2d_poisson_function(X, u):
    du_xx = dde.grad.hessian(u, X, i=0, j=0)
    du_yy = dde.grad.hessian(u, X, i=1, j=1)
    {}, {} = X[:, 0:1], X[:,1:2]
    return du_xx + du_yy - {}
            """.format(self.syms[0], self.syms[1], self.expr_code.strip())
            print(code)
            exec(code, globals())
            self.poisson = create_2d_poisson_function
        else:
            print("Not support yet")
            code = """ """

    def get(self):
        return self.poisson


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
    p2 = BCTranslator("x, y","sin(x**2) - 1/ pi * 3**(y)")
    f = p.get()