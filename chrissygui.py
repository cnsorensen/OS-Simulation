from Tkinter import *
from ttk import *
import random
import time

def test():
    print 'Hello mother fucking world!!!'

def pr_generate( pr_alg, num_frames, num_refs ):
    print 'Page Replacement'

    # the range of the values of references
    range_min = 0
    range_max = 5

    # holds the reference string
    ref_string = []

    # generate the random reference string with the range of
    # values and the number of references
    ref_string = generate_ref_string( range_min, range_max, num_refs )

    print 'Ref string:'
    print ref_string

    if pr_alg == "FIFO":
        draw_pr_fifo( num_frames, num_refs, ref_string )
    elif pr_alg == "Optimal":
        draw_pr_optimal( num_frames, num_refs, ref_string )
    elif pr_alg == "LRU":
        draw_pr_lru( num_frames, num_refs, ref_string )
    elif pr_alg == "LFU":
        draw_pr_lfu( num_frames, num_refs, ref_string )
    elif pr_alg == "NRU":
        draw_pr_nru( num_frames, num_refs, ref_string )
    else:
        print "Well you're fucked."

def generate_ref_string( range_min, range_max, num ):
    
    # holds the string of random numbers
    ref_string = []

    # generate num number of random number and add to the ref string list
    for i in range( 0, num, 1 ):
        j = random.randint( range_min, range_max )
        ref_string.append( j )

    # return that list of random numbers
    return ref_string

################################### FIFO #############################################
def draw_pr_fifo( num_frames, num_refs, ref_string ):
    print "Drawing fifo"

    ## draw the pages out first ##

    # height and width of each page
    # dynamically based off of the number of refs, including spaces
    #   inbetween, and on the width of the window = 500
    width = 500 / ( num_refs * 2 + 1 )

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

    ## fill in the boxes ##
    
    # The y positions for the pages
    # Position 0 is the ref that's currently being processed
    # Position num_frames + 2 will hold the position for the page fault notification
    # These values will stay throughout the process
    y_pos = {}
    y_pos[0] = width / 2
    for frame in range( 1, num_frames + 2, 1 ):
        y_pos[frame] = y_pos[frame-1] + width

    # hold the values of the pages
    # initialize to all -1's for empty
    page_table = {}
    for i in range( 0, num_frames, 1 ):
        page_table[i] = -1

    # holds how long the value has been in the table
    page_time = {}
    for i in range( 0, num_frames, 1 ):
        page_time[i] = -1

    # the x position for the text
    x_pos = 1 * width + width / 2

    # go through the ref string
    for val in ref_string:
        print 'Current page table:'
        print page_table

        # initalize the fault flag to true
        fault_flag = True

        # go through the page table and look for insert or match
        for i in range( 0, num_frames, 1 ):
            # if the value is already there, continue
            if page_table[i] == val:
                fault_flag = False
                break
            # if there is an empty spot, insert and continue
            elif page_table[i] == -1:
                page_table[i] = val
                # start it at 0, it will be incremented to 1 soon
                page_time[i] = 0
                fault_flag = False
                break

        # increment the time of all of the values in the page table
        for i in range( 0, num_frames, 1 ):
            # skip the empty ones
            if page_table[i] != -1:
                page_time[i] = page_time[i] + 1
            
        # if there is a page fault, replace the value that was first in
        # find which value was first in
        if fault_flag == True:
            max_time = -1
            max_index = -1
            for i in range( 0, num_frames, 1 ):
                if page_time[i] > max_time:
                    max_time = page_time[i]
                    max_index = i

            # replace it
            page_time[max_index] = 1
            page_table[max_index] = val
            
        # print the current page table to the display
        # print the ref val on the top
        cantext = pr_canvas.create_text( x_pos, y_pos[0], text = str( val ) )
        for fuck in range( 0, len( page_table ), 1 ):
            if page_table[fuck] != -1:
                cantext = pr_canvas.create_text( x_pos, y_pos[fuck+1], text = str( page_table[fuck] ) )
        
        # if there was a page fault, write it at the bottom of the page table
        if fault_flag == True:
            cantext = pr_canvas.create_text( x_pos, y_pos[len( page_table ) + 1], text ="PF" )

        # increment the x position
        x_pos = x_pos + 2 * width

