class Token():
    def __init__(self, string):
        self.string = string
        self.silenced = False

def tokenize(str):
    return map(lambda s: Token(s), str.split('\n'))

def untokenize(tokens):
    newStr = ''
    for t in tokens:
        if not t.silenced:
            newStr += t.string + '\n'
    return newStr
