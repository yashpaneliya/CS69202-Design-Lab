import sys

cur_type=None
cur_size=0
count=0

for line in sys.stdin:
    fields = line.strip().split()
    if len(fields) < 3:
        continue
    res_type = fields[0]
    res_size = fields[1]
    res_count = fields[2]

    if cur_type == None:
        cur_type = res_type
        cur_size = int(res_size)
        count = int(res_count)
    elif cur_type != res_type:
        print("%s\t%s"%(cur_type,round(cur_size/count,2)))
        count = int(res_count)
        cur_type = res_type
        cur_size = int(res_size)
    else:
        count += int(res_count)
        cur_size += int(res_size)
print("%s\t%s" % (cur_type,round(cur_size/count,2)))
