from picamera import PiCamera
from time import sleep
from PIL import Image

import RPi.GPIO as gpio
import time

from skimage import io
from skimage.io import imread
from skimage.transform import rescale
from skimage.util import invert
from skimage.filters import threshold_minimum
from skimage.morphology import medial_axis

import numpy as np
 #  Capturing the crack

camera = PiCamera()
camera.resolution = (1000,1000)
camera.vflip = 1
camera.start_preview()
sleep(3)
camera.capture('crack.jpg')
camera.stop_preview()

# croping the crack for now

im = Image.open('crack.jpg')

width, height = im.size

new_width = 700
new_height = 700

left = (width - new_width)/2
top = (height - new_height)/2
right = (width + new_width)/2
bottom = (height + new_height)/2

im = im.crop((left,top,right,bottom))
im.save('crackcrop.jpg')

# distance

gpio.setmode(gpio.BCM)

trig = 13
echo = 19

gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)

try :
    gpio.output(trig, False)
    time.sleep(0.5)

    gpio.output(trig, True)
    time.sleep(0.00001)
    gpio.output(trig, False)

    while gpio.input(echo) == 0 :
      pulse_start = time.time()
 
    while gpio.input(echo) == 1 :
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17000
    distance = round(distance, 2)

    print ("Distance : ", distance, "cm")

except :
    gpio.cleanup()
finally :
    gpio.cleanup()
    
#skeleton & medial axis calculate    


image_gray = io.imread('crackcrop.jpg', as_gray=True)


image_gray = rescale(image_gray, 0.6, anti_aliasing=False)


image = invert(image_gray)


thresh_min =  threshold_minimum(image)
binary_min = image > thresh_min

data = binary_min

skel, pixeldistance = medial_axis(data, return_distance=True)

# maxnum = 0
# for x in distance:
#   newmaxnum = max (x)
#   if newmaxnum > maxnum:
#     maxnum = newmaxnum
maxnum = np.max(pixeldistance)
print("skeleton pixel distance : ", maxnum)

answer = distance * maxnum / 360

print ("crack Distance : ", answer , "cm")
