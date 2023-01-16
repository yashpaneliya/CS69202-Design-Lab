import ply.yacc as yacc
import ply.lex as lex

tokens=[
    'OPENQUARTER', 'CLOSEQUARTER', 'OPENMATCHDIV',
    'OPENPOINTTABLE', 'CLOSEPOINTTABLE', 'OPENTABLE', 'OPENLIST', 'CLOSELIST', 'OPENROW', 'CLOSEROW', 'OPENDATA', 'CLOSEDATA', 'OPENHEADER', 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF', 'SEPARATOR',
    'CONTENT', 'GARBAGE', 'OPENLINK', 'OPENABBR', 'CLOSEABBR', 'FRIGHTDIV'
]

def t_OPENQUARTER(t):
    '''<span\sclass="mw-headline"\sid="Quarter-finals">Quarter\-finals</span>'''
    return t

def t_CLOSEQUARTER(t):
    '''<span\sclass="mw-headline"\sid="Semi-finals">Semi\-finals</span>'''
    return t

# def t_OPENPOINTTABLE(t):
#     '''<table\sclass="wikitable"\sstyle="text-align:center;">'''
#     return t

def t_OPENTABLE(t):
    '''<table\sclass="fevent">'''
    return t

def t_CLOSEPOINTTABLE(t):
    '''</table>'''
    return t

def t_OPENMATCHDIV(t):
    '''<div\sitemscope=""\sitemtype="http&\#58;//schema.org/SportsEvent"\sclass="footballbox">'''
    return t

def t_FRIGHTDIV(t):
    '''<div\sclass="fright">'''
    return t

def t_SEPARATOR(t):
    '''<link\srel="mw-deduplicated-inline-style"\shref="mw-data:TemplateStyles:r997937747"/>'''
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

def t_OPENLINK(t):
    r'<link.*?>'

def t_OPENABBR(t):
    r'<abbr.*?>'

def t_CLOSEABBR(t):
    r'</abbr>'   

def t_OPENLIST(t):
    r'<li .*?>'
    return t

def t_CLOSELIST(t):
    r'</li>'
    return t

def t_OPENHREF(t):
    r'<a .*?>'
    return t

def t_CLOSEHREF(t):
    r'</a>'
    return t

def t_OPENHEADER(t):
    r'<th.*?>'
    return t

def t_CLOSEHEADER(t):
    r'</th>'
    return t

def t_CONTENT(t):
    r'[A-Za-z0-9ñáãćéíøäæóōúńÁÉÜÚÑğÓÍïüšëčýÿû,$#§&.+\-:;@ \'")\(–]+'
    return t
	
def t_GARBAGE(t):
    r'<.*?>'

def t_error(t):
    t.lexer.skip(1)

def p_start(p):
    '''start : before OPENQUARTER skip SEPARATOR handlematches CLOSEQUARTER'''

def p_handlematches(p):
    '''handlematches : skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches
                     | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches
                     | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails
                     | skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF skip CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENHEADER CONTENT CLOSEHEADER OPENDATA handlepenscorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches
                     | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF skip CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENHEADER CONTENT CLOSEHEADER OPENDATA handlepenscorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches
                     | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF skip CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENHEADER CONTENT CLOSEHEADER OPENDATA handlepenscorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails
                     | '''
    if len(p) > 1 and len(p) < 45:
        print(p[7],p[13],p[19])
    elif len(p) > 45:
        print(p[7],p[13],p[20])

def p_handlescorer(p):
    '''handlescorer : skip OPENLIST OPENHREF CONTENT CLOSEHREF skip CLOSELIST handlescorer
                    | '''
    if len(p)>1:
        print(p[4])

def p_handlepenscorer(p):
    '''handlepenscorer : skip OPENLIST CONTENT OPENHREF CONTENT CLOSEHREF skip CLOSELIST handlepenscorer
                    | '''
    if len(p)>1:
        print(p[5])

def p_handledetails(p):
    '''handledetails : OPENHREF CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT OPENHREF CONTENT CLOSEHREF skip'''
    print(p[2],p[4],p[6],p[8],p[9],p[11])

def p_before(p):
    '''before : CONTENT before
              | OPENHREF before 
              | CLOSEHREF before
              | OPENHEADER before
              | CLOSEHEADER before
              | OPENDATA before
              | CLOSEDATA before
              | OPENROW before
              | CLOSEROW before
              | OPENLIST before
              | CLOSELIST before
              | OPENTABLE before
              | OPENLINK before
              | CLOSEPOINTTABLE before
              | OPENMATCHDIV before
              | FRIGHTDIV before
              | SEPARATOR before
              | ''' 

def p_skip(p):
    '''skip : CONTENT skip
            | OPENHREF skip
            | CLOSEHREF skip
            | '''

def p_error(p):
    print("Error ",p)
    pass

if __name__ == "__main__":
    lexer = lex.lex()
    parser = yacc.yacc()
    f=open('fifa.html','r',encoding='utf-8')
    data = f.read()
    lexer.input(data)
    log = open('log.txt','w', encoding='utf8')
    while True:
        tok = lexer.token()
        if not tok:
            break
        log.write(str(tok)+'\n')
    log.close()
    res = parser.parse(data)
    # print(res)
    f.close()