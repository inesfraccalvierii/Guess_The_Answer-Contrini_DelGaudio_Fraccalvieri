#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 15:06:26 2021

@author: liviadelgaudio
"""

import tkinter as tk
import socket
from time import sleep
from random import randint
import threading
import Modulo_Domande as quest

your_name = ""
opponent_name = ""
game_round = 0
game_timer = 60
your_choice = 0
your_score = 0
opponent_score = 0
winner = ""
trap = False
questionA = ""
questionB = ""
answerA = randint(1,4)
answerB = answerA + 1

posFirstQuestion = randint(1,3)
print(posFirstQuestion)
defruolo = {1:"Indovino", 2:"Intellettuale", 3:"Storico"}
role = randint(1,3)


# client di rete
client = None
HOST_ADDR = '127.0.0.1'
HOST_PORT = 8080

#definizione dell'aspetto grafico: FINESTRA DI GIOCO PRINCIPALE
window_main = tk.Tk()
window_main.title("Guess the answer")
top_welcome_frame= tk.Frame(window_main)
lbl_name = tk.Label(top_welcome_frame, text = "Name:")
lbl_name.pack(side=tk.LEFT)
ent_name = tk.Entry(top_welcome_frame)
ent_name.pack(side=tk.LEFT)
btn_connect = tk.Button(top_welcome_frame, text="Connect", command=lambda : connect())
btn_connect.pack(side=tk.LEFT)
top_welcome_frame.pack(side=tk.TOP)

top_message_frame = tk.Frame(window_main)
lbl_line = tk.Label(top_message_frame, text="***********************************************************").pack()
lbl_welcome = tk.Label(top_message_frame, text="",font = "Helvetica 13")
lbl_welcome.pack()
lbl_line_server = tk.Label(top_message_frame, text="***********************************************************")
lbl_line_server.pack_forget()
top_message_frame.pack(side=tk.TOP)


top_frame = tk.Frame(window_main)
top_left_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
lbl_your_name = tk.Label(top_left_frame, text="Your name: " + your_name, font = "Helvetica 13 bold")
lbl_opponent_name = tk.Label(top_left_frame, text="Opponent: " + opponent_name)
lbl_score = tk.Label(top_left_frame, text="Your score is: " + str(your_score), font = "Helvetica 14 bold")
lbl_your_name.grid(row=0, column=0, padx=5, pady=8)
lbl_opponent_name.grid(row=1, column=0, padx=5, pady=8)
top_left_frame.pack(side=tk.LEFT, padx=(10, 10))


top_right_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
lbl_game_round = tk.Label(top_right_frame, text="Time left: ", foreground="blue", font = "Helvetica 14 bold")
lbl_timer = tk.Label(top_right_frame, text=" ", font = "Helvetica 24 bold", foreground="blue")
lbl_score = tk.Label(top_right_frame, text="Your score is: " + str(your_score), font = "Helvetica 14 bold")
lbl_score.grid(row=0, column=0)
lbl_game_round.grid(row=1, column=0, padx=5, pady=5)
lbl_timer.grid(row=2, column=0, padx=5, pady=5)
top_right_frame.pack(side=tk.RIGHT, padx=(10, 10))

top_frame.pack_forget()

middle_frame = tk.Frame(window_main)

lbl_line = tk.Label(middle_frame, text="***********************************************************").pack()
lbl_question = tk.Label(middle_frame, text="**** CHOOSE A QUESTION ****", font = "Helvetica 13 bold", foreground="blue").pack()
lbl_line = tk.Label(middle_frame, text="***********************************************************").pack()

round_frame = tk.Frame(middle_frame)
btn1 = tk.Button(round_frame, text=1, command=lambda : process(1), state=tk.NORMAL)
btn2 = tk.Button(round_frame, text=2, command=lambda : process(2), state=tk.NORMAL)
btn3 = tk.Button(round_frame, text=3, command=lambda : process(3), state=tk.NORMAL)    
btn1.grid(row=0, column=0)
btn2.grid(row=0, column=1)
btn3.grid(row=0, column=2)

round_frame.pack(side=tk.TOP)

final_frame = tk.Frame(middle_frame)
lbl_line = tk.Label(final_frame, text="***********************************************************").pack()
lbl_final_result = tk.Label(final_frame, text="**** WRITE YOUR ANSWER BELOW ****", font = "Helvetica 13 bold", foreground="blue")
lbl_final_result.pack()
lbl_line = tk.Label(final_frame, text="***********************************************************").pack()
final_frame.pack(side=tk.TOP)

middle_frame.pack_forget()
    

#funzione per definire il comportamento del gioco alla pressione di un dato tasto, 
#suddivisione in tre casi per assegnare domande coerenti con il ruolo stabilito
def process(i):
    global your_choice, posFirstQuestion, questionA, questionB, answerA, answerB
    your_choice = i
    lbl_final_result.config(foreground="blue")
    #caso indovino
    if role == 1:
        if i == posFirstQuestion:
            questionA = quest.IndovinoQuestions[answerA]
            lbl_final_result["text"] = "%s" %questionA
        elif i == posFirstQuestion+1 | i == posFirstQuestion-1:
            questionB = quest.IndovinoQuestions[answerB]
            lbl_final_result["text"] = "%s" %questionB
        else:
            trap()
    #caso intellettuale
    elif role == 2:
        if i == posFirstQuestion:
            questionA = quest.IntellettualeQuestions[answerA]
            lbl_final_result["text"] = "%s" %questionA
        elif i == posFirstQuestion+1 | i == posFirstQuestion-1:
            questionB = quest.IntellettualeQuestions[answerB]
            lbl_final_result["text"] = "%s" %questionB
        else:
            trap()
    #caso storico
    else:
        if i == posFirstQuestion:
            questionA = quest.StoricoQuestions[answerA]
            lbl_final_result["text"] = "%s" %questionA
        elif i == posFirstQuestion+1 | i == posFirstQuestion-1:
            questionB = quest.StoricoQuestions[answerB]
            lbl_final_result["text"] = "%s" %questionB
        else:
            trap()
    
    enable_disable_buttons("disable")
    

#funzione per il controllo sulla risposta inserita, suddiviso in tre casi in base al ruolo assegnato
def checkAnswer():
    global your_score, posFirstQuestion, answerA, answerB
    my_ans = my_answer.get()
    my_answer.set("")
    #caso indovino
    if role == 1:
        if your_choice == posFirstQuestion and my_ans == quest.IndovinoAnswers[answerA]:
                guess()
        elif (your_choice == posFirstQuestion + 1 or posFirstQuestion -1)  and my_ans == quest.IndovinoAnswers[answerB]:
            guess()
        else:
            not_guess()
    #caso intellettuale
    elif role == 2:
        if your_choice == posFirstQuestion and my_ans == quest.IntellettualeAnswers[answerA]:
            guess()
        elif (your_choice == posFirstQuestion + 1 or posFirstQuestion -1) and my_ans == quest.IntellettualeAnswers[answerB]:
            guess()
        else:
            not_guess()
   #caso storico
    else:
        if your_choice == posFirstQuestion and my_ans == quest.StoricoAnswers[answerA]:
            guess()
        elif (your_choice == posFirstQuestion + 1 or posFirstQuestion -1) and my_ans == quest.StoricoAnswers[answerB]:
            guess()
        else:
            not_guess()
    
    if(posFirstQuestion==3):
        posFirstQuestion=1
    posFirstQuestion = posFirstQuestion+1
    if answerA == 4:
        answerA = 1
        answerB = answerA + 1
    elif answerA == 3:
         answerA = answerA + 2
         answerB = 1
    else:
        answerA = answerA + 2
        answerB = answerA + 1
            

#impostazione della barra per l'inserimento delle risposte e del pulsante per il controllo,
#definizione dell'azione collegata a pressione del tasto (=checkAnswer())
my_answer = tk.StringVar()
button_frame = tk.Frame(window_main)
entry_Answer = tk.Entry(button_frame,textvariable = my_answer)
entry_Answer.bind("<Return>", checkAnswer)
entry_Answer.pack()
send_button = tk.Button(button_frame, text="Check", command=checkAnswer, state=tk.DISABLED)
send_button.pack()
button_frame.pack(side=tk.BOTTOM)


#funzione per gestire l'opzione trabocchetto
def trap():
    global trap, your_score
    enable_disable_buttons("disable")
    lbl_final_result["text"] = "THAT WAS A TRAP! YOU LOST THIS GAME \n you'll be disconnected soon"
    lbl_final_result.config(foreground="red")
    your_score = -100
    trap = True
    lbl_timer["text"] = str(0)

            
#funzione per gestione punteggio quando la risposta inserita è corretta (+1 punto)
def guess():
    global your_score
    your_score = your_score + 1
    lbl_final_result["text"] = "That's a guess!"
    lbl_final_result.config(foreground="green")
    enable_disable_buttons("enable")
    lbl_score["text"] = "Your score is: " + str(your_score)
    

#funzione per gestione punteggio quando la risposta inserita è errata (-1 punto)
def not_guess():
    global your_score
    your_score = your_score - 1
    lbl_final_result["text"] = "Unluckily, that wasn't correct..."
    lbl_final_result.config(foreground="red")
    enable_disable_buttons("enable")
    lbl_score["text"] = "Your score is: " + str(your_score)


#funzione per connessione al server (richiama connect_to_server())
def connect():
    global your_name
    if len(ent_name.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        your_name = ent_name.get()
        lbl_your_name["text"] = "Your name: " + your_name
        connect_to_server(your_name)
        

#funzione per abilitare e disabilitare i pulsanti 1,2,3
def enable_disable_buttons(todo):
    if todo == "disable":
        btn1.config(state=tk.DISABLED)
        btn2.config(state=tk.DISABLED)
        btn3.config(state=tk.DISABLED)
    else:
        btn1.config(state=tk.NORMAL)
        btn2.config(state=tk.NORMAL)
        btn3.config(state=tk.NORMAL)


#funzione per gestione timer
def count_down(my_timer, nothing):

    lbl_game_round["text"] = "Time left: "

    while (my_timer > 0) and trap != True:
        my_timer = my_timer - 1
        print("game timer is: " + str(my_timer))
        lbl_timer["text"] = str(my_timer)
        sleep(1)

    client.send(bytes("%i" %your_score, "utf8"))
    if trap != True:
        lbl_final_result["text"] = ""


def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR, your_name
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        client.send(name.encode()) # Invia il nome al server dopo la connessione

        # disable widgets
        btn_connect.config(state=tk.DISABLED)
        ent_name.config(state=tk.DISABLED)
        lbl_name.config(state=tk.DISABLED)
        enable_disable_buttons("enable")

        # avvia un thread per continuare a ricevere messaggi dal server
        # non bloccare il thread principale :)
        threading._start_new_thread(receive_message_from_server, (client, "m"))
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")


#funzione che si mette in ascolto per i vari messaggi provenienti dal server
def receive_message_from_server(sck, m):
    global your_name, opponent_name, game_round
    global your_choice, your_score, opponent_score
    msg = ""

    while True:
        if trap == True or my_answer == "{quit}":
            msg == "{quit}"
            client.send(bytes(msg, "utf8"))
            sck.close()
            window_main.quit()
            break

        from_server = sck.recv(4096)
        if not from_server: break
    
        #messaggio di benvenuto
        if from_server.startswith("welcome".encode()):
            if from_server == "welcome1".encode():
                lbl_welcome["text"] = "Server says: Welcome " + your_name + "! \nYour role is: %s\n" %defruolo[role] + "Waiting for player 2..."
            elif from_server == "welcome2".encode():
                lbl_welcome["text"] = "Server says: Welcome " + your_name + "!\nYour role is: %s\n" %defruolo[role] + "Game will start soon"
            lbl_line_server.pack()
    
        #ricezione nome avversario dal server
        elif from_server.startswith("opponent_name$".encode()):
            opponent_name = from_server.replace("opponent_name$".encode(), "".encode())
            lbl_opponent_name["text"] = "Opponent: " + opponent_name.decode()
            top_frame.pack()
            middle_frame.pack()
                
    
            # sappiamo che due utenti sono connessi, quindi il gioco è pronto per iniziare
            lbl_welcome["text"] = "Your role is: %s" %defruolo[role] 
            threading._start_new_thread(count_down, (game_timer, ""))
            send_button.config(state=tk.NORMAL)
            lbl_welcome.config(state=tk.DISABLED)
            lbl_line_server.config(state=tk.DISABLED)
    
        # ottieni il punteggio dell'avversario dal server
        else:
            opponent_score = from_server.decode("utf8")
            opponent_score = int(opponent_score)
    
            final_result = ""
            color = ""
               
            #gestione risultato trabocchetto
            if opponent_score == -100 and your_score == -100:
                final_result = "You and your opponent are trapped :("
            elif opponent_score == -100:
                final_result = "You won!!! Your opponent fell into a trap!"
                color = "green"
            #gestione risultato negli altri casi
            else:
                if your_score > opponent_score:
                    final_result = "You Won!!!"
                    color = "green"
                elif your_score == opponent_score:
                    final_result = "It's a Draw!!!"
                    color = "black"
                else:
                    final_result = "You Lost!!!"
                    color = "red"
    
       
            lbl_final_result["text"] = "FINAL RESULT: " + final_result
            lbl_final_result.config(foreground=color)
            sleep(5)
                
            enable_disable_buttons("disable")
            
    sck.close()
    window_main.quit()


window_main.mainloop()