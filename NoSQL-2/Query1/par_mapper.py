import sys
import re
import multiprocessing as mp
import time
image_regex = re.compile(r'\.(png|jpg|gif|ico)$', re.IGNORECASE)
video_regex = re.compile(r'\.(mp4|flv)$', re.IGNORECASE)
audio_regex = re.compile(r'\.(mp3)$', re.IGNORECASE)
web_regex = re.compile(r'\.(html|css|js|php)$', re.IGNORECASE)

def mapper(ifile, ofile):
    fi = open(ifile,'r')
    fo = open(ofile,'w')
    lines = fi.readlines()
    for line in lines:
        fields = line.strip().split()

        resource = fields[6]
        res_size = fields[9]

        if res_size == '-':
            res_size='0'

        try:
            if image_regex.search(resource):
                fo.write("img\t%s\n" % (res_size))
            elif video_regex.search(resource):
                fo.write("vid\t%s\n" % (res_size))
            elif audio_regex.search(resource):
                fo.write("aud\t%s\n" % (res_size))
            elif web_regex.search(resource):
                fo.write("web\t%s\n" % (res_size))
        except Exception as e:
            # Catch any exceptions that occur while searching for pattern and continue to the next iteration
            continue

def combiner(ifile, ofile):
    cur_type=None
    cur_size=0
    count=0
    fi = open(ifile,'r')
    fo = open(ofile,'w')
    lines = fi.readlines()
    lines.sort()
    for line in lines:
        fields = line.strip().split()
        if len(fields) < 2:
            continue

        res_type = fields[0]
        res_size = fields[1]
        
        if cur_type==None:
            cur_type=res_type
            cur_size=int(res_size)
            count=1
        elif cur_type!=res_type:
            fo.write("%s\t%s\t%s\n"%(cur_type,(cur_size),count))
            count=1
            cur_type=res_type
            cur_size=int(res_size)
        else:
            count+=1
            cur_size += int(res_size)

    fo.write("%s\t%s\t%s\n"%(cur_type,(cur_size),count))

def reducer(files):
    cur_type=None
    cur_size=0
    count=0

    result = open('par_result.txt','w')
    
    lines = []
    for file in files:
        f = open(file, 'r')
        flist = f.readlines()
        lines += flist
        f.close()

    lines.sort()
    
    for line in lines:
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
            result.write("%s\t%s\n"%(cur_type,round(cur_size/count,2)))
            count = int(res_count)
            cur_type = res_type
            cur_size = int(res_size)
        else:
            count += int(res_count)
            cur_size += int(res_size)
    result.write("%s\t%s\n"%(cur_type,round(cur_size/count,2)))

inputfiles = [
    'access_log1.txt',
    'access_log2.txt',
    'access_log3.txt',
    'access_log4.txt',
    'access_log5.txt',
    'access_log6.txt',
    'access_log7.txt',
    'access_log8.txt',
    'access_log9.txt',
    'access_log10.txt'
]

# 12 output files
outputfiles = [
    'token1.txt',
    'token2.txt',
    'token3.txt',
    'token4.txt',
    'token5.txt',
    'token6.txt',
    'token7.txt',
    'token8.txt',
    'token9.txt',
    'token10.txt'
]

# 12 aggregation files
aggfiles = [
    'agg1.txt',
    'agg2.txt',
    'agg3.txt',
    'agg4.txt',
    'agg5.txt',
    'agg6.txt',
    'agg7.txt',
    'agg8.txt',
    'agg9.txt',
    'agg10.txt'
]

starttime = time.time()
processes = [mp.Process(target=mapper, args=[inputfiles[i], outputfiles[i]]) for i in range(10)]

for p in processes:
    p.start()
for p in processes:
    p.join()

processes = [mp.Process(target=combiner, args=[outputfiles[i], aggfiles[i]]) for i in range(10)]

for p in processes:
    p.start()
for p in processes:
    p.join()

reducer(aggfiles)

print("Elapsed time (in seconds): ", (time.time() - starttime))