#This is both client and server combined

import os
import socket
from random import randint
#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.connect(("8.8.8.8", 80))
#SERVER_TCP_IP = str(s.getsockname()[0])
#s.close()

SERVER_TCP_IP = "192.168.0.19"
    
SERVER_TCP_IP = ""
TCP_IP = ""
TCP_PORT = 2014
BUFFER_SIZE = 2048
decision = 0

#Local user stats
username = ""
hp = 100
level = 1
xptonext = 500
money = 100
attack = randint(5, 12)
defence = randint(1, 4)
speed = randint(1, 10)

#Opponent stats
opponentUsername = ""
opponentHp = 0
opponentLevel = 0
opponentAttack = 0
opponentDefence = 0
opponentSpeed = 0

#Processes received commands on server side
def serverProcess(data, hp, level, xptonext, money, attack, defence, speed, opponentUsername, opponentHp, opponentLevel, opponentAttack, opponentDefence, opponentSpeed):
    cmd = data.split(" ")
    if cmd[0] == "attack":
        hp = hp - opponentAttack
        print "You lost " + str(opponentAttack) + " hp."
        conn.send(str(opponentAttack))
        #raw_input()
        serverMain(data, hp, level, xptonext, money, attack, defence, speed, opponentUsername, opponentHp, opponentLevel, opponentAttack, opponentDefence, opponentSpeed)

#Processes received commands on client side
def clientProcess(data, hp, level, xptonext, money, attack, defence, speed, opponentUsername, opponentHp, opponentLevel, opponentAttack, opponentDefence, opponentSpeed):
    cmd = data.split(" ")
    if cmd[0] == "attack":
        hp = hp - opponentAttack
        print "You lost " + str(opponentAttack) + " hp."
        s.send(str(opponentAttack))
        #raw_input()
        clientMain(data, hp, level, xptonext, money, attack, defence, speed, opponentUsername, opponentHp, opponentLevel, opponentAttack, opponentDefence, opponentSpeed)

#Main loop for client. Displays vars and asks for command.
def clientMain(data, hp, level, xptonext, money, attack, defence, speed, opponentUsername, opponentHp, opponentLevel, opponentAttack, opponentDefence, opponentSpeed):
    #os.system("cls")
    print "Username:" + username + " HP:" + str(hp) + " Level:" + str(level) + " Attack:" + str(attack) + " Defence:" + str(defence) + " Speed:" + str(speed)
    print "Opponent:" + opponentUsername + " HP:" + str(opponentHp) + " Level:" + str(opponentLevel) + " Attack:" + str(opponentAttack) + " Defence:" + str(opponentDefence) + " Speed:" + str(opponentSpeed)
    print "Your turn."
    action = raw_input(">")
    cmd = action.split(" ")
    
    if action == "help":
        print "Later."
        null = raw_input()
    elif cmd[0] == "attack":
        s.send(action)
        data = s.recv(BUFFER_SIZE)
        opponentHp = opponentHp - int(data)
        clientWait(data, hp, level, xptonext, money, attack, defence, speed, opponentUsername, opponentHp, opponentLevel, opponentAttack, opponentDefence, opponentSpeed)

#Same as clientMain
def serverMain(data, hp, level, xptonext, money, attack, defence, speed, opponentUsername, opponentHp, opponentLevel, opponentAttack, opponentDefence, opponentSpeed):
    print "Your turn"
    #raw_input()
    #os.system("cls")
    print "Username:" + username + " HP:" + str(hp) + " Level:" + str(level) + " Attack:" + str(attack) + " Defence:" + str(defence) + " Speed:" + str(speed)
    print "Opponent:" + opponentUsername + " HP:" + str(opponentHp) + " Level:" + str(opponentLevel) + " Attack:" + str(opponentAttack) + " Defence:" + str(opponentDefence) + " Speed:" + str(opponentSpeed)
    print "Your turn."
    action = raw_input(">")
    #Splits command which allows for more detailed commands 
    cmd = action.split(" ")
    
    if action == "help":
        print "Later."
        null = raw_input()
        main()
    elif cmd[0] == "attack":
        conn.send(action)
        data = conn.recv(BUFFER_SIZE)
        opponentHp = opponentHp - int(data)
        serverWait(data, hp, level, xptonext, money, attack, defence, speed, opponentUsername, opponentHp, opponentLevel, opponentAttack, opponentDefence, opponentSpeed)

