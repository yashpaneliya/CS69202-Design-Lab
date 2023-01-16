import ply.yacc as yacc
import ply.lex as lex

tokens = [
    'BEGINTEAMS',
    'OPENBODY', 'CLOSEBODY', 'OPENROW', 'CLOSEROW', 'OPENDATA', 'CLOSEDATA', 'OPENHEAD', 'CLOSEHEAD', 'OPENHREF', 'CLOSEHREF',
    'CONTENT', 'GARBAGE'
]

t_ignore = '\t'

def t_BEGINTEAMS(t):
    '''<table\sclass="wikitable\ssortable\smw-collapsible\smw-collapsed">'''
    return t

def t_OPENBODY(t):
    r'<tbody.*?>'
    return t

def t_CLOSEBODY(t):
    r'</tbody>'
    return t

def t_OPENROW(t):
    r'<tr.*?>'
    return t

def t_CLOSEROW(t):
    r'</tr>'
    return t

def t_OPENDATA(t):
    r'<td.*?>'
    return t

def t_CLOSEDATA(t):
    r'</td.*?>'
    return t

def t_OPENHEAD(t):
    r'<th.*?>'
    return t

def t_CLOSEHEAD(t):
    r'</th>'
    return t

def t_OPENHREF(t):
    r'<a .*?>'
    return t

def t_CLOSEHREF(t):
    r'</a>'
    return t

def t_CONTENT(t):
    '''[A-Za-z0-9, #&;]+'''
    return t

def t_GARBAGE(t):
    r'<.*?>'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    t.lexer.skip(1)

# Build the lexer

nationlist = []

def p_init(p):
    '''init : teams'''

def p_teams(p):
    '''teams : before BEGINTEAMS skip OPENBODY rows CLOSEBODY'''

def p_before(p):
    '''before : CONTENT before
              | OPENHREF before
              | CLOSEHREF before
              | OPENHEAD before
              | CLOSEHEAD before
              | OPENROW before
              | CLOSEROW before
              | OPENDATA before
              | CLOSEDATA before
              | '''

def p_rows(p):
    '''rows : OPENROW OPENHEAD CONTENT CLOSEHEAD OPENHEAD CONTENT CLOSEHEAD OPENHEAD CONTENT CLOSEHEAD CLOSEROW rows
            | OPENROW columns CLOSEROW rows
            | '''
    
def p_columns(p):
    '''columns : OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CLOSEDATA columns
               | OPENDATA skip CLOSEDATA columns
               | '''
    if len(p) == 8:
        nationlist.append(p[4])

def p_skip(p):
    '''skip : CONTENT skip
            | OPENHREF skip
            | CLOSEHREF skip
            | '''

def p_error(p):
    pass


def getTeamList():
    global nationlist
    nationlist = []
    lexer = lex.lex()
    parser = yacc.yacc()
    f_obj = open('fifa.html','r',encoding='utf-8')
    data = f_obj.read()
    res = parser.parse(data)
    nationlist.pop(5)
    nationlist.pop(10)
    f_obj.close()
    return nationlist