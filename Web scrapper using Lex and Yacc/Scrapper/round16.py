# Module: round16.py
# module to build lexer and parser for round of 16 match
import ply.yacc as yacc
import ply.lex as lex

# to store match fixtures
matchlist = []
# to store match scorers
scorerlist = []
# to store match details (stadium, attendence, referee)
matchdetails = []
# to store penalty scorers
rightpenscorerslist = []

tokens=[
    'OPENROUND', 'ENDROUND', 'OPENMATCHDIV',
    'OPENPOINTTABLE', 'CLOSEPOINTTABLE', 'OPENTABLE', 'OPENLIST', 'CLOSELIST', 'OPENROW', 'CLOSEROW', 'OPENDATA', 'CLOSEDATA', 'OPENHEADER', 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF', 'SEPARATOR',
    'CONTENT', 'GARBAGE', 'OPENLINK', 'OPENABBR', 'CLOSEABBR', 'FRIGHTDIV'
]

def t_OPENROUND(t):
    '''<span\sclass="mw-headline"\sid="Round_of_16">Round\sof\s16</span>'''
    return t

def t_ENDROUND(t):
    '''<span\sclass="mw-headline"\sid="Quarter-finals">Quarter\-finals</span>'''
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
    r'[A-Za-z0-9ñáãćéíøäæóōúńÁÉÜÚÑğÓÍïüšëčýÿû,$#§&.\-:;@ \'")\(–]+'
    return t
	
def t_GARBAGE(t):
    r'<.*?>'

def t_error(t):
    t.lexer.skip(1)

# grammar to find round of 16 stage in the html file
def p_start(p):
    '''start : before OPENROUND skip SEPARATOR handlematches ENDROUND'''

# grammar to handle each match row and extract match details (score)
def p_handlematches(p):
    '''handlematches : skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches
                     | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches
                     | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails
                     | skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF skip CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENHEADER CONTENT CLOSEHEADER OPENDATA handlepenscorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches
                     | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF skip CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENHEADER CONTENT CLOSEHEADER OPENDATA handlepenscorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches
                     | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF skip CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENHEADER CONTENT CLOSEHEADER OPENDATA handlepenscorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails
                     | '''
    if len(p) > 1 and len(p) < 45:
        matchlist.append(p[7]+" "+p[13]+" "+p[19])
    elif len(p) > 45:
        matchlist.append(p[7]+" "+p[13]+" "+p[20])

# grammar to handle scorer details and store it
def p_handlescorer(p):
    '''handlescorer : skip OPENLIST OPENHREF CONTENT CLOSEHREF skip CLOSELIST handlescorer
                    | '''
    if len(p)>1:
        scorerlist.append(p[4])

# grammar to handle penalty scorers (if any)
def p_handlepenscorer(p):
    '''handlepenscorer : skip OPENLIST CONTENT OPENHREF CONTENT CLOSEHREF skip CLOSELIST handlepenscorer
                    | '''
    if len(p)>1:
        rightpenscorerslist.append(p[5])

# grammar to handle stadium details and store it
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
    pass

def round16():
    global matchlist
    global scorerlist
    global matchdetails
    global rightpenscorerslist
    matchlist = []
    scorerlist = []
    matchdetails = []
    rightpenscorerslist = []
    lexer = lex.lex()
    parser = yacc.yacc()
    f=open('fifa.html','r',encoding='utf-8')
    data = f.read()
    lexer.input(data)
    res = parser.parse(data)
    f.close()
    matchlist.reverse()
    # formatting the data for better and generalized access in the future
    round16Data = {
        'matchlist' : matchlist,
        '1':{
            'score' : matchlist[0],
            'details' : matchdetails[0],
            'scorerlist' : [scorerlist[0],scorerlist[1],scorerlist[2],scorerlist[3]],
            'isPen' : False,
            'penscorers' : [],
        },
        '2':{
            'score' : matchlist[1],
            'details' : matchdetails[1],
            'scorerlist' : [scorerlist[4],scorerlist[5],scorerlist[6]],
            'isPen' : False,
            'penscorers' : [],
        },
        '3':{
            'score' : matchlist[2],
            'details' : matchdetails[2],
            'scorerlist' : [scorerlist[7],scorerlist[8],scorerlist[9]],
            'isPen' : False,
            'penscorers' : [],
        },
        '4':{
            'score' : matchlist[3],
            'details' : matchdetails[3],
            'scorerlist' : [scorerlist[10],scorerlist[11],scorerlist[12]],
            'isPen' : False,
            'penscorers' : [],
        },
        '5':{
            'score' : matchlist[4],
            'details' : matchdetails[4],
            'scorerlist' : [scorerlist[13],scorerlist[14]],
            'isPen' : True,
            'penscorers' : [rightpenscorerslist[0],rightpenscorerslist[1],rightpenscorerslist[2],rightpenscorerslist[3],scorerlist[15],scorerlist[16],scorerlist[17],scorerlist[18]],
        },
        '6':{
            'score' : matchlist[5],
            'details' : matchdetails[5],
            'scorerlist' : [scorerlist[19],scorerlist[20],scorerlist[21],scorerlist[22],scorerlist[23]],
            'isPen' : False,
            'penscorers' : [],
        },
        '7':{
            'score' : matchlist[6],
            'details' : matchdetails[6],
            'scorerlist' : [],
            'isPen' : True,
            'penscorers' : [rightpenscorerslist[4],rightpenscorerslist[5],rightpenscorerslist[6],scorerlist[24],scorerlist[25],scorerlist[26],scorerlist[27]],
        },
        '8':{
            'score' : matchlist[7],
            'details' : matchdetails[7],
            'scorerlist' : [scorerlist[28],scorerlist[29],scorerlist[30],scorerlist[31],scorerlist[32]],
            'isPen' : False,
            'penscorers' : [],
        },
    }
    return round16Data