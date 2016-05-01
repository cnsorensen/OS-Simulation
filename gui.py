from Tkinter import *
from ttk import *
import random


def printvar(var):
   print var[0].get()

def pushvar(var):
	for i in range(N-1,0,-1):
		var[i].set(var[i-1].get())
	var[0].set('')

def line():
	canline = can.create_line(0,0,200,100)
	canbox = can.create_rectangle((150,150,250,250))
	bcan.config(text="Hide", command=hide)

def hide():
	bcan.config(text="Draw",command=line)
	can.delete("all")

def randvar():
	string2[0].set(random.randint(0,32))

def gui():
	#set up the window
	root = Tk()
	root.title("Sample GUI using Tkinter")
	root.geometry("500x300")
	#set up the tab structure
	notebook = Notebook(root)

	#set up each fo the tabs and add them 
	one = Frame(notebook) 
	two = Frame(notebook)
	three = Frame(notebook) 

	notebook.add(one, text = "Tab 1")
	notebook.add(two, text = "Tab 2")
	notebook.add(three, text = "Tab 3")
	notebook.pack(side=TOP)
	random.seed()
	return root, one, two, three


def frame1():
	L = Label(one, text='A simple GUI')
	L.pack()
	b = Button(one, text="OK", command=exit)
	b.pack()


def frame2():
	b = Button(two, text="Draw", command=line)
	b.pack()
	can = Canvas(two, width=300, height =300)
	can.pack()
	return b, can


def frame3():
	top = Frame(three)
	top.pack(side=TOP)
	bottom = Frame(three)
	bottom.pack(side=TOP)
	cmds = Frame(three)
	cmds.pack(side=TOP)

	string1 = []
	entry1 = []
	for i in range(M): 
		string1.append(StringVar())
		entry1.append(Entry(top, width=5, textvariable = string1[i]))
		entry1[i].pack(side=LEFT)

	string2 = []
	entry2 = []
	for i in range(N): 
		string2.append(StringVar())
		entry2.append(Entry(bottom, width=6, textvariable = string2[i]))
		entry2[i].pack()


	b1 = Button(cmds, text="Push", command=lambda: pushvar(string2))
	b1.pack(side=LEFT)

	b2 = Button(cmds, text="Print", command=lambda: printvar(string2))
	b2.pack(side=LEFT)

	b3 = Button(cmds, text="Random", command=randvar)
	b3.pack(side=LEFT)
	var = string1[0].get()
	return string1, string2



N = 5
M = 6

root,one,two,three = gui()
frame1()
bcan, can = frame2()
string1, string2 = frame3()


root.mainloop()
