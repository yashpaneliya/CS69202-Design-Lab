# Lex/Yacc assignment
# We need to download the Fifa wikipedia page
# For this we will use urllib library in python
# We will use 'Request'
#  
import os
from urllib.request import Request, urlopen
import ply.lex as lex
import ply.yacc as yacc

# We will use the following url to download the page
url = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup#Stadiums'

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
data = webpage.decode('utf-8')
f = open('fifa.html', 'w',encoding='utf-8')
f.write(data)
f.close()