# Code written by Daniel Gooch for students on the Open University course TM129 in 2019.

# Version 1.0


# imports image processing functions
from PIL import Image
# needed for some of the array manipulation
import numpy as np
# needed for file handling
import os
# needed for processing inputs
import sys
# needed for timing the algorithms
import time

# output array. Global variable to assist with the clustering processing
global output

# needed for using multiple cores
import multiprocessing as mp




# function for comparing three arrays and returning the median values
def median(input_array):

    unpack = np.array_split(input_array, 3, axis=3)
    
    array1 = unpack[0]
    array2 = unpack[1]
    array3 = unpack[2]
   
    #len(split_array1[split]), len(split_array1[split][0])

    size = len(array1)
    size2 = len(array1[0])
    
    # initialises an ouput array of the correct size
    local_output = np.arange(size*size2*4).reshape(size,size2,4)

    # for each pixel in the x dimension
    for x in range(size):
        # for each pixel in the y dimension
        for y in range(size2):
            # for each pixel value RGBA
            for z in range(4):

                # get the pixel value form each image
                a = array1[x][y][z]
                b = array2[x][y][z]
                c = array3[x][y][z]

                # find the median pixel value
                if a > b:
                    if a < c:
                        median = a
                    elif b > c:
                        median = b
                    else:
                        median = c
                else:
                    if a > c:
                        median = a
                    elif b < c:
                        median = b
                    else:
                        median = c
            
                # set the output to the median pixel value
                local_output[x][y][z] = median
                
    # return the processed image array
    return local_output 



# this is the starting function
if __name__== "__main__":

    # read in how many cores to run across the cluster. Must be a value between 2 and 32 [7 * 4-core Raspberry pis] + additional
    cores = int(sys.argv[4])
    
    # open three images and treat them as arrays of pixels iar1, iar2 and iar3 [short for imageArray1 etc]
    i1 = Image.open(str(sys.argv[1]))
    iar1 = np.asarray(i1)
    i1.close()

    
    i2 = Image.open(str(sys.argv[2]))
    iar2 = np.asarray(i2)
    i2.close()

    i3 = Image.open(str(sys.argv[3]))
    iar3 = np.asarray(i3)
    i3.close()
    
    
    
    
    
    # start of the first algorithm on an individual process. Start the timer.
    print('Starting timing on an individual process')
    start = time.time()

    # stack the images so that they can be passed as a single parameter    
    stacked = np.stack((iar1, iar2, iar3), axis=3)    
    
    output = median(stacked)
    


    # output the output array as a png
    if os.path.exists("output1.png"):
        os.remove("output1.png")

    output = output.astype('uint8')

    new_im = Image.fromarray(output, 'RGBA')
    new_im.save("output1.png")

    # end the timer
    end = time.time()
    end_timer = end-start
    end_timer = float("{0:.5f}".format(end_timer))

    print('The single process algorithm took ' + str(end_timer) + ' seconds')



    

    
    
    
    
    
    # start of the second algorithm using the cluster algorithm. Start the timer.
    print('Starting timing using the cluster algorithm')
    start = time.time()
    
    # stack the images so that they can be passed as a single parameter    
    stacked = np.stack((iar1, iar2, iar3), axis=3)    
    
    # split the stacked images
    stacked_split = np.array_split(stacked, cores)
    
    # generate the multiprocessing processes and get the results
    pool = mp.Pool(processes=cores)
    results = pool.map(median, stacked_split)
    
    # combine the results into an image array of the correct dimensions
    output = np.concatenate(results, axis=0)
        

    # output the output array as a png
    if os.path.exists("output2.png"):
        os.remove("output2.png")

    output = output.astype('uint8')

    new_im = Image.fromarray(output, 'RGBA')
    new_im.save("output2.png")

    
    # end the timer
    end = time.time()
    end_timer = end-start
    end_timer = float("{0:.5f}".format(end_timer))

    print('The cluster algorithm took ' + str(end_timer) + ' seconds')
    
    
    
    
    
    

