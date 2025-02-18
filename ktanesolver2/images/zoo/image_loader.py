import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

BASE_DIR = os.path.dirname(__file__)

def _loadimage(items:list):
    image_paths = [os.path.join(BASE_DIR, f"{a}.png") for a in items]
    images = [mpimg.imread(a) for a in image_paths]
    fig,axes = plt.subplots(1,6) if len(items)!=18 else plt.subplots(3,6)
    axes = axes.flatten()
    for i,ax in enumerate(axes):
        if i<len(images):
            ax.imshow(images[i])
            ax.set_title(f'{items[i].capitalize()}')
            ax.set_xticks([]) 
            ax.set_yticks([]) 
            ax.set_xticklabels([]) 
            ax.set_yticklabels([]) 
            ax.set_frame_on(False)
        else: ax.axis('off')
    
    plt.tight_layout()
    plt.show()