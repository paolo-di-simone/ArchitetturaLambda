from scapy.all import sniff
from scapy.layers.inet import IP 
from scapy.layers.inet import TCP
from scapy.layers.inet import Ether
from scapy.layers.inet import UDP
from scapy.packet import * 
import time
import datetime

def get_timestamp():
    timestamp = str(datetime.datetime.now()).replace(" ", ",")
    return timestamp



def packet_handler(packet):
    timestamp = get_timestamp()
    mac_dst = packet[Ether].dst
    mac_src = packet[Ether].src
    type = packet[Ether].type
    try:
        ip_version = packet[IP].version
        ihl = packet[IP].ihl
        tos = packet[IP].tos
        len = packet[IP].len
        id = packet[IP].id
        flags = packet[IP].flags
        frag= packet[IP].frag
        ttl = packet[IP].ttl
        proto = packet[IP].proto
        checksum = packet[IP].chksum
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        
        if(proto ==17):
            sport = packet[UDP].sport
            dport = packet[UDP].dport
            output = str(timestamp)+","+str(mac_dst)+","+str(mac_src)+","+str(type)+","+str(ip_version)+","+str(ihl)+","+str(tos)+","+str(len)+","+str(id)+","+str(flags)+","+str(frag)+","+str(ttl)+","+str(proto)+","+str(checksum)+","+str(ip_src)+","+str(ip_dst)+","+str(sport)+","+str(dport)
            output = output.replace(" ", "")
            print(output)
        
        elif(proto == 1):
            output = str(timestamp)+","+str(mac_dst)+","+str(mac_src)+","+str(type)+","+str(ip_version)+","+str(ihl)+","+str(tos)+","+str(len)+","+str(id)+","+str(flags)+","+str(frag)+","+str(ttl)+","+str(proto)+","+str(checksum)+","+str(ip_src)+","+str(ip_dst)
            output = output.replace(" ", "")
            print(output)
             
        else:
            sport = packet[TCP].sport
            dport = packet[TCP].dport
            sequence = packet[TCP].seq
            ack = packet[TCP].ack
            flag_tcp = packet[TCP].flags
            dataofs  = packet[TCP].dataofs
            window = packet[TCP].window

            try:
                payload = packet[Raw].load
                output = str(timestamp)+","+str(mac_dst)+","+str(mac_src)+","+str(type)+","+str(ip_version)+","+str(ihl)+","+str(tos)+","+str(len)+","+str(id)+","+str(flags)+","+str(frag)+","+str(ttl)+","+str(proto)+","+str(checksum)+","+str(ip_src)+","+str(ip_dst)+","+str(sport)+","+str(dport)+","+str(sequence)+","+str(ack)+","+str(flag_tcp)+","+str(dataofs)+","+str(window)+","+str(payload)
                output = output.replace(" ", "")
                print(output)
            #file.write(output+"\n")
            #print(mac_dst,",", mac_src,",",type,",",ip_version,",",ihl,",",tos,",",len,",",id,",",flags,",",frag,",",ttl,",",proto,",",checksum,",",ip_src,",",ip_dst,",",sport,",",dport,",",options,",",payload)
        
            except IndexError:
                output = str(timestamp)+","+str(mac_dst)+","+str(mac_src)+","+str(type)+","+str(ip_version)+","+str(ihl)+","+str(tos)+","+str(len)+","+str(id)+","+str(flags)+","+str(frag)+","+str(ttl)+","+str(proto)+","+str(checksum)+","+str(ip_src)+","+str(ip_dst)+","+str(sport)+","+str(dport)+","+str(sequence)+","+str(ack)+","+str(flag_tcp)+","+str(dataofs)+","+str(window)
                output = output.replace(" ", "")
                print(output)
            #file.write(output+"\n")
            #print(ip_version,ihl,tos,len,id,flags,frag,ttl,proto,checksum,ip_src,ip_dst,sport,dport,options)



   
    except IndexError:
       output=str(timestamp)+","+str(mac_dst)+","+str(mac_src)+","+str(type)
       output = output.replace(" ", "")
       print(output)
       #file.write(output+"\n")
    
    

   


if __name__ == "__main__":

    #with open("output_file.txt", "a") as file:
    sniff(iface=["eth0","eth1"], prn=packet_handler)
    #sniff(iface=["eth0","eth1"], prn= lambda packet: packet_handler(packet file))


