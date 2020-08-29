from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import random, os, json

computer_img = [r'./images/c_paper.png', r'./images/c_rock.png', r'./images/c_scissor.png']
user_img = [r'./images/u_paper.png', r'./images/u_rock.png', r'./images/u_scissor.png']
img_user = None
img_computer = None 

def user_select(user_choice):
    '''Displaying the selected Action and update winning count'''
    computer_choice = random.randint(0,2)
    winner = find_winner(user_choice, computer_choice)
    
    if winner == 'user':
        global user_score
        msg = int(user_score['text']) + 1
        user_score = Label(root, text=msg, font="Helvetica 24")
        user_score.grid(row=4, column=0, sticky=E)
        Label(root, text='WIN', font="Helvetica 14", foreground='green').grid(row=5, column=1, sticky=W+E)
        compare_highscore(msg, 1)
    elif winner == 'computer':
        global computer_score
        msg = int(computer_score['text']) + 1
        computer_score = Label(root, text=msg, font="Helvetica 24")
        computer_score.grid(row=4, column=2, sticky=W)
        Label(root, text='LOSE', font="Helvetica 14", foreground='red').grid(row=5, column=1, sticky=W+E)
        compare_highscore(msg, 2)
    else:
        global tie_score
        msg = int(tie_score['text']) + 1
        tie_score = Label(root, text=msg, font="Helvetica 14")
        tie_score.grid(row=4, column=1, sticky=W+E)
        Label(root, text='TIE', font="Helvetica 14", foreground='yellow').grid(row=5, column=1, sticky=W+E)
        compare_highscore(msg, 3)

    last_game_score(user_score['text'], computer_score['text'], tie_score['text'])

    # User Selected Action Image
    global img_user
    img_user = ImageTk.PhotoImage(Image.open(user_img[user_choice]))
    logo_panel_user = Label(root, image=img_user)
    logo_panel_user.grid(row=5, column=0, padx=5, pady=6, sticky=E)

    # Computer Selected Action Image
    global img_computer
    img_computer = ImageTk.PhotoImage(Image.open(computer_img[computer_choice]))
    logo_panel_computer = Label(root, image=img_computer)
    logo_panel_computer.grid(row=5, column=2, padx=5, pady=6, sticky=W)


def find_winner(u, c):
    '''Find the winner'''
    if u == c:
        return 'None'
    elif u == 0:
        if c == 1:
            return 'user'
        else:
            return 'computer'
    elif u == 1:
        if c == 2:
            return 'user'
        else:
            return 'computer'
    elif u == 2:
        if c == 0:
            return 'user'
        else:
            return 'computer'


def get_highscore():
    '''Get the Highscore'''
    record = read_json()
    title = "HighScore"
    msg = "Last/Current Game Score:"
    msg += "\n- User Win: "+ str(record['last_user'])
    msg += "\n- Computer Win: "+ str(record['last_computer'])
    msg += "\n- Tie: "+ str(record['last_tie'])
    msg += "\n\nOverall Max. Wins"
    msg += "\n- User Win: "+ str(record['highscore'])
    msg += "\n- Computer Win: "+ str(record['loss'])
    msg += "\n- Tie: "+ str(record['tie'])
    messagebox.showinfo(title, msg)


def reset_game():
    '''Restarting the Game'''
    os.execl(sys.executable, sys.executable, *sys.argv)

def read_json():
    try:
        with open('highscore.json') as f:
            return json.load(f)
    except:
        return {"highscore":0, "loss":0, "tie":0, 'last_user':0, 'last_computer':0, 'last_tie':0}

def write_json(record):
    with open('highscore.json', 'w') as f:
     json.dump(record, f)

def compare_highscore(score, user):
    record = read_json()
    if score > record['highscore'] and user == 1:
        record["highscore"] = score
        write_json(record)
    if score > record['loss'] and user == 2:
        record["loss"] = score
        write_json(record)
    if score > record['tie'] and user == 3:
        record["tie"] = score
        write_json(record)
    

def last_game_score(u, c, t):
    record = read_json()
    record['last_user'] = u
    record['last_computer'] = c
    record['last_tie'] = t
    write_json(record)


# GUI START HERE

root = Tk()
root.title("Paper-Rock-Scissor Game")
root.iconbitmap('images/favicon.ico')
root.resizable(width=False, height=False)
root.geometry("429x368+400+180")

# App Logo
img = ImageTk.PhotoImage(Image.open(".\images\logo.png"))
logo_panel = Label(root, image=img)
logo_panel.grid(row=0, column=0, columnspan=3, pady=(20,0), sticky=W+E)

# HighScore Button
highscore_img = PhotoImage(file=r'./images/highscore.png')
btn_highscore = Button(root, image=highscore_img, compound=LEFT, command=get_highscore)
btn_highscore.grid(row=0, column=2, pady=(20,0), sticky=N+E)

# Restart Game Button
reset_img = PhotoImage(file=r'./images/reset.png')
btn_highscore = Button(root, image=reset_img, compound=LEFT, command=reset_game)
btn_highscore.grid(row=0, column=2, pady=(20,0), sticky=S+E)


#  Define Action Button
btn_paper = Button(root, text="Paper", font="Helvetica 10", padx=15, pady=10,
                                            command=lambda: user_select(0)) 
btn_rock = Button(root, text="Rock", font="Helvetica 10", padx=1, pady=10,
                                            command=lambda: user_select(1)) 
btn_scissor = Button(root, text="Scissor", font="Helvetica 10", padx=15, pady=10,
                                            command=lambda: user_select(2)) 

# Display Action Button
btn_paper.grid(row=2, column=0, padx=10, pady=20, ipadx= 28)
btn_rock.grid(row=2, column=1, padx=10, pady=20, ipadx=36)
btn_scissor.grid(row=2, column=2, padx=10, pady=20, ipadx=17)

# Player Label 
user_name = Label(root, text="User", font="Helvetica 12")
user_name.grid(row=3, column=0, sticky=E)
tie_label = Label(root, text="Tie", font="Helvetica 12")
tie_label.grid(row=3, column=1, sticky=W+E)
computer_name = Label(root, text="Computer", font="Helvetica 12")
computer_name.grid(row=3, column=2, sticky=W)

# User Score - Seperator - Computer Score
user_score = Label(root, text="0", font="Helvetica 24")
user_score.grid(row=4, column=0, sticky=E)
tie_score = Label(root, text="0", font="Helvetica 14")
tie_score.grid(row=4, column=1, sticky=W+E)
computer_score = Label(root, text="0", font="Helvetica 24")
computer_score.grid(row=4, column=2, sticky=W)

# Note:
#  Get the detail of geometry  in console
# root.update()
# print(root.winfo_width())
# print(root.winfo_height())
# print(root.winfo_geometry())
root.mainloop()