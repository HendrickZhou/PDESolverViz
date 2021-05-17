import tokenize

with open("../transpiler/demo.gs", 'rb') as f:
    ts = tokenize.tokenize(f.readline)
