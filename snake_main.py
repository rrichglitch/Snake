from random import random
from tkinter import *

#set the size of board no less than 10
size = 17
#initialize the board
board =[[0]*size for i in range(size)]
empty = []
root = Tk()
restart = Button(root, text='start', padx=5, pady=5)
scoreB = Label(root, text='score: 0')
#repeatable setup
def start():
    #initialize score
    global scor
    scor=0
    #root is tkinter window
    global board
    #filling the board in window and matrix
    for x in range(size):
        for y in range(size):
            board[x][y]=Button(root, text='    ', padx=5, pady=5, state=DISABLED)
            board[x][y].grid(column=x, row=y)
    global scoreB
    scoreB['text']='score: '+str(scor)
    scoreB.grid(column=int(size/2)+1,row=size,columnspan=5)

    restart.grid(column=int(size/2)-4,row=size,columnspan=4)
    #save orginal button color
    global orig_col
    orig_col=restart['bg']
    #initialize array containing IDs for snake segments
    global body
    body=[[int(size/2)+1,int(size/2)],[int(size/2),int(size/2)]]
    global empty
    for i in range(1,size*size+1):
        for seg in body:
            if [(i-1)/size,(i-1)%size]!=seg:
                empty.append([int((i-1)/size),(i-1)%size])
    global dir
    dir="right"
    place_food()
    root.bind("<KeyPress>", keydown)

restart['command']=start


#randomly place food in random empty location
def place_food():
    i=empty[int(random()*len(empty))]
    # print(i)
    board[i[0]][i[1]]['bg'] = "green"

def gen_move():
    for seg in range(body.__len__()-2,-1,-1):
        body[seg+1]=list(body[seg])

# moving the body
def move():
    if dir=="right":
        gen_move()
        body[0][0]+=1
        # print(body)
    elif dir=="down":
        gen_move()
        body[0][1]+= 1
    elif dir=="left":
        gen_move()
        body[0][0]-=1
    elif dir=="up":
        gen_move()
        body[0][1]-= 1
    else:
        root.unbind("<KeyPress>")
        scoreB['text']='your final score is '+str(scor)

#method called when eating and moving simultaneosly
def eat():
    save = body[body.__len__() - 1]
    move()
    body.append(save)
    global scor
    scor+=1
    global scoreB
    scoreB['text']='score: '+str(scor)
    # board[body[0][0]][body[0][1]]['bg']=orig_col
    place_food()

#controls
def keydown(let):
    global dir
    # print(let)
    if let.char=='w':
        dir = "up"
    elif let.char=='a':
        dir = "left"
    elif let.char=='s':
        dir = "down"
    elif let.char=='d':
        dir = "right"

#looped stuff
def looped():
    global dir
    #raising all buttons
    for x in range(size):
        for y in range(size):
            board[x][y]['relief']=RAISED
            if board[x][y]['bg'] == 'black':
                board[x][y]['bg']=orig_col
    #depressing body
    for seg in body:
        board[seg[0]][seg[1]]['relief']=SUNKEN
        board[seg[0]][seg[1]]['bg']='black'

    #check front
    #check borders
    if body[0][0]>=size-1 and dir=="right":
        dir='none'
    elif body[0][1]>=size-1 and dir=="down":
        dir='none'
    elif body[0][0]<=0 and dir=="left":
        dir='none'
    elif body[0][1]<=0 and dir=="up":
        dir='none'
    #check tail
    elif dir=="right" and board[body[0][0]+1][body[0][1]]['relief']==SUNKEN:
        dir = 'none'
    elif dir=="down" and board[body[0][0]][body[0][1]+1]['relief']==SUNKEN:
        dir = 'none'
    elif dir=="left" and board[body[0][0]-1][body[0][1]]['relief']==SUNKEN:
        dir = 'none'
    elif dir=="up" and board[body[0][0]][body[0][1]-1]['relief']==SUNKEN:
        dir = 'none'
    #check food
    elif dir=="right" and board[body[0][0]+1][body[0][1]]['bg']=="green":
        eat()
    elif dir=="down" and board[body[0][0]][body[0][1]+1]['bg']=="green":
        eat()
    elif dir=="left" and board[body[0][0]-1][body[0][1]]['bg']=="green":
        eat()
    elif dir=="up" and board[body[0][0]][body[0][1]-1]['bg']=="green":
        eat()
    else:
        move()
        # print(body)

    root.after(250,looped)

start()
dir="none"
restart['text'] = "start"
looped()
root.mainloop()
