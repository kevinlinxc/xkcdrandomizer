import xkcd
import cv2
import imageio
import matplotlib.pyplot as plt
import numpy as np
import random
from kumikolib import Kumiko

desiredheight = 350

#adds a border to an image with the passed width, returns new image
def pad(image, width):
    black = [0,0,0]
    return cv2.copyMakeBorder(image.copy(),width,width,width,width,cv2.BORDER_CONSTANT,value=black)

#Rejects panels that are too tall or wide, too small or large
def panelcheck(panellist):
    returnlist = []
    for panel in panellist:
        width = panel[2]
        height = panel[3]
        area = width*height
        if area <= 110000 and area > 30000 and height/width > 0.5 and height/width < 3:
            returnlist.append(panel)
    return returnlist

#generates random xkcd image
def makerandomxkcd():
    panellist = np.zeros((350,1))
    while(panellist.shape[1] < 700):
        try:
            #get random comic, pad it because some panels don't have borders
            comic = xkcd.getRandomComic()
            array = imageio.imread(comic.getImageLink())
            array = pad(array,1)
            #get panel corners using kumiko
            k= Kumiko()
            info = k.parse_images([array])
            panels = info[0]['panels']
            goodpanels = panelcheck(panels)
            if (len(goodpanels) == 0):
                continue
            if len(array.shape) > 2:
                array = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)

            print(f'Found comic: {comic.getImageLink()} with shape {array.shape}')
            x, y , w, h = goodpanels[random.randint(0,len(goodpanels)-1)]
            #extract panel (removing top/bottom padding), scale, and hstack
            chosenpanel = array[y+1:y+h-1, x: x+w]
            scalefactor = desiredheight / h
            chosenpanel = cv2.resize(chosenpanel, (int(w*scalefactor), desiredheight))
            panellist = np.hstack([panellist, chosenpanel])
        except:
            #Just look for new comics if some are problematic
            continue
    plt.imshow(panellist, cmap='Greys_r')
    plt.show()
    cv2.imwrite("xkcd.png", panellist)
    return True
for i in range(10):
    print(f"Comic # {i}")
    makerandomxkcd()
# array = imageio.imread("https://imgs.xkcd.com/comics/e_to_the_pi_minus_pi.png")
# array = pad(array,1)
# plt.imshow(array ,cmap='Greys_r')
# cv2.imwrite("xkcd2.png", array)
# plt.show()