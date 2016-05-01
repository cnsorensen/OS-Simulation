from Tkinter import *
from ttk import *
import random
import time

def test():
    print 'Hello mother fucking world!!!'

def pr_generate( pr_alg, num_frames, num_refs ):
    print 'Page Replacement in da hizzhowwwss'
    print pr_alg
    print num_frames

    # the range of the values of references
    range_min = 0
    range_max = 5

    # holds the reference string
    ref_string = []

    # generate the random reference string with the range of
    # values and the number of references
    ref_string = generate_ref_string( range_min, range_max, num_refs )

    print ref_string

    if pr_alg == "FIFO":
        draw_pr_fifo( num_frames, num_refs, ref_string )

#    canline = pr_canvas.create_line( 0, 0, 300, 0 )
    #canbox = pr_canvas.create_rectangle( ( 150, 150, 250, 250 ) )

def generate_ref_string( range_min, range_max, num ):
    
    # holds the string of random numbers
    ref_string = []

    # generate num number of random number and add to the ref string list
    for i in range( 0, num, 1 ):
        j = random.randint( range_min, range_max )
        ref_string.append( j )

    # return that list of random numbers
    return ref_string

def draw_pr_fifo( num_frames, num_refs, ref_string ):
    print "Drawing fifo"

    ## draw the pages out first ##

    # height and width of each page
    # dynamically based off of the number of refs, including spaces
    #   inbetween, and on the width of the window = 500
    width = 500 / ( num_refs * 2 + 1 )
    print width
    print num_frames
    print num_refs
    print ref_string


    # for indexing how far away from the left side times width
    x1_1 = 1
    x1_2 = 2

    # create the outside of the entire page table
    for ref in range( 0, num_refs, 1 ):
        canbox = pr_canvas.create_rectangle( x1_1 * width, width, x1_2 * width, 
                num_frames * width + width )

        # set the variables to draw the inner pages
        x2_1 = x1_1 * width
        x2_2 = x1_2 * width
        y2_1 = 1
        y2_2 = 2

        # adjust the x values for the next reference outline AFTER you 
        # used them to set the variables to draw the inner pages
        x1_1 = x1_1 + 2
        x1_2 = x1_2 + 2

        # draw the inner pages
        for frame in range( 0, num_frames, 1 ):
            canbox = pr_canvas.create_rectangle( x2_1, y2_1 * width, x2_2, y2_2 * width )
            y2_1 = y2_1 + 1
            y2_2 = y2_2 + 1

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
    root.geometry( "900x500" )
    # set up the tab structure
    notebook = Notebook( root )

    # set up each fo the tabs and add them 
    one = Frame( notebook ) 
    two = Frame( notebook )
    three = Frame( notebook ) 

    # label the tabs
    notebook.add( one, text = "Procss Scheduler" )
    notebook.add( two, text = "Memory Management Unit" )
    notebook.add( three, text = "Page Replacement" )
    notebook.pack( side = TOP )

    # the seeder for the randomizer
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
    middle = Frame( three )
    middle.pack( side = TOP )
    bottom = Frame( three )
    bottom.pack( side = TOP )

    ##OLD
    cmds = Frame( three )
    cmds.pack( side = TOP )
    string1 = ""
    string2 = ""
    ##

    # Values for the radio buttons
    pr_algorithms = [
        ( "FIFO", "FIFO" ),
        ( "Optimal", "Optimal" ),
        ( "LRU", "LRU" ),
        ( "LFU", "LFU" ),
        ( "NRU", "NRU" )
    ]

    num_frames_selections = [
        ( "1", 1 ),
        ( "2", 2 ),
        ( "3", 3 ),
        ( "4", 4 ),
        ( "5", 5 )
    ]

    num_refs_selections = [
        ( "5", 5 ),
        ( "6", 6 ),
        ( "7", 7 ),
        ( "8", 8 ),
        ( "9", 9 ),
        ( "10", 10 )
    ]

    # label for the page replacement algorithm selection
    pr_alg_L = Label( top, text = 'Page Replacement Algorithm' )
    pr_alg_L.pack()

    # radio buttons to select the page replacement algorithm
    pr_alg = StringVar()
    # initalize it
    pr_alg.set("FIFO")
    # add each button to the display
    for text, mode in pr_algorithms:
        pr_alg_b = Radiobutton( top, text = text, variable = pr_alg, value = mode )
        pr_alg_b.pack( side = LEFT )


    # label for the number of frames selection
    num_frames_L = Label( middle, text = 'Number of Page Frames:' )
    num_frames_L.pack()

    # radio buttons to select the number of frames
    num_frames = IntVar()
    # initalize it
    num_frames.set( "3" )
    # add each button to the display
    for text, mode in num_frames_selections:
        num_frames_b = Radiobutton( middle, text = text, variable = num_frames, value = mode )
        num_frames_b.pack( side = LEFT )

    # label for the number of references selection
    num_refs_L = Label( bottom, text = 'Number of References:' )
    num_refs_L.pack()

    # radio buttons to select the number of references
    num_refs = IntVar()
    #initalize it
    num_refs.set( "7" )
    # add each button to the display
    for text, mode in num_refs_selections:
        num_refs_b = Radiobutton( bottom, text = text, variable = num_refs, value = mode )
        num_refs_b.pack( side = LEFT )


    # generate button to submit the page replacement information
    pr_generate_b = Button( three, text = "Generate", 
        command = lambda: pr_generate( pr_alg.get(), num_frames.get(), num_refs.get() ) )
    pr_generate_b.pack()

    # the canvas where the page replacement results will be laid
    pr_canvas = Canvas( three, width = 500, height = 500 )
    pr_canvas.pack()


    return pr_generate_b, pr_canvas

if __name__ == "__main__":
    N = 5
    M = 6

    pr_alg = "DOG"

    root,one,two,three = gui()
    frame1()
    bcan, can = frame2()
    pr_generate_b, pr_canvas = frame3()

    root.mainloop()

