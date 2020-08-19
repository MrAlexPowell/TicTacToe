"""
This test has a 3x3 board, winner gets 3 in a row
For practice, opponent is random. After 100 practice, plays me 3 times
Then practices again.
"""

from time import time
from random import randint

#Function that creates options for choices array
def expand(choices,old,n1,n2):
    for i in range(n1*n2):
        past = old+str(i)
        if(unique(past)):
            p = unfinished(past,n1,n2)
            if(p==0):
                choices.append([past,.5])
            else:
                choices.append([past,1.0])

#Function that determines if all inputs are unique
def unique(past):
    bad = False
    for j in past:
        if(past.count(j)>1):
            bad=True
    if(not bad):
        return True
    else:
        return False

#Function that determines if board is complete or not
def unfinished(past,n1,n2):
    p1 = []
    p2 = []
    for i in range(len(past)):
        p1.append(int(past[i])) if i%2==0 else p2.append(int(past[i]))

    #Begin normal sort, determine if elements are in a row
    p1.sort()
    p2.sort()
    for i in range(len(p1)-2):
        if(p1[i+2]-p1[i]==2):
            if(p1[i+2]//n1==p1[i]//n1):
                return 1
    for i in range(len(p2)-2):
        if(p2[i+2]-p2[i]==2):
            if(p2[i+2]//n1==p2[i]//n1):
                return 2

    #Custom sort by which column it is in, determine if same columns
    col = (lambda x:x%3)

    p1.sort(key=col)
    for i in range(len(p1)-2):
        if(col(p1[i+2])==col(p1[i])):
            if(p1[i+2]-p1[i]==(2*n1)):
                return 1
    p2.sort(key=col)
    for i in range(len(p2)-2):
        if(col(p2[i+2])==col(p2[i])):
            if(p2[i+2]-p2[i]==(2*n1)):
                return 2

    #Custom sort by diagonals it is in, determine if same down right diagonal
    dia1 = (lambda x, n=n1:(x%(n+1)))

    p1.sort()
    p1.sort(key=dia1)
    for i in range(len(p1)-2):
        if(dia1(p1[i+2])==dia1(p1[i])):
            if(col(p1[i+2])-col(p1[i])==2):
                if((p1[i+2]//n1)-(p1[i]//n1)==2):
                    return 1
    p2.sort()
    p2.sort(key=dia1)
    for i in range(len(p2)-2):
        if(dia1(p2[i+2])==dia1(p2[i])):
            if(col(p2[i+2])-col(p2[i])==2):
                if((p2[i+2]//n1)-(p2[i]//n1)==2):
                    return 2

    #Determine if elements are in the same down left diagonal
    dia2 = (lambda x, n=n1:(x%(n-1)))

    p1.sort()
    p1.sort(key=dia2)
    for i in range(len(p1)-2):
        if(dia2(p1[i+2])==dia2(p1[i])):
            if(col(p1[i]-col(p1[i+2])==2)):
                if((p1[i+2]//n1)-(p1[i]//n1)==2):
                    return 1
    p2.sort()
    p2.sort(key=dia2)
    for i in range(len(p2)-2):
        if(dia2(p2[i+2])==dia2(p2[i])):
            if(col(p2[i]-col(p2[i+2])==2)):
                if((p2[i+2]//n1)-(p2[i]//n1)==2):
                    return 1
    return 0

#Function that writes choices array to file
def save(choices):
    choices.sort(key=lambda x:(len(x[0]),x[0]))
    f = open("array.txt","w+")
    for i in choices:
        f.write(i[0])
        f.write("\n")
        f.write(str(i[1]))
        f.write("\n")
    f.close()

#Function that prints board given path string
def board(layout,n1,n2):
    p1 = []
    p2 = []
    for i in range(len(layout)):
        p1.append(int(layout[i])) if i%2==0 else p2.append(int(layout[i]))
    n=0
    print()
    for i in range(n1):
        print(" ",end="")
        for j in range(n2):
            if(n in p1):
                print("X",end="")
            elif(n in p2):
                print("O",end="")
            else:
                print(n+1,end="")
            n=n+1
            if(j<n2-1):
                print(" | ",end="")
        print(" ")
        if(i<n1-1):
            for j in range(n2*4-1):
                print("-",end="")
        print()

#Function that allows CPU to play against itself
def run(choices,n1,n2):
    p=randint(1,4)
    p-=3
    if(p<1):
        p=2
    pathA=[]
    pathB=[]
    path=""
    while(unfinished(path,n1,n2)==0 and len(path)<9):
        if(p==1):
            pathA.append(0)
            options=[]
            done = False
            for i in range(len(choices)):
                if(len(choices[i][0])>len(path)+1):
                    break
                elif(len(choices[i][0])==len(path)+1):
                    if(choices[i][0].find(path)==0):
                        done = True
                        options.append(i)
                    else:
                        if(done==True):
                            break
            best = 0
            for i in options:
                if(choices[i][1]>best):
                    best = choices[i][1]
                    pathA[-1] = i
            path += choices[int(pathA[-1])][0][-1]
        else:
            if(len(path)==0):
                path += str(randint(0,n1*n2-1))
                for i in range(len(choices)):
                    if(choices[i][0]==path):
                        pathB.append(i)
                        break
            else:
                pathB.append(0)
                options=[]
                done = False
                for i in range(len(choices)):
                    if(len(choices[i][0])>len(path)+1):
                        break
                    elif(len(choices[i][0])==len(path)+1):
                        if(choices[i][0].find(path)==0):
                            done = True
                            options.append(i)
                        else:
                            if(done==True):
                                break
                best = 0
                for i in options:
                    if(choices[i][1]>best):
                        best = choices[i][1]
                        pathB[-1] = i
                path += choices[int(pathB[-1])][0][-1]
        p2 = p
        p=(p+1,p-1)[p==2]
    if(unfinished(path,n1,n2)==0):
        winner(pathB,pathA,choices,True)
    else:
        if(p2==2):
            winner(pathB,pathA,choices)
        else:
            winner(pathA,pathB,choices)

#Function that edits array based on winner
def winner(winner,loser,choices,tie=False):
    factor = (lambda x:x*3)
    n=.001
    n2=-.001
    if(tie):
        factor = (lambda x:x*1.5)
        n=-.0005
        n2=-.0005
    for i in winner:
        temp=float(choices[i][1])+n
        n=factor(n)
        if(temp>1):
            temp=.999
        if(temp<=0):
            temp=.001
        choices[i][1]=temp
    for i in loser:
        temp=float(choices[i][1])+n2
        n2=factor(n2)
        if(temp>1):
            temp=.999
        if(temp<=0):
            temp=.001
        choices[i][1]=temp

#Function that allows user to play against CPU
def play(choices,player,n1,n2):
    p = player
    path = ""
    pathA = []
    pathB = []
    while(unfinished(path,n1,n2)==0 and len(path)<9):
        board(path,n1,n2)
        if(p==2):
            pathA.append(0)
            options=[]
            done = False
            for i in range(len(choices)):
                if(len(choices[i][0])>len(path)+1):
                    break
                elif(len(choices[i][0])==len(path)+1):
                    if(choices[i][0].find(path)==0):
                        done = 1
                        options.append(i)
                    else:
                        if(done==True):
                            break
            best = 0
            for i in options:
                if(choices[i][1]>best):
                    best = choices[i][1]
                    pathA[-1] = i
            path += choices[int(pathA[-1])][0][-1]
            print("\nI choose space '"+str(int(path[-1])+1)+"'.\n")
        else:
            poss = "012345678"
            print("\nMr. Powell, choose a space.\n>>> ",end="")
            chosen = input()
            while(str(int(chosen)-1) not in poss or str(int(chosen)-1) in path):
                print("Invalid selection...\nEnter available number (1-"+str(n1*n2)+")\n>>> ",end="")
                chosen = input()
            path += str(int(chosen)-1)
            for i in range(len(choices)):
                if(choices[i][0]==path):
                    pathB.append(i)
                    break
        p2 = p
        p=(p+1,p-1)[p==2]
    board(path,n1,n2)
    if(unfinished(path,n1,n2)==0):
        print("\nTie Game.")
        winner(pathB,pathA,choices,True)
    else:
        if(p2==1):
            print("\nCongrats, you won.")
            winner(pathB,pathA,choices)
        else:
            print("\nHahaha, you dumb piece of human garbage, you suck.")
            winner(pathA,pathB,choices)



#_______________________Main Program _________________________
start = time()
choices = []

f = open("array.txt","a+")
f.close()
f = open("array.txt","r")
if f.mode == 'r':
    f1 = f.readlines()
    for i in range(len(f1)//2):
        choices.append([f1[2*i][:-1],(float(f1[2*i+1]))])
f.close()

#Part where it creates the array and file if needed
n1=3
n2=3
k = n1*n2
total = 1
while(k>0):
    total=total*k
    k-=1

if(len(choices)<5):
    print("Detected new workspace.\nWelcome to my TicTacToe simulation (v1.6), courtesy of TechnoCore!")
    print("\nCreating memory map...\n(This may take approximately 30 seconds)\n")
    choices = [["",.5]]
    for k in range(n1*n2):
        for i in choices:
            if(len(i[0])==k and i[1]==.5):
                expand(choices,i[0],n1,n2)
            elif(len(i[0])>k):
                break
    save(choices)
    print("Setup complete.\n")
else:
    print("Welcome back to TicTacToe (v1.6) by TechnoCore, Mr. Powell!")

#Part where we choose to play the game or let it practice
good = True
print("Would you like to play? (Y) or (N)\n>>> ",end="")
playing = input()
first = True
while(good):
    if(playing.lower()=="y"):
        if(first):
            print("\nAlright, let's play!")
        first = False
        print("\nHow many players are gonna play? (\"Q\" to Quit)\n>>> ",end="")
        players = input()
        good2 = True
        while(good2):
            good3=False
            if(players=="1"):
                print("\nWould you like to be player (1) or player (2)?\n>>> ",end="")
                player = "None"
                while(player !="1" and player !="2"):
                    player = input()
                    if(player=="1"):
                        print("\nOkay, you can select your space first.")
                        play(choices,1,n1,n2)
                        good3=True
                        break
                    elif(player=="2"):
                        print("\nOkay, I will go first.")
                        play(choices,2,n1,n2)
                        good3=True
                        break
                    else:
                        print("\nHmmm... that wasn't right.\nEnter \"1\" or \"2\" to make a choice\n>>> ",end="")
            elif(players=="2"):
                p=1
                path = ""
                pathA=[]
                pathB=[]
                poss = "012345678"
                while(unfinished(path,n1,n2)==0 and len(path)<9):
                    board(path,n1,n2)
                    print("\nPlayer",str(p)+", choose a space.\n>>> ",end="")
                    chosen = input()
                    while(str(int(chosen)-1) not in poss or str(int(chosen)-1) in path):
                        print("Invalid selection...\nEnter available number (1-"+str(n1*n2)+")\n>>> ",end="")
                        chosen = input()
                    path = path+str(int(chosen)-1)
                    if(p==1):
                        for i in range(len(choices)):
                            if(choices[i][0]==path):
                                pathA.append(i)
                                break
                    else:
                        for i in range(len(choices)):
                            if(choices[i][0]==path):
                                pathB.append(i)
                                break
                    p2 = p
                    p=(p+1,p-1)[p==2]
                if(unfinished(path,n1,n2)==0):
                    print("\nTie Game.")
                    winner(pathB,pathA,choices,True)
                else:
                    winner(pathB,pathA,choices) if (p2==2) else winner(pathA,pathB,choices)
                board(path,n1,n2)
                print("\nPlayer",p2,"won.")
                good3=True
            elif(players=="0"):
                print("\nOoh I see... you want to take things up a notch...\nYou have accessed the hidden practice menu.\n\nHow many times should I play by myself?\nFor best results, run 500-2000 times (Time:45s-4m)\n>>> ",end="")
                times = -1
                while(int(times)<0):
                    times = input()
                    try:
                        times = int(times)
                    except:
                        print("\nHmmm... that wasn't right.\nEnter a number greater than 0\n>>> ",end="")
                        times = -1
                print("Running",times,"times...")
                stime = time()
                percent = 1
                for i in range(times):
                    run(choices,n1,n2)
                    if(int((i/times)*100)>percent and percent<=100):
                        print(str(percent-1)+"%")
                        percent=int((i/times)*100)+4
                good2=False
                print("Completed in "+str(time()-stime)[:5]+" seconds...")
            elif(players.lower()=="q"):
                playing="n"
                break
            else:
                print("\nHmmm... that wasn't right.\nEnter \"1\" or \"2\" to make a choice\n>>> ",end="")
                players=input()
            if(good==False):
                break
            if(good3):
                print("\nAgain? (Y) or (N) or (H)ome\n>>> ",end="")
                again = "None"
                while(again.lower()!="y" and again.lower()!="n" and again.lower()!="h"):
                    again=input()
                    if(again.lower()=="y"):
                        print("\nReplaying game.")
                    elif(again.lower()=="n"):
                        good=False
                        good2=False
                    elif(again.lower()=="h"):
                        print("Going to home menu.")
                        good2=False
                    else:
                        print("\nHmmm... that wasn't right.\nEnter \"y\" or \"n\" to make a choice\n>>> ",end="")
    elif(playing.lower()=="n"):
        good = False
    else:
        print("\nHmmm... that wasn't right.\nEnter \"y\" or \"n\" to make a choice\n>>> ",end="")
        playing = input()
print("\nExiting game... do not turn off the console...")
save(choices)
print("Exited.")
