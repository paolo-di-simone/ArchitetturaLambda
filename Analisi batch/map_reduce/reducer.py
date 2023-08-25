#!/usr/bin/env python3

import sys


def somma_valori_dizionario(dizionario):
    somma = 0
    for valore in dizionario.values():
        somma += valore
    return somma

pacchetti = {}

contatore = {}

dst_port = {}

src_port = {}

tempo={}

for line in sys.stdin:
 
     data,pacchetto = line.split("\t")
     pacchetto = pacchetto.split("-")
    
     time = pacchetto[0]
     ora = time[:2]
     mac_dst= pacchetto[1]
     mac_src = pacchetto[2]
     tipo = pacchetto[3]
          
     if(data not in pacchetti):
          pacchetti[data]={}
     
     #conta pacchetti per giorno
     if(data not in contatore):
          contatore[data]=0
     
     contatore[data]+=1

     #conta pacchetti in un ora
     if(ora not in tempo):
          tempo[ora] = 0
     
     tempo[ora] += 1

     #conta pacchetti mac_address destinazione
     if (mac_dst not in pacchetti[data]):
          pacchetti[data][mac_dst] = 0
    
     pacchetti[data][mac_dst] +=1

     #conta pacchetti mac_srogente
     if (mac_src not in pacchetti[data]):
          pacchetti[data][mac_src] = 0

     pacchetti[data][mac_src] +=1
      
     #conta pacchetti type
     if (tipo not in pacchetti[data]):
          pacchetti[data][tipo] = 0
     
     pacchetti[data][tipo] += 1
     
     
     if len(pacchetto) > 4: 

          proto = pacchetto[4]
          ip_src = pacchetto[5]
          ip_dst = pacchetto[6]
          sport= pacchetto[7]
          dport = pacchetto[8]
          flag_tcp = pacchetto[9]

          #conta pacchetti protocollo
          if (proto not in pacchetti[data]):
               pacchetti[data][proto] = 0
          
          pacchetti[data][proto] += 1

          #conta pacchetti ip_sorgente
          if (ip_src not in pacchetti[data]):
               pacchetti[data][ip_src] = 0
          
          pacchetti[data][ip_src] += 1

          #conta pacchetti ip_destinazione
          if (ip_dst not in pacchetti[data]):
               pacchetti[data][ip_dst] = 0
          
          pacchetti[data][ip_dst] += 1

          #conta pacchetti porta sorgente
          if(data not in src_port):
               src_port[data]={}

          if (sport not in src_port[data]):
               src_port[data][sport] = 0
          
          src_port[data][sport] += 1

          #conta pacchettu porta destinazione
          if(data not in dst_port):
               dst_port[data]={}

          if (dport not in dst_port[data]):
               dst_port[data][dport] = 0
          
          dst_port[data][dport] += 1

          #conta pacchetti flag tcp
          if (flag_tcp not in pacchetti[data]):
               pacchetti[data][flag_tcp] = 0
          
          pacchetti[data][flag_tcp] += 1

#---------------------------------------TOP 5 porte--------------------------------------------------#

for k,v in src_port.items():
    sorted_word_count = sorted(v.items(),
                           key=lambda item: item[1],
                           reverse=True)

    ordered_dict = {k: v for k, v in sorted_word_count}
    src_port[k] = ordered_dict


for k,v in dst_port.items():
     sorted_word_count = sorted(v.items(),
                           key=lambda item: item[1],
                           reverse=True)

     ordered_dict = {k: v for k, v in sorted_word_count}
     dst_port[k] = ordered_dict


for k in src_port:
     list = []
     i=0
     for v in src_port[k]:
          list.append((v,src_port[k][v]))
          i+=1
          if(i==5):
               break

     src_port[k] = list



for k in dst_port:
     list = []
     i=0
     for v in dst_port[k]:
          list.append((v,dst_port[k][v]))
          i+=1
          if(i==5):
               break

     dst_port[k] = list


#---------------------------------------------------------------------------------------------------------#


for key in pacchetti:
     output = ""
     for elem in pacchetti[key]:
          output += str(elem)+": "+str(pacchetti[key][elem]) + " "   
     for k in tempo:
          time += str(k)+": "+str(tempo[k])+" "

     print( time+" "+str(key) + " "+str(contatore[key])+" "+str(somma_valori_dizionario(contatore)//len(contatore))+" "+str(src_port[key])
            +" "+ str(dst_port[key]) +" "+output)

     