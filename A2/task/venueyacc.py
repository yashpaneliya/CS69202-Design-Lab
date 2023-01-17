import ply.yacc as yacc
import ply.lex as lex

tokens = [
    'BEGINVENUE',
    'OPENBODY', 'CLOSEBODY', 'OPENROW', 'CLOSEROW', 'OPENDATA', 'CLOSEDATA', 'OPENHEAD', 'CLOSEHEAD', 'OPENHREF', 'CLOSEHREF',
    'CONTENT', 'GARBAGE', 'WHITESPACE', 'OPENDIV', 'CLOSEDIV', 'OPENSTYLE', 'CLOSESTYLE',
]

def t_BEGINVENUE(t):
    '''<h3><span\sclass="mw-headline"\sid="Stadiums">Stadiums</span></h3>'''
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

def t_WHITESPACE(t):
    '''[ ]+'''

def t_CONTENT(t):
    '''[A-Za-z0-9, ]+'''
    return t

def t_OPENDIV(t):
    '''<div[^>]*>'''

def t_CLOSEDIV(t):
    '''</div[^>]*>'''

def t_OPENSTYLE(t):
    '''<style[^>]*>'''

def t_CLOSESTYLE(t):
    '''</style[^>]*>'''

def t_GARBAGE(t):
    r'<.*?>'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    t.lexer.skip(1)

# Build the lexer

venue = {}

def p_init(p):
    '''init : before BEGINVENUE skip OPENBODY rows CLOSEBODY'''

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
            | OPENROW OPENHEAD skip CLOSEHEAD columns CLOSEROW rows
            | OPENROW columns CLOSEROW rows
            | '''

def p_columns(p):
    '''columns : OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA CONTENT skip CLOSEDATA'''
    if len(p)==10:
        venue[p[3]] = p[7]

def p_skip(p):
    '''skip : CONTENT skip
            | OPENHREF skip
            | CLOSEHREF skip
            | '''

def p_error(p):
    pass


def getVenueList():
    global venue
    venue = {}
    lexer = lex.lex()
    parser = yacc.yacc()
    f=open('fifa.html','r',encoding='utf-8')
    data = f.read()
    res = parser.parse(data)
    f.close()
    return venue