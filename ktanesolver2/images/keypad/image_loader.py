import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

BASE_DIR = os.path.dirname(__file__)

def loadimage(items:list|int):
    if isinstance(items, int): items = [items]
    
    image_paths = [os.path.join(BASE_DIR, f"{a}.png") for a in items]
    images = [mpimg.imread(a) for a in image_paths]
    
    if len(items)==6:
        fig,axes = plt.subplots(2,3)
        axes = axes.flatten()
        for i,ax in enumerate(axes):
            if i<len(images):
                ax.imshow(images[i])
                ax.set_title(f'Maze: {items[i]}')
                ax.set_xticks([]) 
                ax.set_yticks([]) 
                ax.set_xticklabels([]) 
                ax.set_yticklabels([]) 
                ax.set_frame_on(False)
            else: ax.axis('off')
        plt.tight_layout()
    else:
        plt.figure(figsize=(5,5))
        plt.imshow(images[0])
        plt.title(f'Maze: {items[0]}')
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.box(False)
    plt.show()