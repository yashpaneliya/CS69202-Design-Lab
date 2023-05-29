import ply.yacc as yacc
from urllib.request import Request, urlopen
import ply.lex as lex

tokens =[
    'BEGINSQUAD',
    'OPENBODY', 'CLOSEBODY', 'OPENROW', 'CLOSEROW', 'OPENDATA', 'CLOSEDATA', 'OPENHEAD', 'CLOSEHEAD', 'OPENHREF', 'CLOSEHREF',
    'CONTENT', 'GARBAGE', 'BRACKETS','CLOSEBRACKETS', 'ABBR', 'CLOSEABBR', 'VC', 'C'
]

def t_BEGINSQUAD(t):
    '''<span\sclass="mw-headline"\sid="Current_squad">Current\ssquad</span>'''
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

def t_ABBR(t):
    r'<abbr.*?>'

def t_CLOSEABBR(t):
    r'</abbr>'

def t_OPENHREF(t):
    r'<a.*?>'
    return t

def t_CLOSEHREF(t):
    r'</a>'
    return t

def t_CONTENT(t):
    '''[A-Za-z0-9ñáćéíøæóúÁÉÜÚÑÓÍïüšëčýÿûã,#&;\(\) \-]+'''
    return t

def t_WHITESPACE(t):
    '''[ ]+'''

def t_GARBAGE(t):
    r'<.*?>'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    t.lexer.skip(1)

squad_list = []

def p_start(p):
    '''start : init'''

def p_init(p):
    '''init : before BEGINSQUAD skip OPENBODY rows CLOSEBODY'''

def p_before(p):
    '''before : CONTENT before
              | OPENBODY before
              | CLOSEBODY before
              | OPENHEAD before
              | CLOSEHEAD before
              | OPENDATA before
              | CLOSEDATA before
              | OPENHREF before
              | CLOSEHREF before
              | OPENROW before
              | CLOSEROW before
              | '''

def p_rows(p):
    '''rows : OPENROW OPENHEAD CONTENT CLOSEHEAD OPENHEAD CONTENT CLOSEHEAD OPENHEAD CONTENT CLOSEHEAD OPENHEAD CONTENT CLOSEHEAD OPENHEAD CONTENT CLOSEHEAD OPENHEAD CONTENT CLOSEHEAD OPENHEAD CONTENT CLOSEHEAD CLOSEROW rows
            | OPENROW columns CLOSEROW rows
            | '''

def p_columns(p):
    '''columns : OPENDATA skip CLOSEDATA OPENDATA skip CLOSEDATA OPENHEAD OPENHREF CONTENT CLOSEHREF CLOSEHEAD OPENDATA skip CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA skip CLOSEDATA
               | OPENDATA skip CLOSEDATA OPENDATA skip CLOSEDATA OPENHEAD OPENHREF CONTENT CLOSEHREF CONTENT skip CLOSEHEAD OPENDATA skip CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA skip CLOSEDATA
               | OPENDATA CLOSEDATA'''
    if len(p) > 3:
        squad_list.append(p[9])

def p_skip(p):
    '''skip : CONTENT skip
            | OPENHREF skip
            | CLOSEHREF skip
            | '''

def p_error(p):
    # print("Syntax error in input! ",p)
    pass

# Build the parser
def getCurrentSquad(fname):
    global squad_list
    squad_list = []
    lexer = lex.lex()
    parser = yacc.yacc()
    f = open(fname+".html", 'r', encoding='utf-8')
    data = f.read()
    lexer.input(data)
    file = open(fname+".txt", 'w', encoding='utf-8')
    while True:
        tok = lexer.token()
        if not tok:
            break
        file.write(str(tok)+'\n')
    file.close()
    f.close()
    parser.parse(data)
    return squad_list

# print(getCurrentSquad("Australia_men%27s_national_soccer_team"))