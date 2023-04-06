import socket
import os

IP = socket.gethostbyname(socket.gethostname())
port = 501
addr = (IP,port)
size = 1024
format = "utf-8"

def getFolderFile(path):
    folders = []
    files = []
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file():
                files.append(entry.name)
            if entry.is_dir():
                folders.append(entry.name)
    return folders,files

def upload(conn,path):
    """This function is to send data from the client to the server."""

    conn.send("Enter the filename: ".encode(format))

    filename = conn.recv(size).decode(format)
    file = open(path+filename,"w")

    conn.send("Filename is received.".encode(format))

    data = conn.recv(size).decode(format)
    file.write(data)
    conn.send("File data is recieved.".encode(format))

    file.close()

def download(conn,path):
    """This function is to send the data from server to the client."""
    
    conn.send("Enter the filename: ".encode(format))

    filename = conn.recv(size).decode(format)
    file = open(path+filename,"r")

    conn.send("Filename is received.".encode(format))

    data = file.read()
    conn.send(data.encode(format))
    msg = conn.recv(size).decode(format)
    
    conn.send("File data transmitted.".encode(format))

    file.close()

if(__name__ == "__main__"):

    print("Server is starting.")

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(addr)
    server.listen()
    print("Server is listening.")

    while True:

        path = './'

        conn,addr = server.accept()
        print("New connection {} accepted.".format(addr))


        folders,files = getFolderFile(path)
        conn.send(f"{(folders,files)}".encode(format))

        choice,folder = eval(conn.recv(1024).decode(format))

        while True:
            if choice == 1:
                upload(conn,path)
                break
            elif choice == 2:
                download(conn,path)
                break
            elif choice == 3:
                path = path + f"{folder}/"
                folders,files = getFolderFile(path)
                conn.send(f"{(folders,files)}".encode(format))
                choice,folder = eval(conn.recv(1024).decode(format))

        conn.close()
        print("The connection {} is disconnected.".format(addr))