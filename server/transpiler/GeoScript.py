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
class Context:
    '''
    manage the context of Geometry Script
    when server pass the code, it passed the complete script file
    '''
    keywords = {
        "config" : ["MODE", "2D", "3D"],
        "splitter" : "%%",
        "delimiter" : [' ', ':', '\n', '\t'],
    }
    SECTION_NUM = 3
    script_globals = ["primitive"]

    def __init__(self, filename):
        super().__init__()
        self._read(filename)
        self._preprocess()
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

    @staticmethod
    def import_mod(name):
        if(spec := importlib.util.find_spec(name)):
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
        else:
            print("can't find the language libary")
            return None

    def _compile(self):
        # config
        #
        self.main_code_obj = compile(self.code_def, filename='<string>', mode='exec')
        global_modules = [self.import_mod(mod) for mod in self.script_globals]
        global_expand = []
        for mod in global_modules:
            kws = getmembers(mod, isfunction) + getmembers(mod, isclass)
            global_expand.extend(kws)
        self.final_globals = {keyword[0]:keyword[1] for keyword in global_expand}
        
    def run(self):
        exec(self.main_code_obj, self.final_globals, self.final_globals)
        







class Prompt:
    '''
    return the transpiler result
    '''
    pass
        
class Script2Json:
    '''
    convert geometry model between code and json
    '''
    pass

class Geo2Math:
    '''
    transfer the geometry infomation to tensorflow/pytorch math equations
    '''
    pass



if __name__ == "__main__":
    c = Context("./demo.gs")