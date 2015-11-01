def tokenize(str):
    return str.split('\n')

def untokenize(tokens):
    newStr = ''
    for t in tokens:
        newStr += t + '\n'
    return newStr
