# /usr/bin/python3.8
# transpiler for Geometry Script

import types
import ast
from inspect import isfunction, isclass, getmembers
import importlib.util
# from primitive import Primitive
import primitive

# Transpiler
class Transpiler:
    pass


# IO
class _Context:
    '''
    manage the context of Geometry Script
    when server pass the code, it passed the complete script file
    '''
    keywords = {
        "config" : ["MODE", "1D", "2D", "3D"],
        "splitter" : "%%",
        "delimiter" : [' ', ':', '\n', '\t'],
        "export" : ["build"],
    }
    SECTION_NUM = 3
    script_globals = ["primitive"]
    mode_flag = {"2D":1, "3D":2}

    def __init__(self, input, type=None):
        super().__init__()
        if type == 'f':
            self._read(input)
            self._preprocess()
        else:
            self._preprocess_string(input)
        self._compile()

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
            if line[:2] == self.keywords["splitter"]:
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
                if line[:2] == self.keywords["splitter"]:
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

    def _compile(self):
        # config
        mode_flag = 1
        globals_freevars = {"config_var_mode" : self.mode_flag["2D"]}

        # main
        self.main_code_obj = compile(self.code_def, filename='<string>', mode='exec')
        global_modules = [self.import_mod(mod) for mod in self.script_globals]
        global_expand = []
        for mod in global_modules:
            kws = getmembers(mod, isfunction) + getmembers(mod, isclass)
            global_expand.extend(kws)
        self.final_globals = {keyword[0]:keyword[1] for keyword in global_expand}
        self.final_globals.update(globals_freevars)

        _ast = ast.parse(self.code_export)
        
        def check_build_ast():
            if _ast.body[0].value.func.id == self.keywords["export"][0]:
                return _ast.body[0].value.args[0].id
            else:
                print("export code not correct")
                return None

        self.target_id = check_build_ast()

    def run(self):
        self.code_result_dict = {}
        exec(self.main_code_obj, self.final_globals, self.code_result_dict)
        self.code_result_dict.update({"target_id":self.target_id})
        print(self.code_result_dict)

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


class Prompt:
    '''
    return the transpiler result
    '''
    pass




if __name__ == "__main__":
    c = _Context("./demo.gs")
    c.run()