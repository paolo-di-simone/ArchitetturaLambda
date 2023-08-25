import subprocess
from scapy.all import IP, TCP, Raw, send


def stop_apache2():
    try:
        subprocess.run(["service", "apache2", "stop"], check=True)
        print("Apache2 stopped.")
    except subprocess.CalledProcessError as e:
        print("Error stopping Apache2:", e)



def send_http_503_packet():
    src_port = 12345  # Source port for the TCP connection
    dst_port = 80  # Destination port for HTTP
    seq_num = 1000  # Sequence number
    ack_num = 0     # Acknowledgment number
    
    # Craft the HTTP 503 response packet
    ip_packet = IP(dst="100.0.0.10")
    tcp_packet = TCP(sport=src_port, dport=dst_port, flags="FA", seq=seq_num, ack=ack_num)
    http_data = (
        b"HTTP/1.1 503 Service Unavailable\r\n"
        b"Content-Length: 0\r\n"
        b"\r\n"
    )
    
    packet = ip_packet / tcp_packet / Raw(load=http_data)
    send(packet)
    print("HTTP 503 packet sent.")

if __name__ == "__main__":
     # Change this to the target IP address
    stop_apache2()
    while(True):
        send_http_503_packet()
