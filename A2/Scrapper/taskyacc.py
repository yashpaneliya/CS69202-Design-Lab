# THIS FILE CONTAINS THE GRAMMAR RULES
# ALSO THE DRIVER CODE WHICH READS FIFA.HTML AND RETURNS THE STADIUM TABLE DATA

import ply.yacc as yacc

from tokentask import tokens

def p_start(p):
    '''start : table'''
    p[0] = p[1]

def p_name(p):
    '''name : CONTENT
            | CONTENT name'''
    if len(p) == 3:
        p[0] = p[1]+ ' '+ p[2]
    else:
        p[0] = p[1]

def p_skiptag(p):
    '''skiptag : CONTENT skiptag
                | OPENHREF skiptag
                | CLOSEHREF skiptag
                |'''

# 1st rule::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# <td> OPENDATA
#         <a
#           href="/wiki/Khalifa_International_Stadium"
#           title="Khalifa International Stadium"
#           >  OPENHREF
#           CONTENT => Khalifa International Stadium
#         </a> CLOSEHREF
# </td> CLOSEDATA
# .....remaining td tags <= handledata

# 2nd rule:
# <td> OPENDATA
#    skiptag----->
#    (In skip tag it will take 45032 as CONTENT and remaing stuff will recurse again on skiptag)
#      45,032
#           <sup id="cite_ref-95" class="reference"
#           ><a href="#cite_note-95">&#91;88&#93;</a></sup
#         ><sup id="cite_ref-96" class="reference"
#           ><a href="#cite_note-96">&#91;89&#93;</a></sup
#         ><sup id="cite_ref-97" class="reference"
#           ><a href="#cite_note-97">&#91;H&#93;</a></sup
#         >
# </td> CLOSEDATA
# ... remaining td tags <= handledata
def p_handleData(p):
    '''handledata : OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA handledata
                  | OPENDATA skiptag CLOSEDATA handledata
                  | '''
    if len(p)==7:
        print(p[3])


# 1st rule::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# <tr> OPENROW
#      OPENHEADER <th class="unsortable"> skiptag->City </th> CLOSEHEADER
#       <th>Stadium</th>
#       <th>Capacity</th>
# </tr> CLOSEROW
# ...recusrsion on same variable to scan code after </tr> of headings for remaining rows... <= handlerow

# 2nd rule::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# <tr> OPENROW
#       <th> OPENHEADER
#            OPENHREF  <a href="/wiki/Lusail" title="Lusail">
#            CONTENT =>      Lusail
#            CLOSEHREF  </a>
#       </th> CLOSEHEADER
#       
# handledata--->
#       <td>
#         <a href="/wiki/Lusail_Stadium" title="Lusail Stadium">Lusail Stadium</a>
#       </td>
#       <td>
#         88,966<sup id="cite_ref-86" class="reference"
#           ><a href="#cite_note-86">&#91;82&#93;</a></sup
#         ><sup id="cite_ref-87" class="reference"
#           ><a href="#cite_note-87">&#91;83&#93;</a></sup
#         ><sup id="cite_ref-88" class="reference"
#           ><a href="#cite_note-88">&#91;E&#93;</a></sup
#         >
#       </td>
# </tr> CLOSEROW
# .... remaining rows using recursion <-- handlerow

# 3rd rule::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# <tr> OPENROW
# handledata------>
#       <td>
#         <a href="/wiki/Ahmad_bin_Ali_Stadium" title="Ahmad bin Ali Stadium"
#           >Ahmad bin Ali Stadium</a
#         >
#       </td>
#       <td>
#         45,032<sup id="cite_ref-95" class="reference"
#           ><a href="#cite_note-95">&#91;88&#93;</a></sup
#         ><sup id="cite_ref-96" class="reference"
#           ><a href="#cite_note-96">&#91;89&#93;</a></sup
#         ><sup id="cite_ref-97" class="reference"
#           ><a href="#cite_note-97">&#91;H&#93;</a></sup
#         >
#       </td>
# </tr> CLOSEROW
# ....remaining rows using recursion <= handlerow
def p_handleRow(p):
    '''handlerow : OPENROW OPENHEADER skiptag CLOSEHEADER OPENHEADER skiptag CLOSEHEADER OPENHEADER skiptag CLOSEHEADER CLOSEROW handlerow
                | OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER handledata CLOSEROW handlerow
                | OPENROW handledata CLOSEROW handlerow
                |'''

def p_table(p):
    '''table : BEGINTABLE skiptag OPENTABLE handlerow'''

def p_empty(p):
    '''empty : '''
    pass

def p_content(p):
    '''content : CONTENT
                | empty'''
    p[0] = p[1]

def p_error(p):
    pass

parser = yacc.yacc()

if __name__ == '__main__':
    f=open('fifa.html','r',encoding='utf-8')
    data = f.read()
    res = parser.parse(data)
    print(res)
    f.close()