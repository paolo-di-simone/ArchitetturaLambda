#!/usr/bin/env python3 

import sys
i=0
for line in sys.stdin:
    if(i==0):
        i+=1
        continue
    line = line.strip()
    packet = line.split(",")
    date = packet[0]
    time = packet[1]
    mac_dst= "mac_dst_" + str(packet[2])
    mac_src = "mac_src_" + str(packet[3])
    type = packet[4]

    try:
        proto = packet[5]
        ip_src = "ip_src_" + str(packet[6])
        ip_dst = "ip_dst_" + str(packet[7])
        sport= "sport_" + str(packet[8])
        dport = "dport_" + str(packet[9])
        flag_tcp = packet[10]
        try:    
            payload = packet[11]
            final_packet = str(time)+"-"+mac_dst+"-"+mac_src+"-"+str(type)+"-"+str(proto)+"-"+ip_src+"-"+ip_dst+"-"+sport+"-"+dport+"-"+str(flag_tcp)+"-"+str(payload)
        except IndexError:
         
            final_packet = str(time)+"-"+mac_dst+"-"+mac_src+"-"+str(type)+"-"+str(proto)+"-"+ip_src+"-"+ip_dst+"-"+sport+"-"+dport+"-"+str(flag_tcp)
          
    except:

       final_packet = str(time)+"-"+mac_dst+"-"+mac_src+"-"+str(type)
       
    
    
    
    print('%s\t%s'%(str(date),final_packet))


