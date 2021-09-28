######################################################################
#                 #####       #####            ##                    #
#                  ###         ###             ##                    #
#                  ###         ###             ##                    #
#                  ###         ###     ##      ##                    #
#                  ###############     ##      ##                    #
#                  ###############             ##                 `  #
#                  ###         ###    ###      ##                    #
#                  ###         ###      #      ##                    #
#                  ###         ###      #                            #
#                  ###         ###      #      ##                    #
#                 #####       #####   #####    ##                    #
#                                                                    #
#                made and scripted by nate tanner :)                 #
#         all resources were gathered from youtube and api           #
#         references online. i attempted to stray from using         #
#         pre-made software so and instead stuck with code so        #
#                           there's a lot!                           #
#                                                                    #
#                           started:8/2021                           #
######################################################################

import time
import random
import os

for x in range(1, 7):
    y = x
    if y > 3:
        y -= 3
    print("[INIT]   Initializing" + ("." * y))
    time.sleep(random.random())

for listing in os.listdir():
    if 'speech' in listing and ".mp3" in listing:
        os.remove(listing)

print("[SUCC]   Starting")

import main
#import server

#server.start()
