# File to visualize the PLQ maps.

# Author: Marco Huber, 2021
# Fraunhofer IGD
# marco.huber[at]igd.fraunhofer.de

import cv2
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm

def process_grad(gradient, a, b):
    
    grad = abs(gradient)
    x = np.mean(grad, axis=2)
    x = 1 - (1 / (1 + (a * x **b)))
    return x

def plot_comparison(grad_save, save_path, a, b, withtitle=True):
    
    # split
    names, grads, score = grad_save[:,0], grad_save[:,1], grad_save[:,2]
             
    # iterate over each gradient set                   
    for idx, g in enumerate(tqdm(grads)):

        axes = []
        fig = plt.figure()
        
        plt.rc('font',size=20)
        
        # plot original image for reference
        img = cv2.imread(names[idx])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (112,112))
        tit = "Image $I$"

        if withtitle == True:
            axes.append(fig.add_subplot(1,2,1, title=tit))
        else:
            axes.append(fig.add_subplot(1,2,1))
        
        subtit = "$\hat{Q}_{I}$: " + str(np.round(score[idx],3))
        
        plt.text(30, 126, subtit, fontsize=24)
        
        plt.xticks([])
        plt.yticks([])
        plt.imshow(img)                           
        
        plt.box(False)
        
        # plot explained image
        title = "PLQ-Map $P(\hat{Q}_{I})$"
        
        if withtitle == True:
            axes.append(fig.add_subplot(1,2,2, title=title))
        else:
            axes.append(fig.add_subplot(1,2,2))
        
        plt.xticks([])
        plt.yticks([])
        plt.imshow(process_grad(g, a, b), cmap=plt.get_cmap('RdYlGn'), vmin=0, vmax=1)

        # save
        save = names[idx].split("/")[-1] 
        plt.tight_layout()
        plt.gca().set_axis_off()
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0.05)
        plt.margins(10,10)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.savefig(save_path + save + ".png", bbox_inches='tight', pad_inches = 0)
        plt.close()
        