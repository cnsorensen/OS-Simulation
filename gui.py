from Tkinter import *
from ttk import *
import random

def test():
    print 'Hello mother fucking world!!!'

def printvar( var ):
    print var[0].get()

def pushvar( var ):
	for i in range( N-1, 0, -1 ):
		var[i].set( var[i-1].get() )
	var[0].set( '' )

# Creates a line
def line():
	canline = can.create_line( 0, 0, 200, 100 )
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
    root.geometry( "500x300" )
    # set up the tab structure
    notebook = Notebook( root )

    # set up each fo the tabs and add them 
    one = Frame( notebook ) 
    two = Frame( notebook )
    three = Frame( notebook ) 

    notebook.add( one, text = "Procss Scheduler" )
    notebook.add( two, text = "Memory Management Unit" )
    notebook.add( three, text = "Page Replacement" )
    notebook.pack( side = TOP )
    random.seed()
    return root, one, two, three

# Process Scheduler tab
def frame1():	
    L = Label( one, text = 'Im a labelly label' )
    L.pack()
    b = Button( one, text = "OK", command = exit )
    b.pack()
    add_b = Button( one, text = "Add", command = test )
    add_b.pack()
    clear_b = Button( one, text = "Clear", command = test )
    clear_b.pack()
    generate_b = Button( one, text = "Generate", command = test )
    generate_b.pack()
    ##Add radio buttons to select a scheduler type

# Memory Management Unit tab
def frame2():
    b = Button( two, text="Draw", command = line )
    b.pack()
    can = Canvas( two, width = 300, height = 300 )
    can.pack()
    return b, can

# Page Replacement tab
def frame3():
    top = Frame( three )
    top.pack( side = TOP )
    bottom = Frame( three )
    bottom.pack( side = TOP )
    cmds = Frame( three )
    cmds.pack( side = TOP )

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
    var = string1[0].get()
    return string1, string2

if __name__ == "__main__":
    N = 5
    M = 6

    root,one,two,three = gui()
    frame1()
    bcan, can = frame2()
    string1, string2 = frame3()

    root.mainloop()