################################ OPTIMAL #############################################
def draw_pr_optimal( num_frames, num_refs, ref_string ):
    print "Drawing optimal"

    ## draw the pages out first ##

    # height and width of each page
    # dynamically based off of the number of refs, including spaces
    #   inbetween, and on the width of the window = 500
    width = 500 / ( num_refs * 2 + 1 )

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

    ## fill in the boxes ##
    
    # The y positions for the pages
    # Position 0 is the ref that's currently being processed
    # Position num_frames + 2 will hold the position for the page fault notification
    # These values will stay throughout the process
    y_pos = {}
    y_pos[0] = width / 2
    for frame in range( 1, num_frames + 2, 1 ):
        y_pos[frame] = y_pos[frame-1] + width

    # hold the values of the pages
    # initialize to all -1's for empty
    page_table = {}
    for i in range( 0, num_frames, 1 ):
        page_table[i] = -1

    # holds the distances of the values in the table
    page_dist = {}
    for i in range( 0, num_frames, 1 ):
        page_dist[i] = -1

    # the x position for the text
    x_pos = 1 * width + width / 2

    # create the string of distances for each of the refs
    max_dist = num_refs * 2
    dist_refs = {}
    dist_refs = get_distances( num_refs, ref_string )

    # go through the ref string
    for val in range( 0, num_refs, 1):
        print 'Current page table:'
        print page_table

        # initalize the fault flag to true
        fault_flag = True

        # go through the page table and look for insert or match
        for i in range( 0, num_frames, 1 ):
            # if the value is already there, continue
            if page_table[i] == ref_string[val]:
                # update the page distances
                page_dist[i] = dist_refs[val]
                fault_flag = False
                break
            # if there is an empty spot, insert and continue
            elif page_table[i] == -1:
                page_table[i] = ref_string[val]
                # start it at 0, it will be incremented to 1 soon
                page_dist[i] = dist_refs[val]
                fault_flag = False
                break

        # decrement the distance of all of the values in the page table
        for i in range( 0, num_frames, 1 ):
            # increment that ones that aren't coming back
            if page_dist[i] >= max_dist:
                page_dist[i] = page_dist[i] + 1
            # skip the empty ones
            elif page_dist[i] != -1:
                page_dist[i] = page_dist[i] - 1
            
        # if there is a page fault, replace the value that was first in
        # find which value was first in
        if fault_flag == True:
            max_dist = -1
            max_index = -1
            for i in range( 0, num_frames, 1 ):
                if page_dist[i] > max_dist:
                    max_dist = page_dist[i]
                    max_index = i

            # replace it
            page_dist[max_index] = dist_refs[val]
            page_table[max_index] = ref_string[val]
            
        # print the current page table to the display
        # print the ref val on the top
        cantext = pr_canvas.create_text( x_pos, y_pos[0], text = str( ref_string[val] ) )
        for fuck in range( 0, len( page_table ), 1 ):
            if page_table[fuck] != -1:
                cantext = pr_canvas.create_text( x_pos, y_pos[fuck+1], text = str( page_table[fuck] ) )
        
        # if there was a page fault, write it at the bottom of the page table
        if fault_flag == True:
            cantext = pr_canvas.create_text( x_pos, y_pos[len( page_table ) + 1], text ="PF" )

        # increment the x position
        x_pos = x_pos + 2 * width

def get_distances( num_refs, refs_string ):
    # hold the distances for each ref to their next occurance
    dist_refs = {}

    # the max is double the number of refs for safety.
    # the values are going to be decremented so it prevents from
    # it becoming too small
    max_dist = num_refs * 2

    # initialize the array of distances to the max dist
    for i in range( 0, num_refs, 1 ):
        dist_refs[i] = max_dist 

    # find the distances
    # the current value in the ref string
    curr = -1
    # The flag for if the value is found in the rest of the string
    found_flag = False
    # go through each of the refs
    for i in range( 0, num_refs, 1 ):
        curr_ref = refs_string[i]
        dist = 0
        # go through the rest of the refs following the current one
        for j in range( i + 1, num_refs, 1 ):
            # if there is another occurance, note the distance and continue
            # to the next ref
            if refs_string[j] == curr_ref:
                dist_refs[i] = dist
                found_flag = True
                break
            dist = dist + 1   
        # if there isn't another occurance, set it to the max dist
        if found_flag == False:
            dist_refs[i] = max_dist

    # return the list of distance for references
    return dist_refs

