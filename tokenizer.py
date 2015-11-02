class Token():
    def __init__(self, string):
        self.string = string
        self.silenced = False

def tokenize(str):
    return map(lambda s: Token(s), str.split('\n'))

def untokenize(tokens):
    newStr = ''
    for i in xrange(0, len(tokens)):
        if not tokens[i].silenced:
            newStr += tokens[i].string
        if not i == len(tokens) - 1:
            newStr += '\n'
    return newStr
