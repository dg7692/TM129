# Code written by Daniel Gooch for students on the Open University course TM129 in 2019.

# Version 1.0

# needed for array manipulation
import numpy as np
# needed for file handling
import os
# used for processing input arguments
import sys
# needed for timing the algorithms
import time
# needed for generating the route premutations
from itertools import permutations
# needed for making the unicorn phat work
import unicornhat
# needed for distributing jobs across the cluster
import dispy
import random
import socket



# function for calculating the minimum and maximum route distance within a given set of routes
def distance(perm, distance_dictionary, size):

    # function for calculating the distance between two cities
    def calculate_city(city1, city2, distance_dictionary):
        return distance_dictionary[str(city1) + str(city2)]

    # initialise the return variables
    local_minimum_distance = None
    local_minimum_order = None

    local_maximum_distance = None
    local_maximum_order = None

    # for each route in the set of routes
    for i in list(perm):

        # initialise the distance
        summing_distance = 0
        
        # calculate and sum the distance between each adjacent city in the route
        for j in range(size-1):
            summing_distance += calculate_city(i[j], i[j+1], distance_dictionary)

        # and the return leg to the starting city
        summing_distance += calculate_city(i[size-1], i[0], distance_dictionary)

        # if there is no minimum, set the minimum, otherwise check for minimum distance
        if local_minimum_distance is None:
            local_minimum_distance = summing_distance
            local_minimum_order = i

        if summing_distance < local_minimum_distance:
            local_minimum_distance = summing_distance
            local_minimum_order = i

        # if there is no maximum, set the maximum, otherwise check for maximum distance
        if local_maximum_distance is None:
            local_maximum_distance = summing_distance
            local_maximum_order = i

        if summing_distance > local_maximum_distance:
            local_maximum_distance = summing_distance
            local_maximum_order = i

    # return the minimum and maximum distances
    return local_minimum_distance, local_minimum_order, local_maximum_distance, local_maximum_order



# function for turning the unicorn hat on red
def on():
    for x in range(4):
        for y in range(8):
            unicornhat.set_pixel(x,y,255,0,0)
    unicornhat.show()

# function for turning the unicorn hat on green
def on_green():
    for x in range(4):
        for y in range(8):
            unicornhat.set_pixel(x,y,0,255,0)
            unicornhat.show()

# function for turning off the unicorn hat
def off():
    unicornhat.clear()
    unicornhat.show()



