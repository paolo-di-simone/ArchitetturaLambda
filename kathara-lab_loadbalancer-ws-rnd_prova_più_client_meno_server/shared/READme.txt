Flusso pacchetti-> si lancia dalle macchine client per inviare i pacchetti, python3 flusso...

dentro sniffing ci sono gli sniff l'unico che funziona è tcpdump.py , si lancia sul load balancer, si fa partire prima che partono gli script sui client.
python3 tcpdump.py > output.csv (esempio)

Ctrl-C su tutte le macchine per fermare gli script 

sui server ,quando sono in esecuzione gli script sui client e load balancer, ogni tanto esegui service apache2 stop e poi dopo un po start cosi che il flusso pacchetti è più vario

ho abbozzato codice map_reduce, spark core, spark sql 

cartella output ci sono degli output già calcolati quello con scritto finale senza prova è molto grande l'editor di testo  non te lo apre sono 600000 righe  

Qualsiasi cosa scrivi, spacca tutto con streaming, e se ti viene in mente qualche analisi batch suggerisci, prova streaming se riesci su amazon cosi ci risparmiamo di studiare storm e flume

ti voglio bene 

Filippo 

