import os
import math
import numpy
import matplotlib.pyplot as plt


def file_iterations(filename, output_size, out_file):
    f = os.stat(filename)
    loops = math.floor(output_size/f.st_size)
    print("Need iteration: ", loops)

    with open(out_file, 'w') as outfile:
        for x in range(0, loops):
            with open(filename) as infile:
                outfile.write(infile.read())
    print("Large file produced.")

# helper function to split file
def split_file(num_workers, infile, outfile):
    with open(infile) as input:
        files = [open('%s%d.txt' % (outfile,i), 'w') for i in range(num_workers)]
        for i, line in enumerate(input):
            files[i % num_workers].write(line)
        for f in files:
            f.close()

# visualize data rate
def visualize(times, num_p, Bytes):
    times = numpy.array(times)
    Bytes = numpy.array(Bytes)
    rate = numpy.divide(Bytes, times)
    plt.plot(num_p, rate)
    plt.ylabel("KBps")
    plt.xlabel("Number of Processes")
    plt.savefig('data_rate.png')


