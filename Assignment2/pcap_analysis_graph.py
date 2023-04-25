from scapy.all import *
import networkx as nx
import matplotlib.pyplot as plt
import os


def pcap_analysis(filename):
    
    G = nx.Graph()

    pcap = rdpcap(filename)
    print(len(pcap))
    
    for packet in pcap:

        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dest_ip = packet[IP].dst
            G.add_edge(src_ip,dest_ip)

    nx.draw(G,with_labels=True)
    plt.show()


if __name__ == "__main__":

    filename = input("Enter the filename of the pcap file: ")
    if not os.path.isfile(filename):
        print("{} does not exist. Try again.".format(filename))
        filename = input("Enter the filename of the pcap file: ")

    pcap_analysis(filename)