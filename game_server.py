#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 15:05:35 2021

@author: liviadelgaudio
"""

import tkinter as tk
import socket
import threading
from time import sleep


window = tk.Tk()
window.title("Server")

# Cornice superiore composta da due pulsanti (i.e. btnStart, btnStop)
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Start", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

# Cornice centrale composta da due etichette per la visualizzazione delle informazioni sull'host e sulla porta
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Address: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# Il frame client mostra l'area dove sono elencati i clients che partecipano al gioco
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=10, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))


server = None
HOST_ADDR = '127.0.0.1'
HOST_PORT = 8080
client_name = " "
clients = []
clients_names = []
player_data = []


# Avvia la funzione server
def start_server():
    global server, HOST_ADDR, HOST_PORT
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print (socket.AF_INET)
    print (socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)  # il server Ã¨ in ascolto per la connessione del client

    threading._start_new_thread(accept_clients, (server, " "))

    lblHost["text"] = "Address: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)


# Arresta la funzione server
def stop_server():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)


def accept_clients(the_server, y):
    while True:
        if len(clients) < 2:
            client, addr = the_server.accept()
            clients.append(client)

            # utilizza un thread in modo da non intasare il thread della gui
            threading._start_new_thread(send_receive_client_message, (client, addr))

# Funzione per ricevere messaggi dal client corrente E
# Invia quel messaggio agli altri client
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, player_data, player0, player1

    client_msg = " "

    # invia un messaggio di benvenuto al client
    client_name = client_connection.recv(4096)
    if len(clients) < 2:
        client_connection.send("welcome1".encode())
    else:
        client_connection.send("welcome2".encode())

    clients_names.append(client_name)
    update_client_names_display(clients_names)  # aggiornare la visualizzazione dei nomi dei client

    if len(clients) > 1:
        sleep(1)

        # invia il nome dell'avversario
        clients[0].send(("opponent_name$" + clients_names[1].decode()).encode())
        clients[1].send(("opponent_name$" + clients_names[0].decode()).encode())
        
        # rimane in attesa
    while True:
        data = client_connection.recv(4096)
        if not data: break
        
        #gestione situazione in cui il client ha scelto l'opzione trap
        if data == bytes("{quit}", "utf8"): break
            
        else:
            # estrae il punteggio del giocatore dai dati ricevuti
    
            msg = {
                "score": data,
                "socket": client_connection
            }
            
    
            if len(player_data) < 2:
                player_data.append(msg)
    
            if len(player_data) == 2:
                #decodifica dei messaggi arrivati
                msg0 = player_data[1].get("score")
                msg1 = player_data[0].get("score")
                msg0 = int(msg0)
                msg1 = int(msg1)
                
                try:
                # invia la scelta del giocatore 1 al giocatore 2 e viceversa
                    player_data[0].get("socket").send(bytes("%i" %msg0, "utf8"))
                    player_data[1].get("socket").send(bytes("%i" %msg1, "utf8"))
                except OSError:
                    break
                
                player_data = []
            
        

    # trova l'indice del client, quindi lo rimuove da entrambi gli elenchi (elenco dei nomi dei client e elenco delle connessioni)
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    client_connection.close()

    update_client_names_display(clients_names)  # aggiorna la visualizzazione dei nomi dei client


# Restituisce l'indice del client corrente nell'elenco dei client
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Aggiorna la visualizzazione del nome del client quando un nuovo client si connette O
# Quando un client connesso si disconnette
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c.decode()+"\n")
    tkDisplay.config(state=tk.DISABLED)


window.mainloop()