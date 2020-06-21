#This code is written by Nilotpal Mrinal on 10-06-2020.

#code for server

#We will start with importing packages which is socket

import socket


ip=input("Enter Bind IP: ") #defining the ip for server.
port=int(input("Enter Port: ")) #defining the port for server.

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ip,port))

sock.listen(10)
conn,addr=sock.accept()
cou=0

 # Game logic begins from here.
while True:
    cou=cou+1
    ch=input("Enter Choice: ")
    conn.send(ch.encode())
    print("Waiting...")
    och=str(conn.recv(2048).decode())
    if(och==ch and och!="end" ):
        print("Draw")
    elif(och=='P' or och=='p'):
        if(ch=='S' or ch=='s'):
            print("Loose")
        elif(ch=='C' or ch=='c'):
            print("Win")
    elif(och=='C' or och=='c'):
        if(ch=='S' or ch=='s'):
            print("Win")
        elif(ch=='P' or ch=='p'):
            print("Loose")
    elif(och=='S' or och=='s'):
        if(ch=='P' or ch=='p'):
            print("Win")
        elif(ch=='C' or ch=='c'):
            print("Loose")
    else:
        print("Opponent Quit The Game.")
        break
            
    if(ch=="end"):
        conn.send("end".encode())
        print("You Quite The Game.")
        break

    print("--End Of Round "+str(cou)+"--")
    print("")
sock.close()
        
