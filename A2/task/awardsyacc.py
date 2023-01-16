import ply.yacc as yacc
import ply.lex as lex

tokens = [
    'BEGINAWARDS',
    'OPENBODY', 'CLOSEBODY', 'OPENROW', 'CLOSEROW', 'OPENHEAD', 'CLOSEHEAD', 'OPENDATA','CLOSEDATA',
    'OPENHREF', 'CLOSEHREF',
    'CONTENT', 'GARBAGE'
]

t_ignore = '\t'

def t_BEGINAWARDS(t):
    '''<table\sclass="wikitable"\sstyle="text-align:center">'''
    return t

def t_OPENBODY(t):
    r'<tbody.*?>'
    return t

def t_CLOSEBODY(t):
    r'</tbody>'
    return t

def t_OPENHEAD(t):
    r'<th.*?>'
    return t

def t_CLOSEHEAD(t):
    r'</th>'
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
    r'</td>'
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
    '''[A-za-zñáćéíóúü0-9.,:;#& ]+'''
    return t

def t_GARBAGE(t):
    r'<.*?>'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    t.lexer.skip(1)


awardlist = []

def p_start(p):
    '''start : awards'''

def p_awards(p):
    '''awards : before BEGINAWARDS OPENBODY rows CLOSEBODY'''

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
    '''rows : OPENROW OPENHEAD OPENHREF CONTENT CLOSEHREF CLOSEHEAD OPENHEAD CONTENT CLOSEHEAD OPENHEAD CONTENT CLOSEHEAD CLOSEROW rows
            | OPENROW columns CLOSEROW rows
            | OPENROW OPENHEAD OPENHREF CONTENT CLOSEHREF CLOSEHEAD CLOSEROW rows
            | '''
    if len(p) > 10:
        awardlist.append([p[4],p[8],p[11]])
    elif len(p) == 9:
        awardlist.append(p[4])

def p_columns(p):
    '''columns : OPENDATA OPENHREF CLOSEHREF OPENHREF CONTENT CLOSEHREF CLOSEDATA columns
               | OPENDATA CONTENT CONTENT CLOSEDATA columns
               | OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CLOSEDATA columns
               | '''
    if len(p)==9:
        awardlist.append(p[5])
    elif len(p)==5:
        awardlist.append(p[2])
    elif len(p)==8:
        awardlist.append(p[4])

def p_error(p):
    pass



def getAwardsList():
    global awardlist
    awardlist = []
    lexer = lex.lex()
    parser = yacc.yacc()
    f_obj = open('fifa.html','r',encoding='utf-8')
    data = f_obj.read()
    res = parser.parse(data)
    balltype = awardlist[-1]
    ballwinner = awardlist[0:3][::-1]
    boottype = awardlist[-2]
    bootwinner = awardlist[3:6][::-1]
    otherawards ={}
    otherawards[awardlist[-3]]=awardlist[6]
    otherawards[awardlist[-4]]=awardlist[7]
    otherawards[awardlist[-5]]=awardlist[8]
    winners = {}
    winners[balltype[0]]=ballwinner[0]
    winners[balltype[1]]=ballwinner[1]
    winners[balltype[2]]=ballwinner[2]
    winners[boottype[0]]=bootwinner[0]
    winners[boottype[1]]=bootwinner[1]
    winners[boottype[2]]=bootwinner[2]
    for key in otherawards:
        winners[key]=otherawards[key]
    return winners