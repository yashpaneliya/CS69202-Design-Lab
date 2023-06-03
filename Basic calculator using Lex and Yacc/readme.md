# Basic calculator using Lex and Yacc

## Problem Statement
Develop a simple calculator with the following functionalities:
- Addition
- Subtraction
- Multiplication
- Division
- Prefix notation
- Postfix notation
- Variables

## Code walk-through
- The code is divided into 2 parts
    - Lex file
    - Yacc file
- Lex file contains the regular expressions for the tokens
- Yacc file contains the grammar rules and the actions to be performed on the tokens
- Sample regex in Lex file
    ```bash
    # to identify input as a variable
    t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    # identify decimal form string and convert the input to float
    def t_FLOAT(t):
        r'\d+\.\d+'
        t.value = float(t.value)
    return t
    ```
- Sample grammar rule in Yacc file
    ```bash
    # E -> E + T ==> Recursion at E
    def p_expression_plus(p):
        '''expression : expression PLUS term'''
        p[0] = p[1] + p[3]
    ```

## How to run
```bash
py yacc2.py
```

## Sample output
```bash
Input> 3+2
5
Input> prefix(9+8-9)
+9-89
Input> postfix(9+8-9)
98+9-
Input> 25/5
5.0
Input> 8*9
72
Input> 5*(9+8)
85
Input> x=5
Input> y=6
Input> x+y
11
Input> x+y+z
invalid input 'z'
Input>
```