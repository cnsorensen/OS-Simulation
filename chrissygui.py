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

    # get the number of frames from the user
    num_frames = StringVar()
    num_frames_e = Entry( three, width = 20, textvariable = num_frames )
    num_frames_e.pack()


    # generate button to submit the page replacement information
    pr_generate_b = Button( three, text = "Generate", command = pr_generate )
    pr_generate_b.pack()

    # the canvas where the page replacement results will be laid
    pr_canvas = Canvas( three, width = 500, height = 500 )
    pr_canvas.pack()

    return pr_generate_b, pr_canvas

if __name__ == "__main__":
    N = 5
    M = 6

    root,one,two,three = gui()
    frame1()
    bcan, can = frame2()
    pr_generate_b, pr_canvas = frame3()

    root.mainloop()

