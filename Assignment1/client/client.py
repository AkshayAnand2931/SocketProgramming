import socket

port = 501
size = 1024
format = "utf-8"


def upload(client):
    """This function is used to send data from the client to the server."""

    client.send(f"{(1,folder)}".encode(format))

    msg = client.recv(size).decode(format)
    print("SERVER: {}".format(msg))

    filename = input()
    client.send(filename.encode(format))

    msg = client.recv(size).decode(format)
    print("SERVER: {}".format(msg))

    file = open(filename, "r")
    data = file.read()

    client.send(data.encode(format))
    msg = client.recv(size).decode(format)
    print("SERVER: {}".format(msg))

    file.close()


def download(client):
    """This function is used to data from the server to the client."""

    client.send(f"{(2,folder)}".encode(format))

    msg = client.recv(size).decode(format)
    print("SERVER: {}".format(msg))

    filename = input()
    client.send(filename.encode(format))

    msg = client.recv(size).decode(format)
    print("SERVER: {}".format(msg))

    file = open(filename, "w")
    data = client.recv(size).decode(format)
    file.write(data)
    file.close()

    client.send("File data transmitted.".encode(format))

    msg = client.recv(size).decode(format)
    print("SERVER: {}".format(msg))


if __name__ == "__main__":

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = input("Enter the server IP address:")
    addr = (IP, port)
    client.connect(addr)

    folder = None
    choice = 0
    while (choice != 1 and choice != 2):

        folders, files = eval(client.recv(1024).decode(format))
        if len(files) == 0:
            print("There are no files in the folder.")
        else:
            print("The files available in the following folder is: ")
            for i, dir in enumerate(files):
                print(f'{i}. {dir}')
        print()
        if len(folders) == 0:
            print("There are no folders in the directory.")
        else:
            print("The folders available in the following folder is: ")
            for i, dir in enumerate(folders):
                print(f'{i}. {dir}')
        print()
        choice = int(input("Type 1 for uploading a file. Type 2 for downloading a file. Type 3 for going to another directory"))

        if choice == 1:
            upload(client)
            break
        elif choice == 2:
            download(client)
            break
        elif choice == 3:
            if len(folders) == 0:
                print("There are no folders to go to. Please try again.")
                continue

            print("Here are the available folders. Type the  index value of the directory you wish to go to (Type -1 for going out of the directory)")

            for i, dir in enumerate(folders):
                print(f'{i}. {dir}')
            print()

            folder_index = int(input("Index: "))
            if folder_index == -1:
                client.send(f'{(choice,"None")}'.encode(format))
            else:
                client.send(f'{(choice,folders[folder_index])}'.encode(format))

        else:
            print("Invalid choice.Try again")

    client.close()
