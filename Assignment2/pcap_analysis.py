from scapy.all import *

def pcap_analysis(filename):
    
    packets = rdpcap(filename)

    print("The total number of packets is {}.".format(len(packets)))

    conn = set()
    half_open_conn = set()
    closed_conn = set()

    get_count = 0
    post_count = 0
    tcp_count = 0
    udp_count = 0
    icmp_count = 0

    for packet in packets:

        if packet.haslayer(TCP):
            tcp_count+=1
        elif packet.haslayer(UDP):
            udp_count+=1
        elif packet.haslayer(ICMP):
            icmp_count += 1

        if packet.haslayer(TCP) and packet.haslayer(IP):

            src_ip = packet[IP].src
            dest_ip = packet[IP].dst
            src_port = packet[TCP].sport
            dest_port = packet[TCP].dport
            flags = packet[TCP].flags

            if flags & 0x02:
                conn.add((src_ip,dest_ip,src_port,dest_port))
            elif flags & 0x10 and (src_ip,dest_ip,src_port,dest_port) in conn:
                half_open_conn.add((src_ip,dest_ip,src_port,dest_port))
            elif flags & 0x01 and (src_ip,dest_ip,src_port,dest_port) in half_open_conn:
                half_open_conn.remove((src_ip,dest_ip,src_port,dest_port))
                closed_conn.add((src_ip,dest_ip,src_port,dest_port))

        if packet.haslayer(TCP) and packet.haslayer(Raw) and b'HTTP' in packet[Raw].load:

            method = packet[Raw].load.split()[0].decode('utf-8')
            if method == 'GET':
                get_count+=1
            elif method == 'POST':
                post_count+=1
            
            

    print("The number of icmp connections are {} and udp connections are {} and tcp connections are {}.".format(icmp_count,udp_count,tcp_count))
    print("Number of closed connections are {} and half-open connections are {}".format(len(half_open_conn),len(closed_conn)))
    print("Total number of connections is {}".format(len(conn)))
    print("The number of get requests are {} and post requests are {}.".format(get_count,post_count))




if __name__ == "__main__":

    filename = input("Enter the filename of the pcap file: ")
    if not os.path.isfile(filename):
        print("{} does not exist. Try again.".format(filename))
        filename = input("Enter the filename of the pcap file: ")

    pcap_analysis(filename)