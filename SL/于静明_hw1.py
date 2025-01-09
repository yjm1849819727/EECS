import pdb
import lib601.sm as sm
import string
import operator

#####some thing should be known at first#######
#python 2.6.6(main frame work from the web of our class)
#tokenizer finished
#Parsing a token sequnence finished
#Evaluation finished
#Lazy partial evaluation finished
#the command to test the code is at the last of the file
###################################


class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return self.opStr + '(' + \
               str(self.left) + ', ' +\
               str(self.right) + ')'
    __repr__ = __str__

    def  eval(self,env):
        left_val = self.left.eval(env)
        right_val = self.right.eval(env)
        if isNum(left_val) and isNum(right_val):
            return self.op(left_val,right_val)
        else:
            return self.__class__(left_val,right_val)
    
class Sum(BinaryOp):
    opStr = 'Sum'
    op = operator.add

class Prod(BinaryOp):
    opStr = 'Prod'
    op = operator.mul

class Quot(BinaryOp):
    opStr = 'Quot'
    op = operator.truediv

class Diff(BinaryOp):
    opStr = 'Diff'
    op = operator.sub

class Assign(BinaryOp):
    opStr = 'Assign'

    def eval(self,env):
        value = self.right.eval(env)
        env[self.left.name] = Number(value)
        return None
        
class Number:
    def __init__(self, val):
        self.value = val
        
    def __str__(self):
        return 'Num('+str(self.value)+')'
    __repr__ = __str__

    def eval(self,env):
        return self.value

class Variable:
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return 'Var('+self.name+')'
    __repr__ = __str__

    def eval(self,env):
        if self.name in env:
            return env[self.name]
        else:
            return self


# characters that are single-character tokens
seps = ['(', ')', '+', '-', '*', '/', '=']

# Convert strings into a list of tokens (strings)
def tokenize(input_string):
    # <your code here>
    tokens = []
    current_token = ''
    for char in input_string:
        if char in seps:
            if current_token:
                tokens.append(current_token)
                current_token = ''
            tokens.append(char)
        elif char in string.whitespace:
            if current_token :
                tokens.append(current_token)
                current_token = ''
        else:
            current_token += char
    if current_token:
        tokens.append(current_token)
    return tokens
    pass

# tokens is a list of tokens
# returns a syntax tree:  an instance of {\tt Number}, {\tt Variable},
# or one of the subclasses of {\tt BinaryOp} 
def parse(tokens):
    def parseExp(index):
        # <your code here>
        token = tokens[index]
        if numberTok(token):
            return (Number(float(token)),index+1)
        elif variableTok(token):
            return (Variable(token),index+1)
        elif token == '(':
            (leftTree,nextIndex) = parseExp(index+1)
            op = tokens [nextIndex]
            (rightTree,nextIndex) = parseExp (nextIndex+1)
            if tokens[nextIndex] != ')':
                raise SyntaxError ('Expected closing parenthesis')
            nextIndex +=1
            if op == '+':
                return (Sum(leftTree,rightTree),nextIndex)
            elif op == '-':
                return (Diff(leftTree,rightTree),nextIndex)
            elif op == '*':
                return (Prod(leftTree,rightTree),nextIndex)
            elif op == '/':
                return (Quot(leftTree,rightTree),nextIndex)
            elif op == '=':
                return (Assign(leftTree,rightTree),nextIndex)
            else:
                raise SyntaxError('Unknown operator: '+op)
        else:
            raise SyntaxError('Unexpected token: '+token)
        pass
    (parsedExp, nextIndex) = parseExp(0)
    return parsedExp

# token is a string
# returns True if contains only digits
def numberTok(token):
    for char in token:
        if not char in string.digits: return False
    return True

# token is a string
# returns True its first character is a letter
def variableTok(token):
    for char in token:
        if char in string.letters: return True
    return False

# thing is any Python entity
# returns True if it is a number
def isNum(thing):
    return type(thing) == int or type(thing) == float

