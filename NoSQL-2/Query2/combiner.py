import sys

current_ip = None
current_resources = []

res_dict = {}

for line in sys.stdin:
    fields = line.strip().split("\t")

    if len(fields) < 2:
        continue
        
    ip, resource = fields[0], fields[1]

    if ip not in res_dict.keys():
        res_dict[ip] = set()
    
    res_dict[ip].add(resource)

for key, resources in res_dict.items():
    print('%s\t%s' % (key, ','.join(resources)))

#     if current_ip != ip:
#         if current_ip is not None:
#             print('%s\t%s' % (current_ip, ','.join(current_resources)))

#         current_ip = ip
#         current_resources = []

#     if resource not in current_resources:
#         current_resources.append(resource)

# if current_ip is not None:
#     print('%s\t%s' % (current_ip, ','.join(current_resources)))
