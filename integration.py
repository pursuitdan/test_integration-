import mxnet
#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import os
import sys
import time
import math
import multiprocessing
from multiprocessing import Process, Queue, Pool, Manager

from buffer import Buffer
from sync_manager import SyncManager
from db_utils import create_table_db,log_results,read_all_records_db,analysis
from workers import stream_sender, stream_receiver, realtime_analysis
from helper import file_iterations, split_file, visualize

def interagtion_test(num_senders):
    
    print("---- Number of senders:", num_senders)

    # setup the test variables
    origin_file = 'filedata.txt'
    genera_file = 'newfile.txt'
    splited_files = 'split_file'
    output_size = 100000
    wait_time = 1
    max_time = 5
    db_name = 'test.db'

    # make larger file and split file
    file_iterations(origin_file, output_size, genera_file)
    files = []                                              # create a array of splited file names to hold splited files
    for i in range(num_senders):
        files.append('%s%d.txt' % (splited_files, i))
    split_file(num_senders, genera_file, splited_files)     # split large file into # of files = num_sender
    
    # create buffers array, one buffer for each process
    # each buffer managed by the shared memory manager
    buffers = []
    for i in range(num_senders):
        buffers.append(Buffer())
        buffers[i].index.value = i

    #create a sync manager to share info between the receiver and the analytics
    sm = SyncManager()

    #setup the database
    create_table_db(db_name)

    #### invoke multiple senders
    
    sender_pool = []    # pool for collecting sender process
    sent_ct = Queue()   # sent_ct - use shared memory Queue to store # of records processed

    start = time.time() # start latency measurement

    for i in range(num_senders): 
        p = Process(target = stream_sender, args = (files[i], buffers[i], sent_ct)) # senders
        p.start()
        sender_pool.append(p)

    reader = Process(target=stream_receiver, args=(buffers,sm,wait_time,max_time))  # receivers
    # analytics = Process(target=realtime_analysis, args=(db_name,sm))
    reader.start()
    # analytics.start()

    for p in sender_pool:
        p.join()
    reader.join()
    # analytics.join()

    t = time.time() - start # end latency measurement

    # attempt to read the database for the intial entries (this will eventually be PART 2)
    log_results(read_all_records_db(db_name))

    # end & clean up
    for i in range(num_senders):
        os.remove(files[i])

    total_bytes = 0                     
    while not sent_ct.empty():
        total_bytes += sent_ct.get()    # total memory size of data streamed into buffer
    total_Bytes = total_bytes/1000
    
    return t, total_Bytes

if __name__ == '__main__':

    num_senders = [1, 2, 3]
    times = []
    for n in num_senders:
        result = interagtion_test(n)
        print("time: ", result[0])
        print("data processed (Bytes): ", result[1])

    print("\nTimes: ", times)
