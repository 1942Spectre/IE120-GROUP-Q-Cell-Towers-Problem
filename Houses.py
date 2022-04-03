import numpy as np

def get_houses():

    houses = np.zeros((10,10))
    houses[0,2] = 1
    houses[0,4] = 1
    houses[0,5] = 1
    houses[0,7] = 1

    houses[1,0] = 1
    houses[1,4] = 1

    houses[2,3] = 1
    houses[2,5] = 1
    houses[2,6] = 1
    houses[2,8] = 1
    houses[2,9] = 1

    houses[3,4] = 1
    houses[3,6] = 1
    houses[3,8] = 1

    houses[4,2] = 1
    houses[4,5] = 1
    houses[4,6] = 1
    houses[4,7] = 1
    houses[4,8] = 1

    houses[5,0] = 1
    houses[5,3] = 1
    houses[5,4] = 1
    houses[5,6] = 1

    houses[6,0] = 1
    houses[6,1] = 1
    houses[6,2] = 1
    houses[6,3] = 1
    houses[6,4] = 1
    houses[6,9] = 1

    houses[7,4] = 1
    houses[7,6] = 1

    houses[8,0] = 1
    houses[8,2] = 1
    houses[8,6] = 1
    houses[8,7] = 1
    houses[8,9] = 1

    houses[9,0] = 1
    houses[9,4] = 1
    houses[9,5] = 1
    houses[9,8] = 1
    houses[9,9] = 1

    return houses.astype(np.int8)