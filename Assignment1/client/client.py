import socket

IP = "127.0.0.1"
port = 501
addr = (IP,port)
size = 1024
format = "utf-8"

def upload(client):
    """This function is used to send data from the client to the server."""
    
    client.send("1".encode(format))

    msg = client.recv(size).decode(format)
    print("SERVER: {}".format(msg))

    filename = input()
    client.send(filename.encode(format))

    msg = client.recv(size).decode(format)
    print("SERVER: {}".format(msg))

    file = open(filename,"r")
    data = file.read()

    client.send(data.encode(format))
    msg = client.recv(size).decode(format)
    print("SERVER: {}".format(msg))

    file.close()

def download(client):
    """This function is used to data from the server to the client."""

    client.send("2".encode(format))
    
    msg = client.recv(size).decode(format)
    print("SERVER: {}".format(msg))

    filename = input()
    client.send(filename.encode(format))

    msg = client.recv(size).decode(format)
    print("SERVER: {}".format(msg))

    file = open(filename,"w")
    data = client.recv(size).decode(format)
    file.write(data)
    file.close()

    client.send("File data transmitted.".encode(format))
    
    msg = client.recv(size).decode(format)
    print("SERVER: {}".format(msg))


if __name__ == "__main__":

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(addr)

    folders,files = eval(client.recv(1024).decode(format))
    print(folders,files)
    folder = None
    choice = 0
    while(choice != 1 and choice != 2):

        choice = int(input("Type 1 for uploading a file. Type 2 for downloading a file. Type 3 for going to another directory"))
        if choice == 1:
            upload(client)
            break
        elif choice == 2:
            download(client)
            break
        elif choice == 3:
            print("Here are the available folders. Type the  index value of the directory you wish to go to")
            for i,dir in enumerate(folders):
                print(f'{i}. {dir}')
            folder_index = input("Index: ")
            client.send(f'{(choice,folders[folder_index])}'.encode(format))
        else:
            print("Invalid choice.Try again")
    
    client.close()