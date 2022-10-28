import json

def call( ):

    address  = "1349 Mariposa "
    name = "John Chen"
    mtype = "RF"
    YEAR   = 2018
    date = 152323

    payload = { "found": "yes" , "address": address , "name" : name , "mtype": mtype , 'key' : date ,'year': YEAR}


#   print payload
    jds = json.dumps( payload , indent=12)

    return jds

def call1():

    address  = "1349 Yosemite Ave"
    name = "John Woo"
    mtype = "NRF"
    YEAR   = 2019
    date = 152323


    obj = []
    p1 = { "found": "yes" , "address": address , "name" : name , "mtype": mtype , 'key' : date ,'year': YEAR}
    p2 = { "found": "yes" , "address": address , "name" : name , "mtype": mtype , 'key' : date ,'year': YEAR}
    p3 = { "found": "yes" , "address": address , "name" : name , "mtype": mtype , 'key' : date ,'year': YEAR}
    obj.append(p1)
    obj.append(p2)
    obj.append(p3)

    j = json.dumps(obj, indent=24)
    return j

j = call()
print j

j = call1()
print j


