# THIS FILE CONTAINS THE TOKENS AND TOKENIZER CODE

import ply.lex as lex

# Write grammar tokens for web parsing the fifa.html file
tokens = [
    'BEGINTABLE', 'BEGINTEAMS',
    'OPENTABLE', 'CLOSETABLE', 'OPENROW', 'CLOSEROW',
    'OPENHEADER', 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF',
    'CONTENT', 'OPENDATA', 'CLOSEDATA' ,'OPENSPAN', 'OPENPARA', 'CLOSEPARA',
    'CLOSESPAN', 'OPENDIV', 'CLOSEDIV', 'OPENSTYLE', 'CLOSESTYLE','GARBAGE'
]

t_ignore = '\t'

###############Tokenizer Rules################
# <table class="wikitable sortable mw-collapsible mw-collapsed">


def t_BEGINTABLE(t):

    '''<h3><span\sclass="mw-headline"\sid="Stadiums">Stadiums</span></h3>'''

    return t

def t_BEGINTEAMS(t):
    '''<p><b>Team\sbase\scamps</b>'''
    return t


def t_OPENTABLE(t):
    '''<tbody[^>]*>'''
    return t

def t_CLOSETABLE(t):
    '''</tbody[^>]*>'''
    return t

def t_OPENROW(t):
    '''<tr[^>]*>'''
    return t

def t_CLOSEROW(t):
    '''</tr[^>]*>'''
    return t

def t_OPENHEADER(t):
    '''<th[^>]*>'''
    return t

def t_CLOSEHEADER(t):
    '''</th[^>]*>'''
    return t

def t_OPENHREF(t):
    '''<a[^>]*>'''
    return t

def t_CLOSEHREF(t):
    '''</a[^>]*>'''
    return t

def t_OPENDATA(t):
    '''<td[^>]*>'''
    return t

def t_CLOSEDATA(t):
    '''</td[^>]*>'''
    return t

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

def t_OPENSPAN(t):
    '''<span[^>]*>'''

def t_CLOSESPAN(t):
    '''</span[^>]*>'''

def t_OPENPARA(t):
    '''<p[^>]*>'''
    return t

def t_CLOSEPARA(t):
    '''</p[^>]*>'''
    return t

def t_GARBAGE(t):
    r'<[^>]*>'

def t_error(t):
    t.lexer.skip(1)

file_obj= open('./teams.html','r',encoding="utf8")
data=file_obj.read()
lexer = lex.lex()
lexer.input(data)
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
file_obj.close()