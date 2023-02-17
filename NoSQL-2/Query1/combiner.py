import sys

cur_type=None
cur_size=0
count=0

for line in sys.stdin:
    fields = line.strip().split("\t")
    # wf = open('combined.txt','a')
    # print(fields)
    if len(fields) < 2:
        continue

    res_type = fields[0]
    res_size = fields[1]
    
    if cur_type==None:
        cur_type=res_type
        cur_size=int(res_size)
        count=1
    elif cur_type!=res_type:
        print("%s\t%s\t%s"%(cur_type,(cur_size),count))
        count=1
        cur_type=res_type
        cur_size=int(res_size)
    else:
        count+=1
        cur_size += int(res_size)

print("%s\t%s\t%s"%(cur_type,(cur_size),count))
