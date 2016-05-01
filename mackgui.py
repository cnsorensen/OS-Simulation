
from Tkinter import *
from ttk import *
import random


def test():
    print 'Hello mother fucking world!!!'

def pr_generate():
    print 'Page Replacement in da hizzhowwwss'
    canline = pr_canvas.create_line( 0, 0, 200, 100 )
    canbox = pr_canvas.create_rectangle( ( 150, 150, 250, 250 ) )

def printvar( var ):
    print var[0].get()

def pushvar( var ):
	for i in range( N-1, 0, -1 ):
		var[i].set( var[i-1].get() )
	var[0].set( '' )

# Creates a line
def line():
	canline = can.create_line( 0, 0, 250, 250, 53, 69, 300, 300 )
	canbox = can.create_rectangle( ( 150, 150, 250, 250 ) )
	bcan.config( text = "Hide", command = hide )

def hide():
	bcan.config( text = "Draw", command = line )
	can.delete( "all" )

def randvar():
	string2[0].set( random.randint( 0, 32 ) )

# Sets up the GUI
def gui():
    # set up the window
    root = Tk()
    # title of the window
    root.title( "Simulation Project" )
    # set the size of the window
    root.geometry( "1000x1000" )
    # set up the tab structure
    notebook = Notebook( root )

    # set up each fo the tabs and add them 
    one = Frame( notebook ) 
    two = Frame( notebook )
    three = Frame( notebook ) 

    notebook.add( one, text = "Process Scheduler" )
    notebook.add( two, text = "Memory Management Unit" )
    notebook.add( three, text = "Page Replacement" )
    notebook.pack( side = TOP )
    random.seed()
    return root, one, two, three



# Process Scheduler tab
def frame1(frame):	
    top = Frame(one)
    left = Frame(one)
    left.pack(side=LEFT)
    top.pack(side=TOP)

    sc_canvas = Canvas( one, width = 500, height = 500, borderwidth = 2 )
    sc_canvas.pack(side=RIGHT)

    processList = []
    selection = IntVar()
    priority = StringVar()
    timeslice = StringVar()
    process = StringVar()
    arrival = StringVar()
    burst = StringVar()
    
   
    def gantt(): 
        summ = 0
        if selection.get() == 3:  # shortest job first
            for i in processList:
                summ += int(i[2])
            sc_canvas.create_rectangle(50, 150, summ * 10, 250, fill="blue")
            sc_canvas.create_rectangle(50, 150, int(processList[0][2]) * 100, 250, fill="red")
                
       
    def add():
        t.insert(END,  processid.get() + "\t|\t" + arrivTime.get() + "\t|\t" + burstTime.get() + "\n")
        processList.append(list((processid.get(), arrivTime.get(), burstTime.get())))

    b = Button(left, text="Add Process", width=10, command=add)
    g = Button(top, text="Produce Gantt Chart", width=10, command=gantt)
    
    priorityfield = Entry(left, textvariable = priority)
    timequanta = Entry(left, textvariable = timeslice)
    processid = Entry(left, textvariable = process)
    arrivTime = Entry(left, textvariable = arrival)
    burstTime = Entry(left, textvariable = burst)

    Radiobutton(top, text = "Round Robin", variable = selection, value = 1).pack(side=LEFT)
    Radiobutton(top, text = "Priority", variable = selection, value = 2).pack(side=LEFT)
    Radiobutton(top, text = "SJF", variable = selection, value = 3).pack(side=LEFT)
    g.pack(anchor=SE)

    priorityLabel = Label(left, text="Priority (only for priority scheduling)").pack(anchor=NW)
    priorityfield.pack(anchor = NW)
    timeLabel = Label(left, text="Time slice (only for round robin)").pack(anchor=NW)
    timequanta.pack(anchor = NW)
    processLabel = Label(left, text="Process ID").pack(anchor=NW)
    processid.pack(anchor = NW)
    arrivalLabel = Label(left, text="Arrival Time").pack(anchor=W)
    arrivTime.pack(anchor = W)
    burstLabel = Label(left, text="Burst Time").pack(anchor=SW)
    burstTime.pack(anchor = SW)
    b.pack()

    t = Text(left, height = 20, width = 45)
    t.pack()

    t.insert(END, "Process ID \t|\tArrival Time\t|\tBurst Time\n")
    ##Add radio buttons to select a scheduler type

# Memory Management Unit tab
def frame2():
    b = Button( two, text="Draw", command = line )
    b.pack()
    can = Canvas( two, width = 300, height = 300 )
    can.pack()
    return b, can

# Page Replacement tab
# FIFO, Optimal, LRU, LFU, NRU
# Use Auto-generated reference strings
# The user will select the algorithm, number of frames, and reference string deets
# Output page faults
def frame3():
    top = Frame( three )
    top.pack( side = TOP )
    bottom = Frame( three )
    bottom.pack( side = TOP )
    cmds = Frame( three )
    cmds.pack( side = TOP )

    string1 = ""
    string2 = ""

    pr_algorithms = [
        ( "FIFO", "FIFO" ),
        ( "Optimal", "Optimal" ),
        ( "LRU", "LRU" ),
        ( "LFU", "LFU" ),
        ( "NRU", "NRU" )
    ]

    # radio buttons to select the page replacement algorithm
    pr_alg = StringVar()
    # initalize it
    pr_alg.set("FIFO")
    # add each button
    for text, mode in pr_algorithms:
        pr_alg_b = Radiobutton( top, text = text, variable = pr_alg, value = mode )
        pr_alg_b.pack( side = LEFT )

    # generate button to submit the page replacement information
    pr_generate_b = Button( three, text = "Generate", command = pr_generate )
    pr_generate_b.pack()

    # the canvas where the page replacement results will be laid
    pr_canvas = Canvas( three, width = 500, height = 500 )
    pr_canvas.pack()

    '''
    string1 = []
    entry1 = []
    for i in range( M ): 
	    string1.append( StringVar() )
	    entry1.append( Entry( top, width = 5, textvariable = string1[i] ) )
	    entry1[i].pack( side = LEFT )

    string2 = []
    entry2 = []
    for i in range( N ): 
	    string2.append( StringVar() )
	    entry2.append( Entry( bottom, width = 6, textvariable = string2[i] ) )
	    entry2[i].pack()

    b1 = Button( cmds, text = "Push", command = lambda: pushvar( string2 ) )
    b1.pack( side = LEFT )

    b2 = Button( cmds, text = "Print", command = lambda: printvar( string2 ) )
    b2.pack( side = LEFT )

    b3 = Button( cmds, text = "Random", command = randvar )
    b3.pack( side = LEFT )
    var = string1[0].get()'''
    return pr_generate_b, pr_canvas

if __name__ == "__main__":

    root,one,two,three = gui()
    frame1(root)
    bcan, can = frame2()
    pr_generate_b, pr_canvas = frame3()

    root.mainloop()

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
