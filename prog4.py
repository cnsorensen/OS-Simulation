from Tkinter import *
from ttk import *
import random
import time
from PIL import Image, ImageTk

################################# MEMORY MANAGEMENT ################################
def mm_generate( mem_size, tlb_size, accesses ):

    # times to get to memory from TLB or page table, time to get to page table
    # from tlb, and time from CPU to TLB
    mem_time = 100
    tlb_time = 20
    pagetable_time = 100

    # print these times to the screen
    mm_canvas.insert( END, 'Time to TLB from CPU: ' + str( tlb_time ) + ' ns\n' )
    mm_canvas.insert( END, 'Time to Page Table from CPU: ' + str( pagetable_time ) + ' ns\n' )
    mm_canvas.insert( END, 'Time to Memory from TLB or Page Table: ' + str( mem_time ) + ' ns\n\n' )

    # create the tlb
    tlb = {}
    for i in range( 0, tlb_size, 1 ):
        tlb[i] = -1
    # create the fifo count for it
    tlb_fifo = {}
    for i in range( 0, tlb_size, 1 ):
        tlb_fifo[i] = -1    

    # initialize the EAT
    num_hit = 0
    num_miss = 0
    num_access = 0
    hit_ratio = 0
    miss_ratio = 0
    eat = 0

    # text outputs
    hit_str = "TLB hit."
    miss_str = "TLB miss."
    go_tlb = "Going to TLB."
    go_pt = "Going to page table."
    go_pm = "Going to memory."
    
    # run the number of accesses
    for i in range( 0, accesses, 1 ):
        # flag for if in tlb
        found_flag = False

        # flag for if it's inserted
        insert_flag = False

        # increase number of accesses
        num_access = num_access + 1

        # pick a page
        p = random.randint( 0, mem_size - 1 )
        p_str = "Accessing page " + str( p )
        # print that you're accessing a page
        #mm_canvas.insert( END, p_str + '\n')
        print p_str   

        # search the TLB for p
        for page in tlb:
            if tlb[page] == p:
                found_flag = True
                break

        # p was found in the TLB
        if found_flag == True:
            # print the tlb hit
            #mm_canvas.insert( END, hit_str + '\n')
            print hit_str

            # increment the number of hits
            num_hit = num_hit + 1

        else:
            # print the tlb miss
            #mm_canvas.insert( END, miss_str )
            print miss_str

            # increment the number of misses
            num_miss = num_miss + 1

            # print that you're going to the page table
            #mm_canvas.insert( END, go_pt )
            print go_pt

            # print that you're going to physical memory
            #mm_canvas.insert( END, go_pm )
            print go_pm

            # add p to the tlb
            # print that you're inserting p to the tlb
            insert_str = "Inserting " + str( p ) + " into TLB."
            #mm_canvas.insert( END, insert_str + '\n')
            print insert_str

            for i in range( 0, tlb_size, 1 ):
                # find an empty spot first
                if tlb[i]== -1:
                    # insert it
                    tlb[i] = p
                    tlb_fifo[i] = 0
                    insert_flag = True
                    break                    
            # if there wasn't an empty spot to insert, do the fifo replace
            if insert_flag == False:
                max_time = -1
                max_index = -1
                # find the oldest one there
                for i in range( 0, tlb_size, 1 ):
                    if tlb_fifo[i] > max_time:
                        max_time = tlb_fifo[i]
                        max_index = i
                # insert it
                tlb_fifo[max_index] = 0
                tlb[max_index] = p

        # increment on the times in the tlb
        for i in range( 0, tlb_size, 1 ):
            tlb_fifo[i] = tlb_fifo[i] + 1

        # calculate the eat
        hit_ratio = float( num_hit ) / float( num_access )
        miss_ratio = float( num_miss ) / float( num_access )
        eat = ( hit_ratio * ( tlb_time + mem_time ) ) + ( miss_ratio * ( tlb_time + pagetable_time + mem_time ) )

        # print eat
        eat_str = "EAT = " + str( eat ) + " ns\n"
        #mm_canvas.insert( END, eat_str )
        print eat_str
    
    print 'Total TLB Hits: ' + str( num_hit )
    print 'Total TLB Misses: ' + str( num_miss )
    print 'Total accesses: ' + str( num_access )
    print 'Final EAT: ' + str( eat ) + 'ns'

    mm_canvas.insert( END, 'Total TLB Hits: ' + str( num_hit ) + '\n' )
    mm_canvas.insert( END, 'Total TLB Misses: ' + str( num_miss ) + '\n' )
    mm_canvas.insert( END, 'Total accesses: ' + str( num_access ) + '\n' )
    mm_canvas.insert( END, 'Final EAT: ' + str( eat ) + ' ns\n\n' )

