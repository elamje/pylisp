# look at decorators

# look at intepreter limits

def test():
    assert apply(*parse("(+ 2 2)")) == '22'
    #assert apply(*parse("(+ (+ 1 1) 2)")) == '112'

def map_operator(fn: str):
    import operator
    if fn == "+":
        return operator.add

def parse(sexp: str):
    ''' assume valid sexp and first/last char are parens pair, does not handle nested sexp '''
    no_parens = sexp[1:-1] # slice off parens
    # split on whitespace
    operator, operands = no_parens.split(" ")[0], no_parens.split(" ")[1:]
    # map operator to python operation
    fn = map_operator(operator)
    # TODO handle operand types, right now all strings
    # return callable and its operands
    return fn, operands

def nested_parse(sexp: str):
    # base case is empty string or no more sexp to eval
    if sexp == "" or "(" not in sexp:
        return
    else:
        print (sexp)
        fn, operands = parse(sexp)
        #for each operand call nested parse
        [nested_parse(operand) for operand in operands if operand.startswith("(")]

nested_parse("(+ 2 2 (+ 2 2))")

# build ast

def apply(fn, operands):
    return fn(*operands)

test()

def lisp():
    ''' confirm that python interpreter allows this syntax '''
    '(+ 1 1)'

