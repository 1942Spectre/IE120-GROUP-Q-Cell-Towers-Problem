
import numpy as np
from itertools import combinations
import datetime
from Houses import get_houses
import seaborn as sns
from alive_progress import alive_bar



table = np.zeros((10,10)).astype(np.uint16)



def get_all_possible_coordinates(table):
    coordinates = []
    for x in range(1,table.shape[0] - 1):
        for y in range(1,table.shape[1] - 1):
            coordinates.append((x,y))
    return np.array(coordinates).astype(np.uint16)
all_coordinates = get_all_possible_coordinates(table)
        


def get_n_combinations_of_coordinates(n,coordinates):
    return np.array(list(combinations(coordinates,n))).astype(np.uint16)
    
    

def get_kernel_1():
    return np.array([[100,100,100],[100,100,100],[100,100,100]]).astype(np.uint16)

def get_kernel_2():
    return np.array([[50,50,50],[50,100,50],[50,50,50]]).astype(np.uint16)

def plot_tower_heatmap(houses,tower_coordinates,kernel):

    temp_table = apply_kernels(tower_coordinates,kernel,table)
    temp_table = np.clip(temp_table , 0 , 100)

    
    temp_houses = (temp_table * houses).astype(np.uint16)

    for coordinate in tower_coordinates:
        x = coordinate[0]
        y = coordinate[1]
        temp_houses[x,y] = 200
    houses = houses*20 + temp_houses
    heatmap = sns.heatmap(houses)
    return heatmap

        



### This Function Applies the specified kernel into the table it took
## As a parameter and returns the new table
def apply_kernel(x,y,table,kernel):
    table[x-1,y-1] = table[x-1,y-1] + kernel[0,0]
    table[x,y-1] = table[x,y-1] + kernel[1,0]
    table[x+1,y-1] = table[x+1,y-1] + kernel[2,0]

    table[x-1,y] = table[x-1,y] + kernel[0,1]
    table[x,y] = table[x,y] + kernel[1,1]
    table[x+1,y] = table[x+1,y] + kernel[2,1]

    table[x-1,y+1] = table[x-1,y+1] + kernel[0,1]
    table[x,y+1] = table[x,y+1] + kernel[1,1]
    table[x+1,y+1] = table[x+1,y+1] + kernel[2,1]

    return table.astype(np.uint16)


def apply_kernels(coordinates,kernel,table):
    for coordinate in coordinates:
        ## Get the x and y coordinate of each tower
        x = coordinate[0]
        y = coordinate[1]

        ## Apply the kernel to the table
        table = apply_kernel(x,y,table,kernel)
    return table.astype(np.uint16)

def create_output(n_towers_values,best_coordinates,bests,total_tries):
    tsv_string = "n_towers\tbest_coordinates\tbest_rate\ttotal_tries\n"
    for i in range(0,len(bests)):
        tsv_string = tsv_string + f"{n_towers_values[i]}\t{str(best_coordinates[i].tolist())}\t{bests[i]}\t{total_tries[i]}\n"
    output_folder_name = f"outputs/output_{str(datetime.datetime.now()).replace(' ','-').replace(':','-').split('.')[0]}.tsv"
    with open(output_folder_name,"w+") as file:
        file.write(tsv_string)
    return





def solve(target_rate,kernel,max_n_towers):


    houses = get_houses()


    ## 41*0.7 = 28.7
    target = np.sum(houses) * target_rate
    ## We need at least that amount to achieve the target

    ## Save the best service rate for each number of towers 
    # To be able to visualize it for the report
    bests = []
    best_coordinates = []
    total_tries = []
    n_towers_values = []
    ## INCREASE THE NUMBER OF TOWERS IF TARGET IS NOT ACHIEVED
    for n_towers in range(1,max_n_towers + 1):
        best_rate = 0
        ## GET THE POSSİBLE COORDINATE COMBINATIONS
        possible_coordinate_combinations = get_n_combinations_of_coordinates(n_towers,all_coordinates)
        print(f"Going to try {possible_coordinate_combinations.shape} coordinates for n_towers = {n_towers}")

        ## ITERATE FOR EVERY COORDINATE COMBINATION
        for combination in possible_coordinate_combinations:

            ################################################
            ######### MAIN OPERATION #######################
            ################################################
            temp_table = table.copy()
            temp_table = apply_kernels(combination,kernel,temp_table)
            ## If there is a value bigger than 100 in the table, clip it to 100 (maximum service)
            temp_table = np.clip(temp_table, 0 , 100)
            ## Cross Product of the temp table and the houses will result in 
            ## cells with service which also contain a house will contain the service rate
            ## every other cell will contain zeros.
            ## We divide the sum of this matrix by 100 to get the number of cells that has service
            ## We divide the result by the number of houses to get the rate of cells with service
            rate = np.sum(temp_table * houses / 100)
            ################################################
            ################################################


            ## If the last recorded best rate is less than the current rate
            best_rate = rate if (best_rate < rate) else best_rate

            ################################################
            ####################### SUCCESS CHECK
            ################################################
            if rate >= target:
                tower_table = np.zeros(temp_table.shape)
                for coordinate in combination:
                    x = coordinate[0]
                    y = coordinate[1]
                    tower_table[x,y] = 1

                
                print(tower_table)
                ## Print the coordinates if it has and exit from the function
                print(combination)
                
                bests.append(rate/np.sum(houses) * 100)
                best_coordinates.append(combination)
                total_tries.append(len(possible_coordinate_combinations))
                n_towers_values.append(n_towers)

                # Create a tsv table for the records
                create_output(n_towers_values,best_coordinates,bests,total_tries)
                return

        
        
        ## Save the best rate acquired with the past number of towers to the bests list to be able to visualize the best rates of each n_towers
        bests.append(rate/np.sum(houses) * 100)
        best_coordinates.append(combination)
        total_tries.append(len(possible_coordinate_combinations))
        n_towers_values.append(n_towers)

        ## Save the coordinates which have reached the highest rate with given n_towers
        ## Print that no solution found for that number of towers 
        print(f"Could not find a solution for n_towers = {n_towers}")

    # Create a tsv table for the records
    create_output(n_towers_values,best_coordinates,bests,total_tries)


        
        
        
if __name__ == "__main__":
    try:
        solve(0.7,get_kernel_2(),10)
    except Exception as e:
        with open("log1.txt","w+") as file:
            file.write("Error on case 2" + "\n" + e)
    try:
        solve(0.9,get_kernel_1(), 20)
    except Exception as e:
        with open("log1.txt","w+") as file:
            file.write("Error on case 3"  + "\n" + e)
    try:
        solve(0.9,get_kernel_2(), 30)
    except Exception as e:
        with open("log1.txt","w+") as file:
            file.write("Error on case 4"  + "\n" + e)
        
    
    

