from socket import *
import random
serverName='localhost'
serverPort=5000
clientSocket =socket(AF_INET, SOCK_DGRAM)
message="CONNECT"#"ClientName: NKC, Number: "+str(random.randint(1,100))#input('Input lowercase sentence:')
clientSocket.sendto(message.encode(),(serverName,serverPort))
modifiedMessage,serverAddress=clientSocket.recvfrom(1024)
print(modifiedMessage.decode())
clientSocket.close()
