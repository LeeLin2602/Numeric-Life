from tkinter import *
from tkinter import messagebox
import pathlib

width = height = 6



def prepare(event):
	global root, width, height, width_entry, height_entry, rounds_entry,keep
	width = width_entry.get()
	height = height_entry.get()
	rounds = rounds_entry.get()

	if not (width.isnumeric() and height.isnumeric() and rounds.isnumeric()):
		messagebox.showinfo("Error","Only Integer Value Allowed!")
		return

	width, height, rounds = int(width), int(height), int(rounds)

	if rounds * 2 > width * height:
		messagebox.showinfo("Error","Too many rounds! (less than %s)" % str(1 + (width * height)//2))
		return

	if not (1 <= width <= 24 and 1 <= height <= 24):
		messagebox.showinfo("Error","Map Too Large! (Both height and width less than 24)")
		return


	root.destroy()

	keep = True
	start_game(width, height, rounds)

def start_game(width, height, rounds):
	root = Tk()
	root.geometry("860x680")
	root.title("Numeric Life - Main")
	root.iconbitmap(str(pathlib.Path(__file__).parent) + "\icon.ico")
	root.resizable(False, False)
	root.config(bg = "#ECECEC")

	WHITE = "#FFFFFF"

	Blocks = [[PanedWindow(root, bg = WHITE, height = 660 // height - 3, width = 660 // width - 3) for j in range(width)] for i in range(height)]
	Labels = [[] for i in range(height)]
	Scores = [[] for i in range(height)]
	
	round_msg = Label(root, height = 1, width = 15, text = "Round: 1.1 / %s" % rounds, anchor = W, bg = "#ECECEC")
	Red_Score = Label(root, height = 1, width = 15, text = "RED :" , anchor = W, bg = "#ECECEC")
	Blue_Score = Label(root, height = 1, width = 15, text = "BLUE:", anchor = W, bg = "#ECECEC")
	Red_Score_msg = Label(root, height = 1, width = 10, text = "0" , bg = "#ECECEC")
	Blue_Score_msg = Label(root, height = 1, width = 10, text = "0", bg = "#ECECEC")

	round_msg.pack()
	Red_Score.pack()
	Blue_Score.pack()
	Red_Score_msg.pack()
	Blue_Score_msg.pack()
	round_msg.place(x = 700, y = 30)
	Red_Score.place(x = 700, y = 60)
	Blue_Score.place(x = 700, y = 90)
	Red_Score_msg.place(x = 740, y = 60)
	Blue_Score_msg.place(x = 740, y = 90)
	Counters = [0, 0]
	turn = 0
	keep_game = True
	show_numb = True

	def click(event, i, j, prm = 0):
		nonlocal keep_game, turn, Labels, Scores, width, height, Counters, rounds, round_msg, Red_Score_msg, Blue_Score_msg, show_numb
		
		if not keep_game:
			if show_numb:
				for i in range(height):
					for j in range(width):
						Labels[i][j].config(text = "")
			else:
				for i in range(height):
					for j in range(width):
						Labels[i][j].config(text = str(Scores[i][j]if Scores[i][j] != 0 else ""))

			show_numb = show_numb == False
			return 

		if not (0 <= event.x <= 660 // height - 3  and 0 <= event.y <= 660 // width - 3):
			return

		if not Scores[i][j] == 0:
			return

		if prm == 0:
			score = 0

			if i != 0:
				score += Scores[i - 1][j]
			if j != 0:
				score += Scores[i][j - 1]
			if i != height - 1:
				score += Scores[i + 1][j]
			if j != width - 1:
				score += Scores[i][j + 1]

			score = max(score, 1)
		elif prm == 1:
			score = 1

		Scores[i][j] = score
		Labels[i][j].config(bg = ["#FFB6C1","#73d4f5"][turn % 2], text = score)
		Counters[turn % 2] += score
		
		Red_Score_msg.config(text = str(Counters[0]))
		Blue_Score_msg.config(text = str(Counters[1]))

		turn = turn + 1
		round_msg.config(text = "Round: %s.%s / %s" % (turn // 2 + 1, turn % 2 + 1, rounds))
		
		if turn//2 == rounds:
			keep_game = False
			Counters[1] -= score // 2
			Blue_Score_msg.config(text = str(Counters[1]))
			round_msg.config(text = "Game Set")
			if Counters[0] > Counters[1]:
				messagebox.showinfo("Game Set","The Winner is RED!")
			elif Counters[0] == Counters[1]:
				messagebox.showinfo("Game Set","DRAW!")
			else:
				messagebox.showinfo("Game Set","The Winner is BLUE!")


	for i in range(height):
		for j in range(width):
			Scores[i].append(0)
			Labels[i].append(Label(Blocks[i][j], bg = WHITE, anchor = CENTER,text = "", font = ("Helvetica %s bold" % str(max(8,int((660 // width - 3)//5.5))))))
			Labels[i][j].bind("<ButtonRelease-1>",lambda event, a = i, b = j: click(event, a, b, 0))
			Labels[i][j].bind("<ButtonRelease-3>",lambda event, a = i, b = j: click(event, a, b, 1))
			Blocks[i][j].pack()
			Blocks[i][j].add(Labels[i][j])
			Blocks[i][j].place(x = 13 + (660 // height) * i, y = 13 + (660 // width) * j)
			
	root.mainloop()

def leave(event):
	global root,keep
	root.destroy()

keep = True

while keep:
	keep = False
	root = Tk()
	root.geometry("250x160")
	root.title("Numeric Life - Config")
	root.iconbitmap(str(pathlib.Path(__file__).parent) + "\icon.ico")
	root.resizable(False, False)

	msg1 = Label(root, text = "Input Map Size:")
	msg2 = Label(root, text = "x")
	msg3 = Label(root, text = "Rounds:")
	msg4 = Label(root, text = " < 19")

	def calculate(event, width_entry, height_entry, msg4):
		if width_entry.get().isnumeric() and height_entry.get().isnumeric():
			msg4.config(text = " < " + str(int(width_entry.get()) * int(height_entry.get())//2 + 1))
		else:
			msg4.config(text = "Wrong Value for Size")

	width_entry = Entry(root, width=5)
	height_entry = Entry(root, width=5)
	rounds_entry = Entry(root, width=5)
	width_entry.insert(0,'6')
	height_entry.insert(0,'6')
	rounds_entry.insert(0,'18')

	width_entry.bind("<KeyRelease>", lambda event: calculate(event, width_entry, height_entry, msg4))
	height_entry.bind("<KeyRelease>", lambda event: calculate(event, width_entry, height_entry, msg4))

	button = Button(root, height = 1, width = 5, text = "START")
	button.bind("<ButtonRelease-1>", prepare)
	exit = Button(root, height = 1, width = 5, text = "EXIT")
	exit.bind("<ButtonRelease-1>",leave)


	msg1.pack()
	msg2.pack()
	msg3.pack()
	msg4.pack()
	width_entry.pack()
	height_entry.pack()
	rounds_entry.pack()
	button.pack()
	exit.pack()

	msg1.place(x = 15,  y = 10)
	msg2.place(x = 170, y = 13)
	msg3.place(x = 15,  y = 50)
	msg4.place(x = 170, y = 50)

	width_entry.place(x = 130, y = 15)
	height_entry.place(x = 185,y = 15)
	rounds_entry.place(x = 130, y = 53)
	button.place(x = 185, y = 100)
	exit.place(x = 30, y = 100)
	root.mainloop()