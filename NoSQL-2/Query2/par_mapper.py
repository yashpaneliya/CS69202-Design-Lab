import sys
import re
import multiprocessing as mp
import time

def mapper(ifile, ofile):
    res_pattern = re.compile(r'\.(png|jpg|gif|ico|mp4|mp3|flv|html|css|js|php)*', re.IGNORECASE)
    fi = open(ifile,'r')
    fo = open(ofile,'w')
    lines = fi.readlines()
    for line in lines:
        fields = line.strip().split()
        # extracting ip and the resource
        ip = fields[0]
        req_type = fields[5][1:]
        resource = fields[6]
        # print only if there is a resource and it's a GET request
        if res_pattern.search(resource):
            if req_type=='GET':
                fo.write("%s\t%s\n"%(ip, resource))

def combiner(ifile, ofile):
    fi = open(ifile,'r')
    fo = open(ofile,'w')
    lines = fi.readlines()

    res_dict = {}

    for line in lines:
        fields = line.strip().split("\t")

        if len(fields) < 2:
            continue
            
        ip, resource = fields[0], fields[1]

        if ip not in res_dict.keys():
            res_dict[ip] = set()
        
        res_dict[ip].add(resource)

    for key, resources in res_dict.items():
        fo.write('%s\t%s\n' % (key, ','.join(resources)))

def reducer(files):
    result = open('par_result.txt','w')
    
    lines = []
    for file in files:
        f = open(file, 'r')
        flist = f.readlines()
        lines += flist
        f.close()

    # dictionary to store {ip : resourceList}
    network_dict = {}

    for line in lines:
        fields = line.strip().split("\t")

        if len(fields) < 2:
            continue 

        ip, resource = fields[0], fields[1]
        # storing the resources requested by an ip in a set inside a dictionary
        if ip not in network_dict:
            network_dict[ip] = set()
            reslist = resource.split(",")
            for res in reslist:
                network_dict[ip].add(res)
        else:
            reslist = resource.split(",")
            for res in reslist:
                network_dict[ip].add(res)

    # function to count number of connected components in the network
    def connected_comps(ip_resource_dict):
        # dictionary to store {resource : ipList}
        network = {}
        # Iterating over network_dict to generate network graph
        for ip, resources in ip_resource_dict.items():
            for resource in resources:
                if resource not in network:
                    network[resource] = set()
                network[resource].add(ip)

        # variables to store unique resources
        key1 = set()
        key2 = set()

        for resource in network.keys():
            key1.add(resource)
            key2.add(resource)
        
        for k1 in key1:
            for k2 in key2:
                # if the resource is still there in dictionary
                if k1!=k2 and (k2 in network.keys()) and (k1 in network.keys()):
                    iplist1 = network[k1]
                    iplist2 = network[k2]
                    flag = False
                    # check intersection between two lists of ips of two different resources
                    for ip1 in iplist1:
                        for ip2 in iplist2:
                            if ip1==ip2:
                                flag=True
                                break
                        if flag==True:
                            break
                    # If intersection found, merge the two lists into one list to make connected component
                    if flag==True:
                        for ip in iplist2:
                            network[k1].add(ip)
                        # remove the old list from dictionary
                        network.pop(k2)
        return network

    con_comp = connected_comps(network_dict)
    # variable to count disconnected pairs
    discon_pairs = 0
    # list to record size of iplists
    sizes = []

    for res, li in con_comp.items():
        sizes.append(len(li))

    for i, s in enumerate(sizes):
        for j, s2 in enumerate(sizes):
            if j > i:
                discon_pairs += s*s2

    result.write(str(discon_pairs))

inputfiles = [
    'access_log11.txt',
    'access_log12.txt'
]

# 2 output files
outputfiles = [
    'token1.txt',
    'token2.txt'
]

# 2 aggregation files
aggfiles = [
    'agg1.txt',
    'agg2.txt'
]

starttime = time.time()

processes = [mp.Process(target=mapper, args=[inputfiles[i], outputfiles[i]]) for i in range(2)]

for p in processes:
    p.start()
for p in processes:
    p.join()

processes = [mp.Process(target=combiner, args=[outputfiles[i], aggfiles[i]]) for i in range(2)]

for p in processes:
    p.start()
for p in processes:
    p.join()

reducer(aggfiles)

print("Elapsed time (in seconds): ", (time.time() - starttime))