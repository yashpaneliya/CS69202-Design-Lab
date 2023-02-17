import sys

# dictionary to store {ip : resourceList}
network_dict = {}

for line in sys.stdin:
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

print(discon_pairs)




# visited = set()
# count = 0
# for ip in ip_resource_dict.keys():
#     if ip not in visited:
#         stack = [ip]
#         while stack:
#             current = stack.pop()
#             visited.add(current)
#             for resource in ip_resource_dict[current]:
#                 for connected_ip in network[resource]:
#                     if connected_ip not in visited:
#                         stack.append(connected_ip)
#         count += 1
# return count

# for i, cur_resource in enumerate(network):
#         ip_list = network[cur_resource]
#         # print("i:",i)
#         for j, resource in enumerate(network):
#             if j > i:
#                 # print("j: ",j)
#                 res_ip_list = network[resource]
#                 # flag to check for connected IP
#                 flag = False
#                 for cur_ip in ip_list:
#                     for ip in res_ip_list:
#                         if cur_ip==ip:
#                             # print(cur_ip," " ,ip)
#                             break
#                     if f     flag=True
#                        lag==True:
#                         break
#                 if flag==False:
#                     count+=1