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


# function for comparing the values of two dictionaries and a hashed password
def check_hash(hashed_password, dictionary, dictionary2):

    # by default the password has not been found
    success = 0

    # initialising the combined answer variables
    answer1 = ''
    answer2 = ''

    # for each item in the first dictionary
    for i in list(dictionary):
        # for each item in the second dictionary
        for j in list(dictionary2):

            # combine the words
            test = i+j

            # calculate the hash of the combined words
            temp = hashlib.md5(test.encode('UTF-8'))

            # if the hash of the combined words matched the hash of password   
            if temp.digest() == hashed_password.digest():
                # we have found the components of the original password
                answer1 = i
                answer2 = j
                success = 1

    return answer1, answer2, success  







# the main function
if __name__== "__main__":

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

    print('The hashed password is:')
    # print the hash of the password
    print(hashed_password.digest())


    # open the dictionary file and read the lines to create the dictionary lists 
    with open('words_extract.txt') as f:
        dictionary = [line.rstrip() for line in f]
    f.close()

    with open('words_extract.txt') as f:
        dictionary2 = [line.rstrip() for line in f]
    f.close()
    

    
    
    # start of the second algorithm using the cluster algorithm. Start the timer.
    print('Starting timing using the cluster algorithm')

    check_success = 0
    
    # start the timer
    start = time.time()
    
    # split one of the dictionaries into portions based on the number of cores inputted 
    split_dictionary = np.array_split(dictionary, cores)

    # for each core
    for split in range(cores):

        # run the check_hash function over one full dictionary and each of the partial dictionaries
        test_answer1, test_answer2, success = check_hash(hashed_password, split_dictionary[split], dictionary2)

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
    
    print('The cluster algorithm took ' + str(end_timer) + ' seconds')
    
    
    
    
    # start of the first algorithm on an individual process. Start the timer.
    print('Starting timing on an single process')

    # start the timer
    start = time.time()

    # run the check_hash function across the whole of both dictionaries
    test_answer1, test_answer2, success = check_hash(hashed_password, dictionary, dictionary2)

    if success == 1:
        # output the result
        print('The original words were ' + str(test_answer1) + ' and ' + str(test_answer2)) 
    else:
        print('No matches found') 

    # end the timer
    end = time.time()
    end_timer = end-start
    end_timer = float("{0:.5f}".format(end_timer))

    print('The single process algorithm took ' + str(end_timer) + ' seconds')