#Waits for client data(command to process). This section, as well as clientMain have bug.
def serverWait(data, hp, level, xptonext, money, attack, defence, speed, opponentUsername, opponentHp, opponentLevel, opponentAttack, opponentDefence, opponentSpeed):
    print "Not your turn."
    #raw_input()
    #os.system("cls")
    print "Username:" + username + " HP:" + str(hp) + " Level:" + str(level) + " Attack:" + str(attack) + " Defence:" + str(defence) + " Speed:" + str(speed)
    print "Opponent:" + opponentUsername + " HP:" + str(opponentHp) + " Level:" + str(opponentLevel) + " Attack:" + str(opponentAttack) + " Defence:" + str(opponentDefence) + " Speed:" + str(opponentSpeed)
    data = conn.recv(BUFFER_SIZE)
    serverProcess(data, hp, level, xptonext, money, attack, defence, speed, opponentUsername, opponentHp, opponentLevel, opponentAttack, opponentDefence, opponentSpeed)

#Same as serverWait. When user presses enter on wait, both clients crash or hang.
def clientWait(data, hp, level, xptonext, money, attack, defence, speed, opponentUsername, opponentHp, opponentLevel, opponentAttack, opponentDefence, opponentSpeed):
    print "Not your turn."
    #raw_input()
    #os.system("cls")
    print "Username:" + username + " HP:" + str(hp) + " Level:" + str(level) + " Attack:" + str(attack) + " Defence:" + str(defence) + " Speed:" + str(speed)
    print "Opponent:" + opponentUsername + " HP:" + str(opponentHp) + " Level:" + str(opponentLevel) + " Attack:" + str(opponentAttack) + " Defence:" + str(opponentDefence) + " Speed:" + str(opponentSpeed)
    data = s.recv(BUFFER_SIZE)
    clientProcess(data, hp, level, xptonext, money, attack, defence, speed, opponentUsername, opponentHp, opponentLevel, opponentAttack, opponentDefence, opponentSpeed)

#Inits server
def server():
    #Makes socket global so it can be used in other functions
    global s
    #Creates socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Binds to serverIp
    s.bind(("192.168.0.19", TCP_PORT))
    #Listens for clients (100)
    s.listen(100)
    print "Waiting for the opponent(s)"
    global conn, addr
    #Accepts client
    conn, addr = s.accept()
    #Following 7 lines sends and receives username and stats between each other in turns.
    conn.send(username)
    opponentUsername = conn.recv(BUFFER_SIZE)
    print opponentUsername
    conn.send(str(hp) + " " + str(level) + " " + str(attack) + " " + str(defence) + " " + str(speed))
    data = conn.recv(BUFFER_SIZE)
    status = conn.recv(BUFFER_SIZE)
    print opponentUsername + " has raised their fists against you. Fuck the greetings, time for them to get rekt."
    #Splits stats into array for easy handling
    data = data.split(" ")
    opponentHp = int(data[0])
    opponentLevel = int(data[1])
    opponentAttack = int(data[2])
    opponentDefence = int(data[3])
    opponentSpeed = int(data[4])
    #Client handles who starts first, this just receives the results.
    if status == "wait":
        serverWait(data, hp, level, xptonext, money, attack, defence, speed, opponentUsername, opponentHp, opponentLevel, opponentAttack, opponentDefence, opponentSpeed)
    elif status == "done":
        serverMain(data, hp, level, xptonext, money, attack, defence, speed, opponentUsername, opponentHp, opponentLevel, opponentAttack, opponentDefence, opponentSpeed)
    else:
        print status
        print "Error: Incorrect data."

#Init for client
def client():
    print "Enter server IP."
    TCP_IP = raw_input(">")
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    opponentUsername = s.recv(BUFFER_SIZE)
    s.send(username)
    data = s.recv(BUFFER_SIZE)
    s.send(str(hp) + " " + str(level) + " " + str(attack) + " " + str(defence) + " " + str(speed))
    print opponentUsername + " has scoweled at your fists. No one scowls at you, so fuck it, time for them to get rekt."
    data = data.split(" ")
    opponentHp = int(data[0])
    opponentLevel = int(data[1])
    opponentAttack = int(data[2])
    opponentDefence = int(data[3])
    opponentSpeed = int(data[4])
    #Checks which of the players speed is greater, and tells server
    if speed > opponentSpeed:
        s.send("wait")
        clientMain(data, hp, level, xptonext, money, attack, defence, speed, opponentUsername, opponentHp, opponentLevel, opponentAttack, opponentDefence, opponentSpeed)
    else:
        s.send("done")
        clientWait(data, hp, level, xptonext, money, attack, defence, speed, opponentUsername, opponentHp, opponentLevel, opponentAttack, opponentDefence, opponentSpeed)


print "Please enter your username."
username = raw_input(">")
os.system("cls")
print "Server(1) or Client(0)?"
decision = raw_input(">")
os.system("cls")
if decision == "1":
    server()
elif decision == "0":
    client()
else:
    print "Please pick an option"
    
