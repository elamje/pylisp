# look at decorators
# look at intepreter limits
# look at ast data structures after recursive parser works
# ast should be a tree, how to do a tree in python?

def test():
    assert apply(*parse("(+ 2 2)")) == '22'
    #assert apply(*parse("(+ (+ 1 1) 2)")) == '112'

PRIMATIVES = [str, int]
OPERATORS = ["+"]

def map_operator(fn: str):
    import operator
    if fn == "+":
        return operator.add

def parse(sexp: str):
    ''' assume valid sexp and first/last char are parens pair, does not handle nested sexp '''

    no_parens = sexp[1:-1] # slice off parens
    # in case of nested sexp ignore anything after a (
    first_level = no_parens.split("(")[0].strip()
    # split on whitespace
    operator, operands = first_level.split(" ")[0], first_level.split(" ")[1:]
    # map operator to python operation
    fn = map_operator(operator)
    # TODO handle operand types, right now all strings
    # return callable and its operands
    return fn, operands

class Tree:
    def __init__(self, data, children=[]):
        self.children = children
        self.data = data
        self.meta = "future metadata"
    def add_child(self, Tree):
        self.children += [Tree]
        




def nested_parse(sexp: str, ast=Tree(data="root", children=[])) -> list:
    ''' handle (function) (function p1) (function p1 ... n)'''
    def _is_primative(p):
       return type(p) in PRIMATIVES
    if _is_primative(sexp):
       return ast
   # if sexp
    elif sexp.startswith("(") and sexp.endswith(")"):
       raw = sexp[1:-1] # raw function & params
       split = raw.split(" ")
       return ast.add_child(Tree(data=map_operator(split[0]), children = [nested_parse(x, ast) for x in split[1:]]))
    else:
       raise Exception # this should never hit

np = nested_parse("(+ 2 2 (+ 2 2))")



# build ast

def apply(fn, operands):
    return fn(*operands)

test()

def lisp():
    ''' confirm that python interpreter allows this syntax '''
    '(+ 1 1)'

# The above is my failed attempt to create a parser and evaluator without any guidance

################
###########
######
# Adapted from P Norvig's example

'''
Define types
'''
Symbol = str              # A Scheme Symbol is implemented as a Python str
Number = (int, float)     # A Scheme Number is implemented as a Python int or float
Atom   = (Symbol, Number) # A Scheme Atom is a Symbol or Number
List   = list             # A Scheme List is implemented as a Python list
Exp    = (Atom, List)     # A Scheme expression is an Atom or List
Env    = dict             # A Scheme environment (defined below) 
                          # is a mapping of {variable: value}

def literalize(token: str):
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)


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

def eval(x: Exp, env=global_env):
    if isinstance(x, Symbol):
        return env[x]
    if isinstance(x, Number):
        return x
    else:
        try:
            proc = eval(x[0], env)
            args = [eval(arg, env) for arg in x[1:]]
            return proc(*args)
        except IndexError:
            pass

def run(x: Exp, env=global_env):
    return eval(parse(x), env)

