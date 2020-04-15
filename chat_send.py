'''
chat area:
to akhon ekdom basic python diye communication korbo ok
accha, sock_stream? likhechi oi line tai dekh, IPv4 ta ki? Internet protocol 192.168.0.1 ei IP standard taa hocche IPv4 aar ekta ache IPv6 message gulo enter mere likhis nahole onek side e hoye jacche
accha
save korli''' 

import socket #ei library tai tor network socket diye communication r jonne pre-installed
#ekta keyboard setting thik korchilam
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.AF_INET mane socket theke AF_INET use korchi eta protocal INET mane IPv4, tarpor SOCK_STREAM mane socket e streaming allow korlam aar 's' taa amader socket taa

s.bind((socket.gethostname(),1234)) #gethostname provides the local ip of the pc and 1234 is the port I specified to be used
s.listen(5) #ebar ei socket taa communication r jonno listen kora start korche max 5 taa alada connection possible '5' r mane

while True:
    clientsocket, address = s.accept() #jodi conno connection ase or clientsocket aar address taa left r variable guloi store hoye jabe
    print("Connection established")
    clientsocket.send(bytes("Welcome to the server!", "utf-8")) #send mane to bujhechis bracket bhetorer jinis taa client ke pathache bytes diye string taa ke binary te conevrt kore pathachi

#ei code taa ke tor documents\vscode e save kore ne
#diye bolis