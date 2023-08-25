import os
from scapy.all import IP,UDP,ICMP, send

contatore = 0 
while(True):
# Run the curl command and capture the output
    if(contatore % 7 == 0):
        ip_packet = IP(dst="100.0.0.2")
        udp_packet = UDP(dport=80)
        packet = ip_packet / udp_packet
        send(packet)
        contatore+=1
        continue
    
    if(contatore % 10 == 0):
        ip_packet = IP(dst="100.0.0.2")
        icmp_packet = ICMP()
        packet = ip_packet / icmp_packet
        send(packet)
        contatore+=1
        continue

    curl_command = 'curl http://100.0.0.2/'
    html_content = os.popen(curl_command).read()
    contatore+=1

# Print or further process the captured HTML content
#print(html_content)
