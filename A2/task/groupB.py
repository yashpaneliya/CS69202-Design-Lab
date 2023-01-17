import ply.yacc as yacc
import ply.lex as lex

stagelist = []
matchlist = []
scorerlist = []
matchdetails = []

tokens=[
    'BEGINSTAGEB', 'BEGINSTAGEC', 'OPENMATCHDIV',
    'OPENPOINTTABLE', 'CLOSEPOINTTABLE', 'OPENTABLE', 'OPENLIST', 'CLOSELIST', 'OPENROW', 'CLOSEROW', 'OPENDATA', 'CLOSEDATA', 'OPENHEADER', 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF', 'SEPARATOR',
    'CONTENT', 'GARBAGE', 'OPENLINK', 'OPENABBR', 'CLOSEABBR', 'FRIGHTDIV'
]

def t_BEGINSTAGEB(t):
    '''<span\sclass="mw-headline"\sid="Group_B">Group\sB</span>'''
    return t

def t_BEGINSTAGEC(t):
    '''<span\sclass="mw-headline"\sid="Group_C">Group\sC</span>'''
    return t

def t_OPENPOINTTABLE(t):
    '''<table\sclass="wikitable"\sstyle="text-align:center;">'''
    return t

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
    r'[A-Za-z0-9ñáćéíøäæóúÁÉÜÚÑÓÍïüšëčýÿû,$#§&.\-:;@ \'")\(–]+'
    return t

def t_GARBAGE(t):
    r'<.*?>'

def t_error(t):
    t.lexer.skip(1)

def p_start(p):
    '''start : before BEGINSTAGEB skip OPENPOINTTABLE handletable CLOSEPOINTTABLE skip SEPARATOR handlematches BEGINSTAGEC'''

def p_handletable(p):
    '''handletable : OPENROW handlerow CLOSEROW handletable
                   | '''

def p_handlerow(p):
    '''handlerow : OPENHEADER skip CLOSEHEADER OPENHEADER skip OPENLIST skip CLOSELIST OPENLIST skip CLOSELIST OPENLIST skip CLOSELIST CLOSEHEADER OPENHEADER skip CLOSEHEADER OPENHEADER skip CLOSEHEADER OPENHEADER skip CLOSEHEADER OPENHEADER skip CLOSEHEADER OPENHEADER skip CLOSEHEADER OPENHEADER skip CLOSEHEADER OPENHEADER skip CLOSEHEADER OPENHEADER skip CLOSEHEADER OPENHEADER skip CLOSEHEADER handlerow
                 | OPENDATA skip CLOSEDATA OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA handlerow
                 | OPENDATA skip CLOSEDATA OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA skip CLOSEDATA handlerow
                 | OPENDATA skip CLOSEDATA OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CLOSEHEADER OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA handlerow
                 | '''
    if len(p)==35:
        stagelist.append(p[7]+" "+p[23]+" "+p[26])
    elif len(p)==38:
        stagelist.append(p[7]+" "+p[23]+" "+p[26])
    elif len(p)==37:
        stagelist.append(p[7]+" "+p[13]+" " +p[25])
    
def p_handlematches(p):
    '''handlematches : skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches
                     | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches
                     | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails
                     | '''
    if len(p)>1:
        matchlist.append(p[7]+" "+p[13]+" "+p[19])

def p_handlescorer(p):
    '''handlescorer : skip OPENLIST OPENHREF CONTENT CLOSEHREF skip CLOSELIST handlescorer
                    | '''
    if len(p)>1:
        scorerlist.append(p[4])

def p_handledetails(p):
    '''handledetails : OPENHREF CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT OPENHREF CONTENT CLOSEHREF skip'''
    # print(p[2],p[4],p[6],p[8],p[9],p[11])
    matchdetails.append(p[2]+" "+p[4]+" "+p[6]+" "+p[8]+" "+p[9]+" "+p[11])

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
              | OPENPOINTTABLE before
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
    print('Error at line ', p)
    pass

def groupB():
    global stagelist
    global matchlist
    global scorerlist
    global matchdetails
    stagelist = []
    matchlist = []
    scorerlist = []
    matchdetails = []
    lexer = lex.lex()
    parser = yacc.yacc()
    f=open('fifa.html','r',encoding='utf-8')
    data = f.read()
    lexer.input(data)
    res = parser.parse(data)
    matchlist.reverse()
    groupBdata = {
        'pointtable' : stagelist,
        'matchlist' : matchlist,
        'matches' : {
            '1': {
                'score' : matchlist[0],
                'details' : matchdetails[0],
                'scorers' : [scorerlist[0],scorerlist[1],scorerlist[2],scorerlist[3],scorerlist[4],scorerlist[5]]
            },
            '2': {
                'score' : matchlist[1],
                'details' : matchdetails[1],
                'scorers' : [scorerlist[6],scorerlist[7]]
            },
            '3': {
                'score' : matchlist[2],
                'details' : matchdetails[2],
                'scorers' : [scorerlist[8],scorerlist[9]]
            },
            '4': {
                'score' : matchlist[3],
                'details' : matchdetails[3],
                'scorers' : []
            },
            '5': {
                'score' : matchlist[4],
                'details' : matchdetails[4],
                'scorers' : [scorerlist[10],scorerlist[11]]
            },
            '6': {
                'score' : matchlist[5],
                'details' : matchdetails[5],
                'scorers' : [scorerlist[12]]
            }
        }
    }
    f.close()
    return groupBdata