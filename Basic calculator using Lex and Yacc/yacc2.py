import ply.yacc as yacc

# importing tokens from p1.py
from p2 import tokens

# dictionary to store variables and their values
var_dict={}

# variable to store postfix expression
postfix =''

# assigning values to variables
def p_assign(p):
    'assign : ID EQUALS expression'
    var_dict[p[1]] = p[3]

# If not a assignment expression then it is an expression
def p_expression(p):
    '''assign : expression'''
    p[0] = p[1]

# rule for double equals
def p_double_equals(p):
    'expression : expression DOUBLE_EQUALS expression'
    if p[1] == p[3]:
        p[0] = 'yes'
    else:
        p[0] = 'no'

# E -> E + T
def p_expression_plus(p):
    '''expression : expression PLUS term'''
    global postfix
    p[0] = p[1] + p[3]
    postfix = postfix + '+'

# E -> E - T
def p_expression_minus(p):
    '''expression : expression MINUS term'''
    global postfix
    p[0] = p[1] - p[3]
    postfix = postfix + '-'

# E -> T
def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

# T -> T * F
def p_term_times(p):
    '''term : term TIMES factor'''
    global postfix
    p[0] = p[1] * p[3]
    postfix = postfix + '*'

# T -> T / F
def p_term_divide(p):
    'term : term DIVIDE factor'
    global postfix
    if p[3] == 0 :
        print("Can't divide by 0")
        raise ZeroDivisionError('integer division by 0')
    p[0] = p[1] / p[3]
    postfix = postfix + '/'

# T -> F
def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

# F -> F ^ F
def p_factor_power(p):
    'factor : factor POWER factor'
    global postfix
    p[0] = p[1] ** p[3]
    postfix = postfix + '^'

# F -> F % F
def p_factor_mod(p):
    'factor : factor MOD factor'
    global postfix
    p[0] = p[1] % p[3]
    postfix = postfix + '%'

# F -> -F
def p_factor_unary(p):
    'factor : MINUS factor'
    global postfix
    p[0] = -p[2]
    postfix = postfix + '-'

# F -> ID
def p_factor_id(p):
    'factor : ID'
    if p[1] not in var_dict:
        print("invalid input '%s'" % p[1])
        raise NameError('Undefined variable')
    p[0] = var_dict[p[1]]

# F -> INT
def p_factor_number(p):
    'factor : INT'
    global postfix
    p[0] = p[1]
    postfix = postfix + str(p[0])

# F -> FLOAT
def p_factor_float(p):
    'factor : FLOAT'
    global postfix
    p[0] = p[1]
    postfix = postfix + str(p[0])

# F -> (E)
def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]
    
# Error rule for syntax errors
def p_error(p):
    print("Syntax error at '%s'" % p.value)
    quit()

# Build the parser
parser = yacc.yacc()

# Driver code
while True:
    # clearing postfix expression
    postfix=''
    try:
        # taking expression as input
        s = input('Input> ')
    except EOFError:
        break
    try:
        # checking if the input is a variable
        if var_dict[s]:
            print(var_dict[s])
        continue
    except KeyError:
        pass

    temp=''
    if s=='exit':
        print("Exiting...")
        break
    if 'postfix' in s:
        # extracting the expression
        temp=s
        s = s[8:-1]
    if 'prefix' in s:
        # extracting the expression
        temp=s
        s = s[7:-1]
        # reversing the expression to perform postfix on it in order to get prefix of original expression
        s = s[::-1]
    
    # parsing the expression
    try:
        res = parser.parse(s)
        if res is not None:
            if 'postfix' in temp:
                print(postfix)
            elif 'prefix' in temp:
                print(postfix[::-1])
            else:
                print(res)
    except ZeroDivisionError:
        pass
    except NameError:
        pass