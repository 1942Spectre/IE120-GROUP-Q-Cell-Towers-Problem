import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import ast
from Towers import plot_tower_heatmap,get_kernel_1
from Houses import get_houses



sns.set()




outputs = os.listdir("outputs")
sns.set_theme(style="whitegrid", palette="pastel")



if outputs:
    #n_towers \t best_coordinates \t best_rate \t total_tries \n "
    for output in outputs:
        df = pd.read_csv("outputs/" + output,sep="\t")

        plt.clf()
        plt.plot(df["n_towers"] ,df["best_rate"])
        plt.title("BEST POSSIBLE SERVICE RATES")
        plt.xlabel("Number of towers")
        plt.ylabel("Service Rate")
        plt.xticks(np.array(range(0,df["n_towers"].max()+1)))

        plt.savefig( "plots/" + str(output) + "rate_plot.png")

        plt.clf()
        plt.plot(df["n_towers"] ,df["total_tries"])
        plt.title("Number of combinations for each number of towers")
        plt.xlabel("Number of towers")
        plt.ylabel("Service Rate")
        plt.xticks(np.array(range(0,df["n_towers"].max()+1)))

        plt.savefig("plots/" + str(output) + "num_tries_plot.png")

        plt.clf()

        coordinates = df["best_coordinates"]
        coordinates = coordinates.tail(1).values[0]

        coordinates = ast.literal_eval(coordinates)


        heatmap = plot_tower_heatmap(get_houses()  , coordinates ,get_kernel_1() )
        fig = heatmap.get_figure()
        fig.savefig("plots/heatmap" + output + ".png")
        fig.clf()

        
    



        

    