# Run calculator interactively
def calc():
    env = {}
    while True:
        e = raw_input('%')            # prints %, returns user input
        if not e.strip():
            continue
        parsed_exp = parse(tokenize(e))
        result = parsed_exp.eval(env)
        if result is not None:
            print(result)
        print('  env  =',env)

# exprs is a list of strings
# runs calculator on those strings, in sequence, using the same environment
def calcTest(exprs):
    print('----------------------------------------------------------calcTest-------------------------------------------------------')
    env = {}
    for e in exprs:
        print ('%', e)                   # e is the experession
        parsed_exp = parse(tokenize(e))
        result = parsed_exp.eval(env)
        if result is not None:
            print(result)
            print('  env =',env)

# Simple tokenizer tests
'''Answers are:
['fred']
['777']
['777', 'hi', '33']
['*', '*', '-', ')', '(']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
'''
def testTokenize():
    print('-------------------------------------------------------testTokenize-------------------------------------------------------')
    print tokenize('fred ')
    print tokenize('777 ')
    print tokenize('777 hi 33 ')
    print tokenize('**-)(')
    print tokenize('( hi * ho )')
    print tokenize('(fred + george)')
    print tokenize('(hi*ho)')
    print tokenize('( fred+george )')

# Simple parsing tests from the handout
'''Answers are:
Var(a)
Num(888.0)
Sum(Var(fred), Var(george))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Assign(Var(a), Prod(Num(3.0), Num(5.0)))
'''
def testParse():
    print('-------------------------------------------------------testParse-------------------------------------------------------')
    print parse(['a'])
    print parse(['888'])
    print parse(['(', 'fred', '+', 'george', ')'])
    print parse(['(', '(', 'a', '*', 'b', ')', '/', '(', 'cee', '-', 'doh', ')' ,')'])
    print parse(tokenize('((a * b) / (cee - doh))'))
    print parse(tokenize('(a = (3 * 5))'))

####################################################################
# Test cases for EAGER evaluator
####################################################################

def testEval():
    print('-------------------------------------------------------testEval-------------------------------------------------------')
    env = {}
    Assign(Variable('a'), Number(5.0)).eval(env)
    print Variable('a').eval(env)
    env['b'] = 2.0
    print Variable('b').eval(env)
    env['c'] = 4.0
    print Variable('c').eval(env)
    print Sum(Variable('a'), Variable('b')).eval(env)
    print Sum(Diff(Variable('a'), Variable('c')), Variable('b')).eval(env)
    Assign(Variable('a'), Sum(Variable('a'), Variable('b'))).eval(env)
    print Variable('a').eval(env)
    print env

#testEval()
# Basic calculator test cases (see handout)
testExprs = ['(2 + 5)',
             '(z = 6)',
             'z',
             '(w = (z + 1))',
             'w'
             ]
#calcTest(testExprs)

####################################################################
# Test cases for LAZY evaluator
####################################################################

# Simple lazy eval test cases from handout
'''Answers are:
Sum(Var(b), Var(c))
Sum(2.0, Var(c))
6.0
'''
def testLazyEval():
    print('-------------------------------------------------------testLazyEval-------------------------------------------------------')
    env = {}
    Assign(Variable('a'), Sum(Variable('b'), Variable('c'))).eval(env)
    print Variable('a').eval(env)
    env['b'] = Number(2.0)
    print Variable('a').eval(env)
    env['c'] = Number(4.0)
    print Variable('a').eval(env)

# Lazy partial eval test cases (see handout)
lazyTestExprs = ['(a = (b + c))',
                  '(b = ((d * e) / 2))',
                  'a',
                  '(d = 6)',
                  '(e = 5)',
                  'a',
                  '(c = 9)',
                  'a',
                  '(d = 2)',
                  'a']

## More test cases (see handout)
partialTestExprs = ['(z = (y + w))',
                    'z',
                    '(y = 2)',
                    'z',
                    '(w = 4)',
                    'z',
                    '(w = 100)',
                    'z']

# calcTest(partialTestExprs)

#test scripts
testTokenize()
testParse()
testEval()
calcTest(testExprs)
testLazyEval()
calcTest(lazyTestExprs)
