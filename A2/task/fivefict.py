# PARSER to get last 5 matches

import ply.lex as lex
import ply.yacc as yacc

tokens = [
    'BEGINPREV', 'BEGINNEXT',
    'OPENHREF', 'CLOSEHREF', 'ABBR', 'CLOSEABBR', 'OPENDIV', 'CLOSEDIV', 'OPENTABLE', 'CLOSETABLE',
    'CONTENT', 'GARBAGE', 'STAFF',
]

def t_BEGINPREV(t):
    '''<span\sclass="mw-headline"\sid="2022">2022</span>'''
    return t

def t_BEGINNEXT(t):
    '''<span\sclass="mw-headline"\sid="2023">2023</span>'''
    return t

def t_STAFF(t):
    '''<span\sclass="mw-headline"\sid="Coaching_staff">Coaching\sstaff</span>'''
    return t

def t_OPENTABLE(t):
    r'<table.*?>'
    return t

def t_CLOSETABLE(t):
    r'</table>'
    return t

def t_OPENDIV(t):
    r'<div.*?>'
    return t

def t_CLOSEDIV(t):
    r'</div.*?>'
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
    '''[A-Za-z0-9ñáćéíóúü.: ]+'''
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

prevlist = []
futlist = []

def p_init(p):
    '''init : before BEGINPREV divs BEGINNEXT futdivs STAFF
            | before BEGINPREV OPENHREF CONTENT CLOSEHREF divs BEGINNEXT OPENHREF CONTENT CLOSEHREF futdivs STAFF
            | before BEGINPREV divs STAFF
            | before BEGINPREV OPENHREF CONTENT CLOSEHREF divs STAFF'''

def p_before(p):
    '''before : CONTENT before
              | OPENHREF before
              | CLOSEHREF before
              | OPENDIV before
              | CLOSEDIV before
              | OPENTABLE before
              | CLOSETABLE before
              | '''

def p_divs(p):
    '''divs : OPENDIV anchors OPENTABLE skip CLOSETABLE CLOSEDIV divs
            | '''

def p_anchors(p):
    '''anchors : OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT OPENHREF CONTENT CLOSEHREF'''
    if len(p) > 1:
        prevlist.append(p[2] + " vs " + p[8])

def p_futdivs(p):
    '''futdivs : OPENDIV futanchors OPENTABLE skip CLOSETABLE CLOSEDIV futdivs
            | '''

def p_futanchors(p):
    '''futanchors : OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT OPENHREF CONTENT CLOSEHREF'''
    if len(p) > 1:
        futlist.append(p[2] + " vs " + p[8])

def p_skip(p):
    '''skip : CONTENT skip
            | OPENHREF skip
            | CLOSEHREF skip
            | OPENDIV skip
            | CLOSEDIV skip
            | '''

def p_error(p):
    pass

def getfivefixtures(filename):
    global prevlist
    global futlist
    prevlist = []
    futlist = []
    lexer = lex.lex()
    parser = yacc.yacc()
    f = open(filename+".html", 'r', encoding='utf-8')
    data = f.read()
    lexer.input(data)
    parser.parse(data)
    # check length of list is 5 or less (in case of error)
    if len(prevlist) > 5:
        prevlist = prevlist[-5:]
    if len(futlist) > 5:
        futlist = futlist[:5]
    print("================Last 5 matches================")
    for i in prevlist:
        print(i)
    print("================Next 5 matches================")
    for i in futlist:
        print(i)
    print("==============================================")

getfivefixtures("Brazil_national_football_team")