# /usr/bin/python3.8
# transpiler for Geometry Script

import types
import ast
import json
from inspect import isfunction, isclass, getmembers
import importlib.util
# from primitive import Primitive
import primitive

func_kws = getmembers(primitive, isfunction)
func_kws = [_[0] for _ in func_kws]
prim_kws = getmembers(primitive, isclass)
prim_kws = [_[0] for _ in prim_kws if _[0][0] != '_']
keywords = {
    "config" : ["MODE", "1D", "2D", "3D"],
    "splitter" : "%%",
    "delimiter" : [' ', ':', '\n', '\t'],
    "export" : ["build"],
    "primitive" : prim_kws,
    "ops": func_kws,
}
DEBUG = False
local = False

class Tree:
    def __init__(self, id):
        self.children = []
        self.id = id
        self.content = None

    def _to_dict(self):
        result = {"id": self.id, "content": self.content}
        children_list = []
        for child in self.children:
            children_list.append(child._to_dict())
        result["children"] = children_list
        return result

class Traversal(ast.NodeVisitor):
    def __init__(self):
        self.know_nodes = dict()
        super().__init__()

    def visit_Assign(self, node):
        var = node.targets[0].id
        if var in self.know_nodes: # change name
            print("re-assign forbid!")
            return
        if isinstance(node.value, ast.Call): # init expr
            init_node = Tree(var)
            # init_node.content = node.value
            # get init parameters
            params_list = []
            for arg in node.value.args:
                if isinstance(arg, ast.Num):
                    params_list.append(arg.n)
                elif isinstance(arg, ast.List):
                    arg_list = [elt.n for elt in arg.elts]
                    params_list.append(arg_list)
            init_node.content = {'params': params_list, 'type': node.value.func.id}
            self.know_nodes[var] = init_node
        elif isinstance(node.value, ast.Name): # copy forbidden
            print('copy forbidden!')
            return
        elif isinstance(node.value, ast.BinOp): # build tree
            new_root = Tree(var)
            if self.recur_binop(node.value, new_root) is False:
                print('undefined operator!')
                return 
            self.know_nodes[var] = new_root

        # TODO: forbid 3 elements operations

    def recur_binop(self, entry, root):
        if not isinstance(entry, ast.BinOp):
            return True
        op = entry.op.__class__.__name__
        left = entry.left.id
        right = entry.right.id

        n_op = Tree(op)
        root.children.append(n_op)
        if left not in self.know_nodes:
            return False
        n_l = self.know_nodes[left]
        n_op.children.append(n_l)
        if right not in self.know_nodes:
            return False

        n_r = self.know_nodes[right]
        n_op.children.append(n_r)

        self.recur_binop(entry.left, n_l)
        self.recur_binop(entry.right, n_r)

class ReplaceCallOp(ast.NodeTransformer):
    def __init__(self):
        self.op_map = {
            "union":ast.BitAnd(),
            "diff": ast.Sub(),
            "inter": ast.Add(),
        }
        super().__init__()

    def visit_Call(self, node):
        if node.func.id in keywords["ops"]:
            return ast.BinOp(
                left=ast.Name(id=node.args[0].id, ctx=ast.Load()),
                right=ast.Name(id=node.args[1].id, ctx=ast.Load()),
                op=self.op_map[node.func.id],
            )
        else:
            return node

