# Code written by Daniel Gooch for students on the Open University course TM129 in 2019.

# dictionary from Neil Smith at the Open University, available on GitHub, https://github.com/NeilNjae/cipher-tools

# Version 1.0

# used for hash functions
import hashlib
# used for the array manipulation
import numpy as np
# needed for file handling
import os
# used for processing input arguments
import sys
# needed for timing the algorithms
import time
# needed for distributing jobs across the cluster
import dispy
# needed for making the unicorn phat work
from unicornhatmini import UnicornHATMini
import random
import socket



# function for comparing the values of two dictionaries and a hashed password
def check_hash(input_hashed_password, dictionary, dictionary2):

    # used for hash functions
    import hashlib
    # used for the array manipulation
    import numpy as np
    
    
    # by default the password has not been found
    success = 0

    # initialising the combined answer variables
    answer1 = ''
    answer2 = ''

    # for each item in the first dictionary
    for i in list(dictionary2):
        # for each item in the second dictionary
        for j in list(dictionary):

            # combine the words
            test = i+j

            # calculate the hash of the combined words
            temp = hashlib.md5(test.encode('UTF-8'))

            # if the hash of the combined words matched the hash of password   
            if temp.digest() == input_hashed_password:
                # we have found the components of the original password
                answer1 = i
                answer2 = j
                success = 1

    return answer1, answer2, success  



# function for turning the unicorn hat on red
def on():
    u_width, u_height = unicornhatmini.get_shape()
    for x in range(u_width):
        for y in range(u_height):
            unicornhatmini.set_pixel(x,y,255,0,0)
    unicornhatmini.show()

# function for turning the unicorn hat on green
def on_green():
    u_width, u_height = unicornhatmini.get_shape()
    for x in range(u_width):
        for y in range(u_height):
            unicornhatmini.set_pixel(x,y,0,255,0)
    unicornhatmini.show()

# function for turning off the unicorn hat
def off():
    unicornhatmini.clear()
    unicornhatmini.show()



# the main function
if __name__== "__main__":

    # set the unicorn hat up
    unicornhatmini = UnicornHATMini()
    #unicornhatmini.set_layout(unicornhat.PHAT)
    unicornhatmini.set_brightness(0.5)
    
    # inputs must be lower case words
    word1 = sys.argv[1]

    # inputs must be lower case words
    word2 = sys.argv[2]

    # input must be an integer between 2 and 32 inclusive
    cores = int(sys.argv[3])

    # create the password from the two input words
    password = word1 + word2

    # create the hash of the password
    hashed_password = hashlib.md5(password.encode('UTF-8'))

    # print the hash of the password
    print('The hashed password is:')
    print(hashed_password.digest())


    # open the dictionary file and read the lines to create the dictionary lists 
    with open('words_extract.txt') as f:
        dictionary = [line.rstrip() for line in f]
    f.close()

    with open('words_extract.txt') as f:
        dictionary2 = [line.rstrip() for line in f]
    f.close()
    
    
    
    
    
    
    # start of the second algorithm using the cluster algorithm. Start the timer.
    print('Starting timing on the Raspberry Pi cluster')

    # initialise result vars
    test_answer1 = ''
    test_answer2 = ''
    final_answer1 = ''
    final_answer2 = ''
    success = 0
    check_success = 0
    
    # start the timer
    start = time.time()
    
    # turn the unicorn hat on
    on()
    
    # split one of the dictionaries into portions based on the number of cores inputted 
    split_dictionary = np.array_split(dictionary, cores)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    
    # setup the dispy cluster
    cluster = dispy.JobCluster(check_hash, loglevel=dispy.logger.CRITICAL, ip_addr=s.getsockname()[0], nodes='192.168.1.*')

  
    # initalise the array of jobs
    jobs = []
    
    # for each core, create a new dispy job which runs the check_hash function over a segment of the dictionary
    for split in range(cores):
        job = cluster.submit(hashed_password.digest(), split_dictionary[split], dictionary2)
        jobs.append(job)
    cluster.wait() # waits until all jobs finish

        
    # for each completed job
    for job in jobs:
        
        test_answer1, test_answer2, success = job() # waits for job to finish and returns results

        # if success has been found, store the answers
        if success == 1:
            final_answer1 = test_answer1
            final_answer2 = test_answer2
            check_success = 1

    if check_success == 1:
        # output the result
        print('The original words were ' + str(final_answer1) + ' and ' + str(final_answer2)) 
    else:
        print('No matches found')

    # end the timer
    end = time.time()
    end_timer = end-start
    end_timer = float("{0:.5f}".format(end_timer))
    
    print('The Raspberry Pi cluster took ' + str(end_timer) + ' seconds')
    
    
    # make the unicorn hat green for three seconds
    while (time.time() < end +3):
        on_green()
    
    
    
    
    
    
    
    
    
    
    
    

    # start of the first algorithm on an individual process. Start the timer.
    print('Starting timing on an individual Raspberry Pi')

    # turn the unicorn hat on
    on()
    
    # start the timer
    start = time.time()

    # run the check_hash function across the whole of both dictionaries
    test_answer1, test_answer2, success = check_hash(hashed_password.digest(), dictionary, dictionary2)

    if success == 1:
        # output the result
        print('The original words were ' + str(final_answer1) + ' and ' + str(final_answer2)) 
    else:
        print('No matches found')
        
    # end the timer
    end = time.time()
    end_timer = end-start
    end_timer = float("{0:.5f}".format(end_timer))
    
    print('An individual Raspberry Pi took ' + str(end_timer) + ' seconds')

    # make the unicorn hat green for five seconds
    while (time.time() < end + 5):
        on_green()