####################################### LRU ##########################################
def draw_pr_lru( num_frames, num_refs, ref_string ):
    print "Drawing LRU"

    ## draw the pages out first ##

    # height and width of each page
    # dynamically based off of the number of refs, including spaces
    #   inbetween, and on the width of the window = 500
    width = 500 / ( num_refs * 2 + 1 )

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

    ## fill in the boxes ##
    
    # The y positions for the pages
    # Position 0 is the ref that's currently being processed
    # Position num_frames + 2 will hold the position for the page fault notification
    # These values will stay throughout the process
    y_pos = {}
    y_pos[0] = width / 2
    for frame in range( 1, num_frames + 2, 1 ):
        y_pos[frame] = y_pos[frame-1] + width

    # hold the values of the pages
    # initialize to all -1's for empty
    page_table = {}
    for i in range( 0, num_frames, 1 ):
        page_table[i] = -1

    # Holds how long the value has been in the table
    page_time = {}
    for i in range( 0, num_frames, 1 ):
        page_time[i] = -1

    # Holds the time when the value was inserted
    page_insert_time = {}
    for i in range( 0, num_frames, 1 ):
        page_insert_time[i] = -1
    insert_time = 0
    

    # the x position for the text
    x_pos = 1 * width + width / 2

    # go through the ref string
    for val in ref_string:
        print 'Current page table:'
        print page_table

        # update the time
        insert_time = insert_time + 1

        # initalize the fault flag to true
        fault_flag = True

        # go through the page table and look for insert or match
        for i in range( 0, num_frames, 1 ):
            # if the value is already there, continue
            if page_table[i] == val:
                fault_flag = False
                # reset the timer
                page_time[i] = 0
                break
            # if there is an empty spot, insert and continue
            elif page_table[i] == -1:
                page_table[i] = val
                # start it at 0, it will be incremented to 1 soon
                page_time[i] = 0
                fault_flag = False
                # set the time that it was inserted
                page_insert_time[i] = insert_time
                break

        # increment the time of all of the values in the page table
        for i in range( 0, num_frames, 1 ):
            # skip the empty ones
            if page_table[i] != -1:
                page_time[i] = page_time[i] + 1
            
        # if there is a page fault, replace the value was least recently used
        if fault_flag == True:
            max_time = -1
            max_index = -1
            # used for FIFO within the algorithm
            min_insert_time = num_refs * 2
            for i in range( 0, num_frames, 1 ):
                # if it's the least recently used
                if page_time[i] > max_time:
                    # but it's also the first one of that least recently used value
                    if page_insert_time[i] < min_insert_time:
                        max_time = page_time[i]
                        max_index = i
                        min_insert_time = page_insert_time[i]

            # replace it
            page_time[max_index] = 1
            page_table[max_index] = val
            page_insert_time[max_index] = insert_time

        # print the current page table to the display
        # print the ref val on the top
        cantext = pr_canvas.create_text( x_pos, y_pos[0], text = str( val ) )
        for fuck in range( 0, len( page_table ), 1 ):
            if page_table[fuck] != -1:
                cantext = pr_canvas.create_text( x_pos, y_pos[fuck+1], text = str( page_table[fuck] ) )
        
        # if there was a page fault, write it at the bottom of the page table
        if fault_flag == True:
            cantext = pr_canvas.create_text( x_pos, y_pos[len( page_table ) + 1], text ="PF" )

        # increment the x position
        x_pos = x_pos + 2 * width