# Transpiler
class Transpiler:
    ''' 
    get the context, and run the transpiling process:
        include: ast pruning(optimization), deepxde code build, geometry json generation
    '''
    script_globals = ["primitive"]
    mode_flag = {"1D":0, "2D":1, "3D":2}

    def __init__(self, code_source):
        if local:
            self.context = _Context(code_source, 'f')
        else:
            self.context = _Context(code_source) # code source is string by default
        self.code_def = self.context.code_def
        self.code_export = self.context.code_export
        self.code_config = self.context.code_config

    def run(self):
        self._pruning()
        self._compile_and_run()
        json_stream = self.geo_proto(self.result_tree)
        json_stream.update({"mode":self.mode})
        return self.code_result_dict, json_stream, self.final_globals["config_mode"]
        
    @staticmethod
    def import_mod(name):
        spec = importlib.util.find_spec(name)
        if(spec):
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
        else:
            print("can't find the language libary")
            return None

    @staticmethod
    def geo_proto(tree):
        if DEBUG:
            print(json.dumps(tree._to_dict(), indent=2))
            with open("./test.json", 'w') as f:
                json.dump(tree._to_dict(), f, indent=2)
        return tree._to_dict()

    def _pruning(self):
        export_ast = ast.parse(self.code_export)
        def check_build_ast():
            if export_ast.body[0].value.func.id == keywords["export"][0]:
                return export_ast.body[0].value.args[0].id
            else:
                print("export code not correct")
                return None
        self.target_id = check_build_ast()

        def_ast = ast.parse(self.code_def)
        # 1. keep only supported expr: assignment expr
        class RemoveNonAssign(ast.NodeTransformer):
            def visit_Module(self, node):
                new_body = []
                for expr in node.body:
                    if isinstance(expr, ast.Assign):
                        new_body.append(expr)
                node.body = new_body
                return node
        new_ast = ast.fix_missing_locations(RemoveNonAssign().visit(def_ast))

        # 2.turn all Function call to BinOp
        new_ast = ast.fix_missing_locations(ReplaceCallOp().visit(new_ast))

        # 3.turn assignment function to bin op, do the grammer check meanwhile
        t = Traversal()
        t.visit(new_ast)
        
        self.result_tree = t.know_nodes[self.target_id]


    def _compile_and_run(self):
        # config
        lineo = self.code_config.split(":")
        lineo = [a.strip() for a in lineo]
        self.mode = lineo[1]
        globals_freevars = {"config_mode" : self.mode_flag[self.mode]}

        # main
        self.main_code_obj = compile(self.code_def, filename='<string>', mode='exec')
        global_modules = [self.import_mod(mod) for mod in self.script_globals]
        global_expand = []
        for mod in global_modules:
            kws = getmembers(mod, isfunction) + getmembers(mod, isclass)
            global_expand.extend(kws)
        self.final_globals = {keyword[0]:keyword[1] for keyword in global_expand}
        self.final_globals.update(globals_freevars)
        
        self.code_result_dict = {}
        exec(self.main_code_obj, self.final_globals, self.code_result_dict)
        self.code_result_dict.update({"target_id":self.target_id})
        if DEBUG:
            print(self.code_result_dict)
        return str(self.code_result_dict)




# IO
class _Context:
    '''
    manage the context of Geometry Script
    when server pass the code, it passed the complete script file
    '''
    SECTION_NUM = 3

    def __init__(self, input, type=None):
        super().__init__()
        if type == 'f':
            self._read(input)
            self._preprocess()
        else:
            self._preprocess_string(input)
        # self._compile()

    # @classmethod
    # def sim_token(cls, string):
    #     start_idx = 0
    #     for i, s in enumerate(string):
    #         if s not in cls.keywords["delimiter"]:
    #             continue
    #         else:
    #             start_idx += 1
    #             yield s[start_idx, i]

    # IO
    def _read(self, script_file):
        self.file = script_file

    def _preprocess_string(self, code_str):
        code_section = []
        cur_section = ""
        for ln, line in enumerate(code_str.splitlines()):
            line = line + '\n'
            if line[:2] == keywords["splitter"]:
                code_section.append(cur_section)
                cur_section = ""
            else:
                cur_section += line
        code_section.append(cur_section)
        if len(code_section) != self.SECTION_NUM:
            print("not correct!")

        self.code_config = code_section[0]
        self.code_def = code_section[1]
        self.code_export = code_section[2]

    def _preprocess(self):
        '''
        split the context into seperated code block
        '''        
        code_section = []
        with open(self.file) as f:
            cur_section = ""
            for ln, line in enumerate(f):
                # if ln == 0: # TODO
                if line[:2] == keywords["splitter"]:
                    code_section.append(cur_section)
                    cur_section = ""
                else:
                    cur_section += line
            code_section.append(cur_section)

        if len(code_section) != self.SECTION_NUM:
            print("not correct!")

        self.code_config = code_section[0]
        self.code_def = code_section[1]
        self.code_export = code_section[2]




class Prompt:
    '''
    return the transpiler result
    '''
    pass




if __name__ == "__main__":
    c = Transpiler("./demo.gs")
    c.run()