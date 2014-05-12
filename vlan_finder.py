#!/usr/bin/env python

import pyodbc
from netaddr import *

vlanList = {}
connectionString = ""

def findVlan(mac):
    try:
        #http://www.tryolabs.com/Blog/2012/06/25/connecting-sql-server-database-python-under-ubuntu/
        con = pyodbc.connect(connectionString)
        cursor = con.cursor()
        cursor.execute("select ipaddress from dbo.zNetworkAddress where MacAddress='%s'"%mac)
        result = cursor.fetchone()
        if result:
            ip = IPAddress(result[0])
            for s, v in vlanList.items():
                if ip in s:
                    return [v]
        return set(vlanList.values())        
    except:
        print "ERROR"
        print sys.exc_info()[0]
        return set(vlanList.values())
    finally:
        con.close()    
    

with open("vlans.txt") as f:
    for l in f.readlines():
        v, s = l.split("\t")
        vlanList[IPNetwork(s.strip())] = int(v)

with open("connectionstring.txt") as f:
    connectionString = f.read()
    
