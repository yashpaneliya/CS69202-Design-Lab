import ply.lex as lex
import ply.yacc as yacc

tokens = [
    'BEGINPLAYER', 'BEGINCLUB', 'BEGINCAREER', 'BEGINIC', 'ENDIC', 'BEGINSCAREER',
    'OPENHEAD', 'CLOSEHEAD', 'OPENDATA', 'CLOSEDATA', 'OPENROW', 'CLOSEROW',
    'CONTENT','OPENRB', 'CLOSERB', 'ARROW', 'LOAN',
    'SB', 'GARBAGE',
]

def t_BEGINPLAYER(t):
    '''<th\scolspan="4"\sclass="infobox-header"\sstyle="background-color:\s\#b0c4de;\sline-height:\s1.5em">Personal\sinformation</th>'''
    return t

def t_BEGINCLUB(t):
    '''<th\scolspan="4"\sclass="infobox-header"\sstyle="background-color:\s\#b0c4de;\sline-height: 1.5em">Club\sinformation</th>'''
    return t

def t_BEGINCAREER(t):
    '''<th\scolspan="4"\sclass="infobox-header"\sstyle="background-color:\s\#b0c4de;\sline-height:\s1.5em">Youth\scareer</th>'''
    return t

def t_BEGINSCAREER(t):
    '''<th\scolspan="4"\sclass="infobox-header"\sstyle="background-color:\s\#b0c4de;\sline-height: 1.5em">Senior\scareer*</th>'''
    return t

def t_BEGINIC(t):
    '''<th\scolspan="4"\sclass="infobox-header"\sstyle="background-color:\s\#b0c4de;\sline-height:\s1.5em">International\scareer<sup>‡</sup></th>'''
    return t

def t_ENDIC(t):
    '''<th\scolspan="4"\sclass="infobox-header"\sstyle="background-color:\s\#b0c4de;\sline-height:\s1.5em">'''
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
    r'<\tr>'
    return t

def t_OPENDATA(t):
    r'<td.*?>'
    return t

def t_CLOSEDATA(t):
    r'</td>'
    return t

def t_ARROW(t):
    '''\s→\s'''

def t_LOAN(t):
    '''\s\(loan\)'''

def t_OPENRB(t):
    r'\(.*?'

def t_CLOSERB(t):
    r'\).*?'

def t_CONTENT(t):
    '''[A-Za-z0-9ñáćéíóúü\- ]+'''
    return t

def t_SB(t):
    r'\[.*?\]'

def t_GARBAGE(t):
    r'<.*?>'

def t_error(t):
    t.lexer.skip(1)


def p_init(p):
    '''init : before BEGINPLAYER personalinfo
            | '''

def p_before(p):
    '''before : CONTENT before
              | OPENHEAD before
              | CLOSEHEAD before
              | '''

def p_personalinfo(p):
    '''personalinfo : OPENROW OPENHEAD CONTENT CLOSEHEAD OPENDATA CONTENT skip CLOSEDATA CLOSEROW personalinfo
                    | clubinfo
                    | '''
    if len(p) > 2:
        print(p[3],p[6])

def p_clubinfo(p):
    '''clubinfo : BEGINCLUB OPENHEAD CONTENT CLOSEHEAD OPENDATA CONTENT CLOSEDATA OPENHEAD CONTENT CLOSEHEAD OPENDATA CONTENT CLOSEDATA career'''
    print(p[3], p[6])

def p_career(p):
    '''career : BEGINCAREER OPENHEAD CONTENT CONTENT CLOSEHEAD OPENDATA CONTENT CLOSEDATA scareer
            | '''

def p_scareer(p):
    '''scareer : BEGINSCAREER CLOSEROW OPENROW handlerow CLOSEROW nationalteam
            | '''

def p_handlerow(p):
    '''handlerow : OPENHEAD CONTENT CLOSEHEAD OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA handlerow
                | '''
    if len(p) > 1:
        print(p[2],p[5],p[8],p[11])

def p_nationalteam(p):
    '''nationalteam : BEGINIC handlerow ENDIC'''

def p_skip(p):
    '''skip : CONTENT skip
            | '''

def p_error(p):
    print('Error at ',p)
    pass

lexer = lex.lex()
f = open('Harry_Maguire.html','r',encoding='utf8')
log = open('log.txt','w',encoding='utf8')
data = f.read()
lexer.input(data)
while True:
    t = lexer.token()
    if t is None:
        break
    log.write(str(t)+'\n')

parser = yacc.yacc()
parser.parse(data)