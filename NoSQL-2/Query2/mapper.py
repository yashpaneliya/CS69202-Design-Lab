import sys
import re

res_pattern = re.compile(r'\.(png|jpg|gif|ico|mp4|mp3|flv|html|css|js|php)*', re.IGNORECASE)

for line in sys.stdin:
    fields = line.strip().split()

    ip = fields[0]
    req_type = fields[5][1:]
    resource = fields[6]

    if res_pattern.search(resource):
        if req_type=='GET':
            print("%s\t%s"%(ip, resource))