####################################### LFU ##########################################
def draw_pr_lfu( num_frames, num_refs, ref_string ):
    print "Drawing LFU"

    ## draw the pages out first ##

    # height and width of each page
    # dynamically based off of the number of refs, including spaces
    #   inbetween, and on the width of the window = 500
    width = 500 / ( num_refs * 2 + 1 )

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

    ## fill in the boxes ##
    
    # The y positions for the pages
    # Position 0 is the ref that's currently being processed
    # Position num_frames + 2 will hold the position for the page fault notification
    # These values will stay throughout the process
    y_pos = {}
    y_pos[0] = width / 2
    for frame in range( 1, num_frames + 2, 1 ):
        y_pos[frame] = y_pos[frame-1] + width

    # hold the values of the pages
    # initialize to all -1's for empty
    page_table = {}
    for i in range( 0, num_frames, 1 ):
        page_table[i] = -1

    # Holds the freqency of the number of time the page has been used
    page_freq = {}
    for i in range( 0, num_frames, 1 ):
        page_freq[i] = -1

    # Holds the time when the value was inserted
    page_insert_time = {}
    for i in range( 0, num_frames, 1 ):
        page_insert_time[i] = -1
    insert_time = 0

    # the x position for the text
    x_pos = 1 * width + width / 2

    # go through the ref string
    for val in ref_string:
        print 'Current page table:'
        print page_table

        # increment the time
        insert_time = insert_time + 1

        # initalize the fault flag to true
        fault_flag = True

        # go through the page table and look for insert or match
        for i in range( 0, num_frames, 1 ):
            # if the value is already there, continue
            if page_table[i] == val:
                fault_flag = False
                # reset the timer
                page_freq[i] = page_freq[i] + 1
                break
            # if there is an empty spot, insert and continue
            elif page_table[i] == -1:
                page_table[i] = val
                # start it at 1
                page_freq[i] = 1
                fault_flag = False
                # set the timestamp for it
                page_insert_time[i] = insert_time
                break

        # if there is a page fault, replace the value with the least frequency
        if fault_flag == True:
            min_freq = num_refs * 2
            min_index = -1
            # used for FIFO within the algorithm
            min_insert_time = num_refs * 2
            for i in range( 0, num_frames, 1 ):
                # if it's least frequently used
                if page_freq[i] < min_freq:
                    # but it's also the first of the least frequently used
                    if page_insert_time[i] < min_insert_time:
                        min_freq = page_freq[i]
                        min_index = i
                        min_insert_time = page_insert_time[i]

            # replace it
            page_freq[min_index] = 1
            page_table[min_index] = val
            page_insert_time[min_index] = insert_time

        # print the current page table to the display
        # print the ref val on the top
        cantext = pr_canvas.create_text( x_pos, y_pos[0], text = str( val ) )
        for fuck in range( 0, len( page_table ), 1 ):
            if page_table[fuck] != -1:
                cantext = pr_canvas.create_text( x_pos, y_pos[fuck+1], text = str( page_table[fuck] ) )
        
        # if there was a page fault, write it at the bottom of the page table
        if fault_flag == True:
            cantext = pr_canvas.create_text( x_pos, y_pos[len( page_table ) + 1], text ="PF" )

        # increment the x position
        x_pos = x_pos + 2 * width


####################################### NRU ##########################################
def draw_pr_nru( num_frames, num_refs, ref_string ):
    print "Drawing NRU"

    ## draw the pages out first ##

    # height and width of each page
    # dynamically based off of the number of refs, including spaces
    #   inbetween, and on the width of the window = 500
    width = 500 / ( num_refs * 2 + 1 )

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

    ## fill in the boxes ##
    
    # The y positions for the pages
    # Position 0 is the ref that's currently being processed
    # Position num_frames + 2 will hold the position for the page fault notification
    # These values will stay throughout the process
    y_pos = {}
    y_pos[0] = width / 2
    for frame in range( 1, num_frames + 2, 1 ):
        y_pos[frame] = y_pos[frame-1] + width

    # hold the values of the pages
    # initialize to all -1's for empty
    page_table = {}
    for i in range( 0, num_frames, 1 ):
        page_table[i] = -1

    # Holds the time of the number for how long it's been since used
    page_time = {}
    for i in range( 0, num_frames, 1 ):
        page_time[i] = -1

    # the x position for the text
    x_pos = 1 * width + width / 2

    # go through the ref string
    for val in ref_string:
        print 'Current page table:'
        print page_table

        # initalize the fault flag to true
        fault_flag = True

        # go through the page table and look for insert or match
        for i in range( 0, num_frames, 1 ):
            # if the value is already there, continue
            if page_table[i] == val:
                fault_flag = False
                # reset the time (it'll be incremented soon)
                page_time[i] = 0
                break
            # if there is an empty spot, insert and continue
            elif page_table[i] == -1:
                page_table[i] = val
                # start it at 0 (it'll be incremented soon)
                page_time[i] = 0
                fault_flag = False
                break

        # increment all of the times
        for i in range( 0, num_frames, 1 ):
            page_time[i] = page_time[i] + 1


        # if there is a page fault, replace the value that hasn't been used
        # the longest
        if fault_flag == True:
            max_time = -1
            max_index = -1
            for i in range( 0, num_frames, 1 ):
                if page_time[i] > max_time:
                    max_time = page_time[i]
                    max_index = i

            # replace it
            page_time[max_index] = 1
            page_table[max_index] = val
            
        # print the current page table to the display
        # print the ref val on the top
        cantext = pr_canvas.create_text( x_pos, y_pos[0], text = str( val ) )
        for fuck in range( 0, len( page_table ), 1 ):
            if page_table[fuck] != -1:
                cantext = pr_canvas.create_text( x_pos, y_pos[fuck+1], text = str( page_table[fuck] ) )
        
        # if there was a page fault, write it at the bottom of the page table
        if fault_flag == True:
            cantext = pr_canvas.create_text( x_pos, y_pos[len( page_table ) + 1], text ="PF" )

        # increment the x position
        x_pos = x_pos + 2 * width

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

