from socket import *
import random
import threading
import time
serverPort = 6000
serverSocket=socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('',serverPort))
print('The Server is ready to recieve')
clients={}

def listenToRequests():
    while True:
        message, clientAddress = serverSocket.recvfrom(1024)
        if(message.decode().upper()=="CONNECT"):
            clients[clientAddress]="active"
            modifiedMessage="You are added "+str(clientAddress)
            serverSocket.sendto(modifiedMessage.encode(),clientAddress)
        else:
            clients[clientAddress]="inactive"
            modifiedMessage="You are removed "+str(clientAddress)
            serverSocket.sendto(modifiedMessage.encode(),clientAddress)
   
def listenPeriodic(ip,port):
    
    try:
        serverSocket.settimeout(1)
        message, clientAddress = serverSocket.recvfrom(1024)
        if(message.decode().upper()=="CONNECT"):
            clients[clientAddress]="active"
            modifiedMessage="You are alive "+str(clientAddress)
            serverSocket.sendto(modifiedMessage.encode(),clientAddress)
        else:
            clients[clientAddress]="inactive"
    except:
        clients[(ip,port)]="inactive"
        

            
def broadcastactives():
    while True:
        acline=filter(lambda x:clients[x]=="active",clients.keys())
        
        for i in acline:
            print("*",i[0],i[1],"*\n")
            serverSocket.sendto("|".join(acline).encode(),i)
            client_p_thread = threading.Thread(target=listenPeriodic,args=(i[0],i[1]))
            client_p_thread.start() 
            time.sleep(1)
            
        time.sleep(5)
                     
if __name__ == "__main__":
    client_l_thread = threading.Thread(target=listenToRequests)
    client_a_thread = threading.Thread(target=broadcastactives)
    client_l_thread.start()
    # starting thread 2
    client_a_thread.start()
 
    # wait until thread 1 is completely executed
    client_l_thread.join()
    # wait until thread 2 is completely executed
    client_a_thread.join()
 
    # both threads completely executed
    print("Done!")