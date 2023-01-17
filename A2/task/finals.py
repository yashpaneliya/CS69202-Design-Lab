import ply.yacc as yacc
import ply.lex as lex

matchlist = []
scorerlist = []
matchdetails = []
rightpenscorerslist = []

tokens = [
    "OPENFINAL",
    "CLOSEFINAL",
    "OPENMATCHDIV",
    "OPENPOINTTABLE",
    "CLOSEPOINTTABLE",
    "OPENTABLE",
    "OPENLIST",
    "CLOSELIST",
    "OPENROW",
    "CLOSEROW",
    "OPENDATA",
    "CLOSEDATA",
    "OPENHEADER",
    "CLOSEHEADER",
    "OPENHREF",
    "CLOSEHREF",
    "SEPARATOR",
    "CONTENT",
    "GARBAGE",
    "OPENLINK",
    "OPENABBR",
    "CLOSEABBR",
    "FRIGHTDIV",
]


def t_OPENFINAL(t):
    """<span\sclass="mw-headline"\sid="Final">Final</span>"""
    return t


def t_CLOSEFINAL(t):
    """<span\sclass="mw-headline"\sid="Statistics">Statistics</span>"""
    return t


# def t_OPENPOINTTABLE(t):
#     '''<table\sclass="wikitable"\sstyle="text-align:center;">'''
#     return t


def t_OPENTABLE(t):
    """<table\sclass="fevent">"""
    return t


def t_CLOSEPOINTTABLE(t):
    """</table>"""
    return t


def t_OPENMATCHDIV(t):
    """<div\sitemscope=""\sitemtype="http&\#58;//schema.org/SportsEvent"\sclass="footballbox">"""
    return t


def t_FRIGHTDIV(t):
    """<div\sclass="fright">"""
    return t


def t_SEPARATOR(t):
    """<link\srel="mw-deduplicated-inline-style"\shref="mw-data:TemplateStyles:r997937747"/>"""
    return t


def t_OPENROW(t):
    r"<tr.*?>"
    return t


def t_CLOSEROW(t):
    r"</tr>"
    return t


def t_OPENDATA(t):
    r"<td.*?>"
    return t


def t_CLOSEDATA(t):
    r"</td>"
    return t


def t_OPENLINK(t):
    r"<link.*?>"


def t_OPENABBR(t):
    r"<abbr.*?>"


def t_CLOSEABBR(t):
    r"</abbr>"


def t_OPENLIST(t):
    r"<li .*?>"
    return t


def t_CLOSELIST(t):
    r"</li>"
    return t


def t_OPENHREF(t):
    r"<a .*?>"
    return t


def t_CLOSEHREF(t):
    r"</a>"
    return t


def t_OPENHEADER(t):
    r"<th.*?>"
    return t


def t_CLOSEHEADER(t):
    r"</th>"
    return t


def t_CONTENT(t):
    r'[A-Za-z0-9ñáãćéíøäæóōúńÁÉÜÚÑğÓÍïüšëčýÿû,$#§&.+\-:;@ \'")\(–]+'
    return t


def t_GARBAGE(t):
    r"<.*?>"


def t_error(t):
    t.lexer.skip(1)


def p_start(p):
    """start : before OPENFINAL skip SEPARATOR handlematches CLOSEFINAL"""


def p_handlematches(p):
    """handlematches : skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches
    | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches
    | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails
    | skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF skip CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENHEADER CONTENT CLOSEHEADER OPENDATA handlepenscorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches
    | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF skip CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENHEADER CONTENT CLOSEHEADER OPENDATA handlepenscorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches
    | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF skip CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENHEADER CONTENT CLOSEHEADER OPENDATA handlepenscorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails
    |"""
    if len(p) > 1 and len(p) < 45:
        matchlist.append(p[7] + " " + p[13] + " " + p[19])
    elif len(p) > 45:
        matchlist.append(p[7] + " " + p[13] + " " + p[20])


def p_handlescorer(p):
    """handlescorer : skip OPENLIST OPENHREF CONTENT CLOSEHREF skip CLOSELIST handlescorer
    |"""
    if len(p) > 1:
        scorerlist.append(p[4])


def p_handlepenscorer(p):
    """handlepenscorer : skip OPENLIST CONTENT OPENHREF CONTENT CLOSEHREF skip CLOSELIST handlepenscorer
    |"""
    if len(p) > 1:
        rightpenscorerslist.append(p[5])


def p_handledetails(p):
    """handledetails : OPENHREF CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT OPENHREF CONTENT CLOSEHREF skip"""
    matchdetails.append(
        p[2] + " " + p[4] + " " + p[6] + " " + p[8] + " " + p[9] + " " + p[11]
    )


def p_before(p):
    """before : CONTENT before
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
    |"""


def p_skip(p):
    """skip : CONTENT skip
    | OPENHREF skip
    | CLOSEHREF skip
    |"""


def p_error(p):
    pass


def final():
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
    f = open("fifa.html", "r", encoding="utf-8")
    data = f.read()
    lexer.input(data)
    res = parser.parse(data)
    finalData = {
        "matchlist": matchlist,
        "1": {
            "score": matchlist[0],
            "details": matchdetails[0],
            "scorerlist": [scorerlist[0], scorerlist[1], scorerlist[2]],
            "isPen": True,
            "penscorers": [scorerlist[3],scorerlist[4],scorerlist[5],scorerlist[6],rightpenscorerslist[0],rightpenscorerslist[1],rightpenscorerslist[2],rightpenscorerslist[3]],
        },
    }
    f.close()
    return finalData

print(final())