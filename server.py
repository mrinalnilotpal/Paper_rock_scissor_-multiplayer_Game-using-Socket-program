import tkinter as tk                              #Python package for GUI.
import threading                                  # To make the program multitasking by doing operations simultaneously.
import socket                                     # socket is a python package for data communication and resource sharing.
from time import sleep                            # to use timing features


# We shall now turn our attention to the design of GUI and integrating functions in between. First we will design a window with a seperate blocks of code for top, middle and bottom portion design.

# In[43]:


# We are generating a window with the code below and the top part of it.

window = tk.Tk()
window.title("Server")

# We plan to provide two buttons on the top frame.
tpFram = tk.Frame(window)
btSt = tk.Button(tpFram, text="Start", command=lambda : stat_serv())
btSt.pack(side=tk.LEFT)
btStp = tk.Button(tpFram, text="Stop", command=lambda : stp_serv(), state=tk.DISABLED)
btStp.pack(side=tk.LEFT)
tpFram.pack(side=tk.TOP, pady=(5, 0))


# we will move to the middle frame design of the window.

# In[44]:


# Middle frame consisting of two labels for displaying the host and port info
mf = tk.Frame(window)
lablHost = tk.Label(mf, text = "Address: localhost")
lablHost.pack(side=tk.LEFT)
lablPort = tk.Label(mf, text = "Port:8085")
lablPort.pack(side=tk.LEFT)
mf.pack(side=tk.TOP, pady=(5, 0))


# we will now add client area which will be a background with slightly grey colour area. We are also adding scrollbar to show the indexing of the number of users.

# In[45]:


# The client frame shows the client area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=10, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))


# Next we move our focus to build two functions for servers to start and stop server.
# 1. stat_serv()
# 2. stp_serv()

# In[46]:


server = None

player_data = []
client_name = " "
clients = []
HST_ADR = '127.0.0.1'
HST_PRT = 4444
clients_names = []


# function to start the server.
def stat_serv():
    global server, HST_ADR, HST_PRT 
    
    btSt.config(state=tk.DISABLED)
    btStp.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print (socket.AF_INET)
    print (socket.SOCK_STREAM)

    server.bind((HST_ADR, HST_PRT))
    server.listen(5)  # server is listening for client connection

    threading._start_new_thread(accept_clients, (server, " "))

    lablHost["text"] = "Address: " + HST_ADR
    lablPort["text"] = "Port: " + str(HST_PRT)


# Function to stop the server.
def stp_serv():
    global server
    btSt.config(state=tk.NORMAL)
    btStp.config(state=tk.DISABLED)


# Now comes the central idea of the server model and with this we are directly entering into the core of Server model. Below we define two functions-
# 1. send_receive_client_message
# 2. accept_clients
# 
# These two functions gives us an intuitive picture of the working of socket package.

# In[47]:


# Function to accept clients
def accept_clients(the_server, y):
    while True:
        if len(clients) < 2:
            client, addr = the_server.accept()
            clients.append(client)

            # use a thread so as not to clog the gui thread
            threading._start_new_thread(send_receive_client_message, (client, addr))

# Function to receive message from current client AND
# Send that message to other clients
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, player_data, player0, player1

    client_msg = " "

    # send welcome message to client
    client_name = client_connection.recv(4096)
    if len(clients) < 2:
        client_connection.send("welcome1")
    else:
        client_connection.send("welcome2")

    clients_names.append(client_name)
    update_client_names_display(clients_names)  # update client names display

    if len(clients) > 1:
        sleep(1)

        # send opponent name
        clients[0].send("opponent_name$" + clients_names[1])
        clients[1].send("opponent_name$" + clients_names[0])
        # go to sleep

    while True:
        data = client_connection.recv(4096)
        if not data: break

        # get the player choice from received data
        player_choice = data[11:len(data)]

        msg = {
            "choice": player_choice,
            "socket": client_connection
        }

        if len(player_data) < 2:
            player_data.append(msg)

        if len(player_data) == 2:
            # send player 1 choice to player 2 and vice versa
            player_data[0].get("socket").send("$opponent_choice" + player_data[1].get("choice"))
            player_data[1].get("socket").send("$opponent_choice" + player_data[0].get("choice"))

            player_data = []

    # find the client index then remove from both lists(client name list and connection list)
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    client_connection.close()

    update_client_names_display(clients_names)  # update client names display


# In[48]:


# Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Update client name display when a new client connects OR
# When a connected client disconnects
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c+"\n")
    tkDisplay.config(state=tk.DISABLED)


window.mainloop()


# With the abouve code the window.mainloop() will run infinitely untill the user selects connect or halts the program manually. In the next part of this presentation we will explore the client model and see its working. 

# # End of Server program.

# In[ ]:




