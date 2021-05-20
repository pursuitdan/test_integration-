import os
import sys
import time
import sqlite3

# file -> buffer
def stream_sender(filename, buffer, count):
    #info('sender')
    sent_ct = 0 
    with open(filename,'r') as f:
        for line in f:
            line = line.rstrip()   # strip white space
            words = line.split()   # split string into a list of words
            if len(words) == 3:    # only take lines with desired information
                    buffer.add(words)
                    sent_ct += sys.getsizeof(words)   # take bit size of records
    count.put(sent_ct)

    # acknowledge to the log that stream_receiver has stopped 
    # sending new inputs to the buffer
    print('ALERT: stream_sender stopped sending packets')
    print('STATS: sent tuples: {}'.format(sent_ct))


# given a shared buffer, stream_receiver reads the 
# buffer and inserts the buffer items into the database
# the process stops after 5 seconds of no new insertions
# into the empty buffer
#    buffer = a instance of the Buffer class to read
#    wait = the time in seconds to wait before reading again
#         after reading an empty buffer 
#    max_time = the max number of seconds to wait for a new buffer 
#         entry before terminating the process
#    buffers - buffer array rotate on
def stream_receiver(buffers,sm,wait,max_time):
        #info('receiver')

        # open a connection with the DB
        conn = sqlite3.connect('test.db')
        cur = conn.cursor()

        # keep track of the # of consecutive times the buffer was empty 
        # when attempting to be read
        empty_ct = 0 

        # keep track of the number of packets read out of the buffer
        read_ct = 0
        print('streaming start: {}'.format(time.time()))

        while empty_ct < max_time: 
            for buffer in buffers:  # rotate on buffers
                # attempt to read from the buffer
                if buffer.ready():
                    #print('reader buff state: {}'.format(buffer))
                    buff_item = buffer.remove()
                    buff_item.append(read_ct) #append an ID to the buffer item
                    cur.execute('INSERT INTO uniqueMAC1 (TX, RX, SNR, ID) VALUES (?, ?, ?, ?)',buff_item)
                    conn.commit() #we need to commit here or else the read values will not be seen by a parallel connection
                    empty_ct = 0 #reset the empty ct
                    read_ct += 1 
                else: 
                    #print('nothing to read')
                    time.sleep(wait)
                    empty_ct += 1 

        # notify the analysis function that the stream has ended
        sm.stop(read_ct)

        # TODO - is this the best setup for when to commit? 
        conn.commit()
        cur.close()
        conn.close()

        # acknowledge to the log that stream_receiver has stopped 
        # receiving new inputs to the buffer
        print('ALERT: steam_reciever stopped receiving packets')
        print('STATS: buffer empty: {} | read tuples: {}'.format(not buffer.ready(),read_ct))
        print('streaming end: {}'.format(time.time()))

# the realtime analysis runs a user-defined query / analsis on the data 
# after it has been entered into the database
def realtime_analysis(db_name, sm):

     print('analysis start: {}'.format(time.time()))
     f = open("analysis_results.txt", "w")

     # continue querying until stream stops
     while sm.sending(): 
          analysis(f)
          time.sleep(1) #try to read new data every 5 seconds

     f.close()
     print('analysis end: {}'.format(time.time()))