# the main function
if __name__== "__main__":

    # input must be an integer between 3 and 9 inclusive
    size = int(sys.argv[1])

    # input must be an integer between 2 and 32 inclusive
    cores = int(sys.argv[2])
    
    # generate the set of all routes
    if size == 3:
        perm = list(permutations([1, 2, 3]))
    elif size == 4:
        perm = list(permutations([1, 2, 3, 4]))
    elif size == 5:
        perm = list(permutations([1, 2, 3, 4, 5]))
    elif size == 6:
        perm = list(permutations([1, 2, 3, 4, 5, 6]))
    elif size == 7:
        perm = list(permutations([1, 2, 3, 4, 5, 6, 7]))
    elif size == 8:
        perm = list(permutations([1, 2, 3, 4, 5, 6, 7, 8]))
    elif size == 9:
        perm = list(permutations([1, 2, 3, 4, 5, 6, 7, 8, 9]))
    elif size == 10:
        perm = list(permutations([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))


    # initialise the mimumum distance and order  
    minimum_distance = None
    minimum_order = None

    # initialise the maximum distance and order  
    maximum_distance = None
    maximum_order = None

    # a list of the distance between two cities
    distance_dictionary = {
        "12": 14,
        "13": 4,
        "14": 9,
        "15": 12,
        "16": 12,
        "17": 4,
        "18": 4,
        "19": 4,
        "110": 4,
        
        "21": 14,
        "23": 8,
        "24": 5,
        "25": 2,
        "26": 13,
        "27": 6,
        "28": 6,
        "29": 6,
        "210": 6,
        
        "31": 4,
        "32": 8,
        "34": 7,
        "35": 11,
        "36": 2,
        "37": 8,
        "38": 8,
        "39": 8,
        "310": 8,
        
        "41": 9,
        "42": 5,
        "43": 7,
        "45": 2,
        "46": 10,
        "47": 2,
        "48": 2,
        "49": 2,
        "410": 2,
        
        "51": 12,
        "52": 2,
        "53": 11,
        "54": 2,
        "56": 14,
        "57": 6,
        "58": 6,
        "59": 6,
        "510": 6,
        
        "61": 12,
        "62": 13,
        "63": 2,
        "64": 10,
        "65": 14,
        "67": 5,
        "68": 5,
        "69": 5,
        "610": 5,

        "71": 4,
        "72": 6,
        "73": 8,
        "74": 2,
        "75": 6,
        "76": 5,
        "78": 16,
        "79": 16,
        "710": 16,

        "81": 4,
        "82": 6,
        "83": 8,
        "84": 2,
        "85": 6,
        "86": 5,
        "87": 16,
        "89": 13,
        "810": 2,

        "91": 4,
        "92": 6,
        "93": 8,
        "94": 2,
        "95": 6,
        "96": 5,
        "97": 16,
        "98": 13,
        "910": 4,

        "101": 4,
        "102": 6,
        "103": 8,
        "104": 2,
        "105": 6,
        "106": 5,
        "107": 16,
        "108": 2,
        "109": 4,

    }






# start the timing on the cluster algorithm
    print('Starting timing on the Raspberry Pi cluster')
    start = time.time()

    # turn the lights on
    on()

    # divide the set of all routes up by the number of cores
    split_array1 = np.array_split(perm, cores)
    

    # initialise the return variables
    return_minimum_distance = []
    return_minimum_order = []
    return_maximum_distance = []
    return_maximum_order = []

    return_minimum_index = None
    return_maximum_index = None


    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    

    # setup the dispy cluster
    cluster = dispy.JobCluster(distance, loglevel=dispy.logger.CRITICAL, ip_addr=s.getsockname()[0], nodes='192.168.1.*')

    # initalise the array of jobs
    jobs = []
    
    # for each core, create a new dispy job which runs the distance function over a segment of the set of routes
    for split in range(cores):
        job = cluster.submit(split_array1[split], distance_dictionary, size)
        jobs.append(job)
    cluster.wait() # waits until all jobs finish

   
    # for each completed job
    for job in jobs:
        
        return_minimum_distance_a, return_minimum_order_a, return_maximum_distance_a, return_maximum_order_a = job() # waits for job to finish and returns results
        
        # save the minimum and maximum result from that job
        return_minimum_distance.append(return_minimum_distance_a)
        return_minimum_order.append(return_minimum_order_a)
        return_maximum_distance.append(return_maximum_distance_a)
        return_maximum_order.append(return_maximum_order_a)



    # for each of the returned minimums/maximums, find the minimum and maximum
    for j in range(len(return_minimum_distance)):
        
        if minimum_distance is None:
            minimum_distance = return_minimum_distance[j]
            return_minimum_index = j

        if return_minimum_distance[j] is not None:
            if return_minimum_distance[j] < minimum_distance:
                minimum_distance = return_minimum_distance[j]
                return_minimum_index = j

        if maximum_distance is None:
            maximum_distance = return_maximum_distance[j]
            return_maximum_index = j

        if return_maximum_distance[j] is not None:
            if return_maximum_distance[j] > maximum_distance:
                maximum_distance = return_maximum_distance[j]
                return_maximum_index = j
      

    # output the results
    print('Minimum distance is ' + str(minimum_distance))
    print('On route ' + str(return_minimum_order[return_minimum_index]))

    print('Maximum distance is ' + str(maximum_distance))
    print('On route ' + str(return_maximum_order[return_maximum_index]))


    # end the timer
    end = time.time()
    end_timer = end-start
    end_timer = float("{0:.5f}".format(end_timer))
    
    print('The Raspberry Pi cluster took ' + str(end_timer) + ' seconds')


    # make the unicorn hat green for three seconds
    while (time.time() < end +3):
        on_green()
    








    print('Starting timing on an individual Raspberry Pi')
    start = time.time()
    
    # turn the unicorn hat on
    on()

    # calculate the minimum across all potential routes
    minimum_distance, minimum_order, maximum_distance, maximum_order = distance(perm, distance_dictionary, size)

    
    # output the answer
    print('Minimum distance is ' + str(minimum_distance))
    print('On route ' + str(minimum_order))

    print('Maximum distance is ' + str(maximum_distance))
    print('On route ' + str(maximum_order))

    # end the timer
    end = time.time()
    end_timer = end-start
    end_timer = float("{0:.5f}".format(end_timer))
    
    print('An individual Raspberry Pi took ' + str(end_timer) + ' seconds')

    # make the unicorn hat green for five seconds
    while (time.time() < end + 5):
        on_green()

