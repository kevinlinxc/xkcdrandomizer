# version run by Serverless Lambda function
import imageio
import xkcd
import cv2
import matplotlib.pyplot as plt
import numpy as np
import random
from kumikolib import Kumiko
import tweepy
import json
import os

desiredheight = 1000
local = False
debug = False
printonly = False

# adds border padding to an image with the passed width, returns new image
def pad(image, width):
    black = [0,0,0]
    return cv2.copyMakeBorder(image.copy(),width,width,width,width,cv2.BORDER_CONSTANT,value=black)

# rejects panels that are too tall or wide, too small or large
def panelcheck(panellist):
    returnlist = []
    for panel in panellist:
        width = panel[2]
        height = panel[3]
        area = width*height
        if area <= 110000 and area > 30000 and height/width > 0.5 and height/width < 3:
            returnlist.append(panel)
    return returnlist

# generates random xkcd image
def makerandomxkcd():
    comicbuilder = np.zeros((desiredheight,1))
    comiclist = []
    while comicbuilder.shape[1] < desiredheight*2:
        try:
            # get random comic, pad it because some panels don't have borders
            comic = xkcd.getRandomComic()
            array = imageio.imread(comic.getImageLink())
            array = pad(array,1)
            # get panel corners using kumiko
            k = Kumiko()
            info = k.parse_images([array])
            panels = info[0]['panels']
            goodpanels = panelcheck(panels)
            if len(goodpanels) == 0:
                continue
            if len(array.shape) > 2:
                array = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
            if debug:
                print(f'Found comic: {comic.getImageLink()} with shape {array.shape}')
            x, y , w, h = goodpanels[random.randint(0,len(goodpanels)-1)]
            # extract panel (removing top/bottom padding), scale, and hstack
            chosenpanel = array[y+1:y+h-1, x: x+w]
            scalefactor = desiredheight / h
            chosenpanel = cv2.resize(chosenpanel, (int(w*scalefactor), desiredheight))
            comicbuilder = np.hstack([comicbuilder, chosenpanel])
            comiclist.append(comic.__getattribute__("number"))
        except:
            # just look for new comics if some are problematic
            continue
    if debug:
        plt.imshow(comicbuilder, cmap='Greys_r')
        plt.show()
    cv2.imwrite("/tmp/xkcd.png", comicbuilder)
    return comiclist if len(comiclist)>0 else None

def execute():
    if local: #Get api key from config file
        with open('config.json') as config_file:
            config = json.load(config_file)
            auth = tweepy.OAuthHandler(config['keys']['api_key'], config['keys']['api_key_secret'])
            auth.set_access_token(config['keys']['consumer_key'], config['keys']['consumer_key_secret'])

    else: # get api key from Lambda env variables
        auth = tweepy.OAuthHandler(os.environ['api_key'], os.environ['api_key_secret'])
        auth.set_access_token(os.environ['consumer_key'], os.environ['consumer_key_secret'])
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    message = makerandomxkcd()
    statusout = ''
    if message:
        imagepath = '/tmp/xkcd.png'
        message = [str(m) for m in message]
        statusout = "#xkcd comics "+ ', '.join(message)
        if printonly:
            print(statusout)
        else:
            api.update_with_media(imagepath, status=statusout)
            print("posted")
    return statusout

def handler(event, context):
    statusout = execute()
    body = {
        "message": statusout,
        "input": event
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response