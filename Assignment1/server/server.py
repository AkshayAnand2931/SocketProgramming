import socket

IP = "127.0.0.1"
port = 500
addr = (IP,port)
size = 1024
format = "utf-8"


def upload(conn):
    """This function is to send data from the client to the server."""

    conn.send("Enter the filename: ".encode(format))

    filename = conn.recv(size).decode(format)
    file = open(filename,"w")

    conn.send("Filename is received.".encode(format))

    data = conn.recv(size).decode(format)
    file.write(data)
    conn.send("File data is recieved.".encode(format))

    file.close()

def download(conn):
    """This function is to send the data from server to the client."""
    
    conn.send("Enter the filename: ".encode(format))

    filename = conn.recv(size).decode(format)
    file = open(filename,"r")

    conn.send("Filename is received.".encode(format))

    data = file.read()
    conn.send(data.encode(format))
    msg = conn.recv(size).decode(format)
    
    conn.send("File data transmitted.".encode(format))

if(__name__ == "__main__"):

    print("Server is starting.")

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(addr)
    server.listen()
    print("Server is listening.")

    while True:

        conn,addr = server.accept()
        print("New connection {} accepted.".format(addr))

        choice = conn.recv(size).decode(format)
        if choice == "1":
            upload(conn)
        elif choice == "2":
            download(conn)
        else:
            print("Invalid choice.")

        conn.close()
        print("The connection {} is disconnected.".format(addr))