############################ PAGE REPLACEMENT #######################################
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
        can_box = pr_canvas.create_rectangle( x1_1 * width, width, x1_2 * width, 
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

        # initalize the fault flag to true
        fault_flag = True
        insert_flag = False

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
                insert_flag = True
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
        if fault_flag == True or insert_flag == True:
            cantext = pr_canvas.create_text( x_pos, y_pos[len( page_table ) + 1], text ="PF" )

        # increment the x position
        x_pos = x_pos + 2 * width

################################ OPTIMAL #############################################
def draw_pr_optimal( num_frames, num_refs, ref_string ):

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

        # initalize the fault flag to true
        fault_flag = True
        insert_flag = False

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
                insert_flag = True
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
        if fault_flag == True or insert_flag == True:
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

    # the x position for the text
    x_pos = 1 * width + width / 2

    # go through the ref string
    for val in ref_string:

        # initalize the fault flag to true
        fault_flag = True
        insert_flag = False

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
                insert_flag = True
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
            for i in range( 0, num_frames, 1 ):
                # if it's the least recently used
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
        if fault_flag == True or insert_flag == True:
            cantext = pr_canvas.create_text( x_pos, y_pos[len( page_table ) + 1], text ="PF" )

        # increment the x position
        x_pos = x_pos + 2 * width

####################################### LFU ##########################################
def draw_pr_lfu( num_frames, num_refs, ref_string ):

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

    # the x position for the text
    x_pos = 1 * width + width / 2

    # go through the ref string
    for val in ref_string:

        # initalize the fault flag to true
        fault_flag = True
        insert_flag = False

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
                insert_flag =True
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
                    min_freq = page_freq[i]
                    min_index = i

            # replace it
            page_freq[min_index] = 1
            page_table[min_index] = val

        # print the current page table to the display
        # print the ref val on the top
        cantext = pr_canvas.create_text( x_pos, y_pos[0], text = str( val ) )
        for fuck in range( 0, len( page_table ), 1 ):
            if page_table[fuck] != -1:
                cantext = pr_canvas.create_text( x_pos, y_pos[fuck+1], text = str( page_table[fuck] ) )
        
        # if there was a page fault, write it at the bottom of the page table
        if fault_flag == True or insert_flag == True:
            cantext = pr_canvas.create_text( x_pos, y_pos[len( page_table ) + 1], text ="PF" )

        # increment the x position
        x_pos = x_pos + 2 * width


####################################### NRU ##########################################
def draw_pr_nru( num_frames, num_refs, ref_string ):

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

        # initalize the fault flag to true
        fault_flag = True
        insert_flag = False

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
                insert_flag = True
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
        if fault_flag == True or insert_flag == True:
            cantext = pr_canvas.create_text( x_pos, y_pos[len( page_table ) + 1], text ="PF" )

        # increment the x position
        x_pos = x_pos + 2 * width

# Sets up the GUI
def gui():
    # set up the window
    root = Tk()
    # title of the window
    root.title( "Simulation Project" )
    # set the size of the window
    #root.geometry( "900x500" )
    root.geometry( "1000x1000" )
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

######################################## FRAME 1 #########33#######################
# Process Scheduler tab
def frame1():	
    top = Frame(one)
    left = Frame(one)
    left.pack(side=LEFT)
    top.pack(side=TOP)

    sc_canvas = Text( one, width = 75, height = 50 )
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
        ganttchart = ""  
        

        if selection.get() == 3:  # shortest job first
            for i in processList:
                remainingTime.append(int(i[2]))
            print remainingTime
            for i in sorted(sorted(processList, key=itemgetter(1)), key=itemgetter(2)):
                for j in range(0, int(i[2])):
                    ganttchart += "| " + i[0] + " "


        if selection.get() == 2: # priority scheduling
            for i in sorted(processList, key=itemgetter(3)):
                for j in range (0, int(i[2])):
                    ganttchart += "| " + i[0] + " "

        if selection.get() == 1: # round robin
            totalslices = 0
            remainingTime = []
            for i in processList:
                totalslices += int(i[2])
            totalslices /= int(processList[0][4])
            for i in processList:
                if int(i[2]) > 0:
                    for j in range (0, int(processList[0][4])):
                        ganttchart += "| " + i[0] + " "
                    next = int(i[2]) - 2
                    if next < 0:
                        next = 0
                    processList.append(list((i[0], "fill", next)))

        ganttchart += "\n\n\n"
        sc_canvas.insert(END, ganttchart)


    def add():
        t.insert(END,  processid.get() + "\t|\t" + arrivTime.get() + "\t|\t" + burstTime.get() + "\n")
        processList.append(list((processid.get(), arrivTime.get(), burstTime.get(), priority.get(), timeslice.get())))

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

################################# FRAME 2 ###########################################
# Memory Management Unit tab
def frame2():
    top = Frame( two )
    top.pack( side = TOP )
    top2 = Frame( two )
    top2.pack( side = TOP )
    top3 = Frame( two )
    top3.pack( side = TOP )
    middle = Frame( two )
    middle.pack( side = LEFT )

    # Values for the radio buttons
    mem_sizes = [
        ( "10", 10 ),
        ( "15", 15 ),
        ( "20", 20 )
    ]

    tlb_sizes = [
        ( "5", 5 ),
        ( "6", 6 ),
        ( "7", 7 ),
        ( "8", 8 ),
        ( "9", 9 ),
    ]

    num_accesses = [
        ( "50", 50 ),
        ( "100", 100 ),
        ( "150", 150 ),
        ( "200", 200 )
    ]

    # label for the number of frames in memory
    mem_size_L = Label( top, text = 'Number of frames in memory:' )
    mem_size_L.pack()

    # radio buttons to select the size of memory
    mem_size = IntVar()
    # initalize it
    mem_size.set("15")
    # add each button to the display
    for text, mode in mem_sizes:
        mem_size_b = Radiobutton( top, text = text, variable = mem_size, value = mode )
        mem_size_b.pack( side = LEFT )
    
    # label for the size of TLB
    tlb_size_L = Label( top2, text = 'Size of TLB:' )
    tlb_size_L.pack()

    # radio buttons to select the size of memory
    tlb_size = IntVar()
    # initalize it
    tlb_size.set("5")
    # add each button to the display
    for text, mode in tlb_sizes:
        tlb_size_b = Radiobutton( top2, text = text, variable = tlb_size, value = mode )
        tlb_size_b.pack( side = LEFT )

    # label for the number of accesses
    tlb_size_L = Label( top3, text = 'Number of Accesses:' )
    tlb_size_L.pack()

    # radio buttons for the number of accesses
    num_access = IntVar()
    # initalize it
    num_access.set("25")
    # add each button to the display
    for text, mode in num_accesses:
        num_access_b = Radiobutton( top3, text = text, variable = num_access, value = mode )
        num_access_b.pack( side = LEFT )


    # the image of the paging hardware in the window
    image = Image.open( "paginghardware.jpg" )
    image = image.resize( (350, 250 ), Image.ANTIALIAS )
    photo = ImageTk.PhotoImage( image )
    photo_L = Label( middle, image = photo )
    photo_L.image = photo
    photo_L.pack()

    # generate button to submit for memory management
    mm_generate_b = Button( two, text = "Generate",
        command = lambda: mm_generate( mem_size.get(), tlb_size.get(), num_access.get() ) )
    mm_generate_b.pack()

    # canvas to write the text
    #mm_canvas = Canvas( two, width = 500, height = 500 )
    #mm_canvas.pack()

    mm_canvas = Text( two, width = 75, height= 50 )
    mm_canvas.pack()

    return mm_generate_b, mm_canvas

############################### FRAME 3 ###########################################
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

    root,one,two,three = gui()
    frame1()
    mm_generate_b, mm_canvas = frame2()
    pr_generate_b, pr_canvas = frame3()

    root.mainloop()

