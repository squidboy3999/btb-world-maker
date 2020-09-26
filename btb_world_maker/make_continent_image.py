from PIL import Image
from random import randint


def build_map_image(cm_map):
    background = Image.open("images/background.jpg")
    forest_images=[]
    forest_images.append(Image.open("images/forest_1_small.jpg"))
    forest_images.append(Image.open("images/forest_2_small.jpg"))
    forest_images.append(Image.open("images/forest_3_small.jpg"))
    grass_images=[]
    grass_images.append(Image.open("images/grass_1_small.jpg"))
    grass_images.append(Image.open("images/grass_2_small.jpg"))
    grass_images.append(Image.open("images/grass_3_small.jpg"))
    desert_images=[]
    desert_images.append(Image.open("images/coast_3_small.jpg"))
    mountain_images=[]
    #mountain_images.append(Image.open("images/mountain_1_small.jpg"))
    mountain_images.append(Image.open("images/mountain_2_small.jpg"))
    marsh_images=[]
    marsh_images.append(Image.open("images/marsh_1_small.jpg"))
    #marsh_images.append(Image.open("images/marsh_2_small.jpg"))
    #marsh_images.append(Image.open("images/marsh_3_small.jpg"))
    coast_images=[]
    #coast_images.append(Image.open("images/coast_1_small.jpg"))
    #coast_images.append(Image.open("images/coast_2_small.jpg"))
    coast_images.append(Image.open("images/coast_3_small.jpg"))
    ocean_images=[]
    ocean_images.append(Image.open("images/ocean_1_small.jpg"))
    #ocean_images.append(Image.open("images/ocean_2_small.jpg"))
    #ocean_images.append(Image.open("images/ocean_3_small.jpg"))
    for i in range(50):
        for j in range(50):
            area=(i*20,j*20,(i+1)*20,(j+1)*20)
            if cm_map[i][j]=="f":
                background.paste(forest_images[randint(0,len(forest_images)-1)],area)
            elif cm_map[i][j]=="g":
                background.paste(grass_images[randint(0,len(grass_images)-1)],area)
            elif cm_map[i][j]=="d":
                background.paste(desert_images[randint(0,len(desert_images)-1)],area)
            elif cm_map[i][j]=="t":
                background.paste(mountain_images[randint(0,len(mountain_images)-1)],area)
            elif cm_map[i][j]=="r":
                background.paste(marsh_images[randint(0,len(marsh_images)-1)],area)
            elif cm_map[i][j]=="o":
                background.paste(ocean_images[randint(0,len(ocean_images)-1)],area)
            else:
                background.paste(coast_images[randint(0,len(coast_images)-1)],area)
    background.save("images/new_background.jpg")


def is_beach(tile_val):
    cases=["c","di","nb","sb","eb","wb","swc","sec","nwc","nec","nc","sc","ec","wc","ns","ew"]
    if(tile_val in cases):
        return True
    else:
        return False
