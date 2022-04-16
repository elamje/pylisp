# look at intepreter limits

#####################
################
###########
######

# Adapted from P Norvig's example (http://norvig.com/lispy.html)
# Let's make this clojure flavored
# ast is just a list of lists

'''
Can we do better?
Can we interop with python libs?
Can we write the code in a python file and have it execute without wrapping
'''

'''
Define types
'''
symbol = str              # A Scheme Symbol is implemented as a Python str
num = (int, float)     # A Scheme Number is implemented as a Python int or float
literal   = (Symbol, Number) # A Scheme Atom is a Symbol or Number
list   = list             # A Scheme List is implemented as a Python list
exp    = (Atom, List)     # A Scheme expression is an Atom or List
env    = dict             # A Scheme environment (defined below) 
                          # is a mapping of {variable: value}

def literalize(token: str):
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return symbol(token)


def tokenize(code: str):
    return code.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(code: str):
    return read_tokens(tokenize(code))

def read_tokens(tokens: list) -> list:
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        l = []
        while tokens[0] != ')':
            l.append(read_tokens(tokens))
        tokens.pop(0)
        return l
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return literalize(token)

import math
import operator

def default_env():
    ''' Set up a basic lisp env '''
    return {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        'print': print
    }

global_env = default_env()

def eval(x: exp, env=global_env):
    if isinstance(x, symbol):
        return env[x]
    if isinstance(x, num):
        return x
    else:
        try:
            proc = eval(x[0], env)
            args = [eval(arg, env) for arg in x[1:]]
            return proc(*args)
        except IndexError:
            pass

def run(x: exp, env=global_env):
    return eval(parse(x), env)


#### Run directly
run('''
(+ 1 1)
''')

#### Run with a decorator
def lispy(func: callable):
    def wrap():
        out = run(func())
        print(out)
    return wrap

@lispy
def code():
    return '''
    (+ 1 1)
    '''
#### Run from file TODO
#### Run from repl TODO
