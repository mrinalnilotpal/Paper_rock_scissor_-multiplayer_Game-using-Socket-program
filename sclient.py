#This code is written by Nilotpal Mrinal on 10-06-2020.
# This code is the second half and denotes the codes for client.

#We will start with importing packages.
import socket
# code for client

ip=input("Enter Server IP: ") # Taking the input server ip add.
port=int(input("Enter Port: ")) # taking port number input.


sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)#Starting the conection
sock.connect((ip,port))

cou=0; # counter for number of times game played.

while True:
    
    cou=cou+1
    ch=input("Enter Choice: ")
    sock.send(ch.encode())
    
    print("Waiting...")
    och=str(sock.recv(2048).decode())

    # Game logic begins from here.
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
        break;


    if(ch=="end"):
        sock.send("end".encode())
        print("You Quite The Game.")
        break
    print("--End Of Round "+str(cou)+"--")
    print("")

sock.close()
