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
from darkflow.net.build import TFNet
import cv2
import matplotlib.pyplot as plt
import numpy as np

def boxing(original_img, predictions):
    newImage = np.copy(original_img)
    for result in predictions:
        top_x = result['topleft']['x']
        top_y = result['topleft']['y']
        btm_x = result['bottomright']['x']
        btm_y = result['bottomright']['y']
        confidence = result['confidence']
        label = result['label'] + " " + str(round(confidence, 3))
        #change confidence here
        if confidence > 0.26:
            newImage = cv2.rectangle(newImage, (int(top_x), int(top_y)), (int(btm_x), int(btm_y)), (0,255,0), 3)
            newImage = cv2.putText(newImage, label, (int(top_x), int(top_y-5)), cv2.FONT_HERSHEY_COMPLEX_SMALL , 0.8, (0, 230, 0), 1, cv2.LINE_AA) 
                        
    return newImage

#loading pb file and meta
gpio.cleanup()

options = {"model": "/home/pi/Downloads/darkflow-master/cfg/crack_yolo.cfg", "load": 24000, "batch":1, "threshold":0.26}
tfnet = TFNet(options)

gpio.setmode(gpio.BCM)
trig = 13
echo = 19
gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)
gpio.setup(16, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.add_event_detect(16,gpio.RISING, bouncetime=300)
camera = PiCamera()
answer=0


#  Capturing the crack
while True:
    #camera.resolution = (1000,1000)
    #camera.vflip = 1
    camera.start_preview()
    count=0
    while (count<30):
        if gpio.event_detected(16):
            break
        else:
            sleep(0.5)
            count = count + 1
            
    #camera.stop_preview()


    camera.capture('crack.jpg')
    

    try :
        gpio.output(trig, False)
        time.sleep(0.1)
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
    #     
    except :
         gpio.cleanup()
    #finally :
    #     gpio.cleanup()
    camera.stop_preview()

    #read and predict the camera img
    #print("Distance : ", distance, "cm")
    imgcv = cv2.imread('crack.jpg')
    result = tfnet.return_predict(imgcv)
    #print(result)

    #change confidence lvl

    seq = [x['confidence'] for x in result]

    for objects in result:
        if objects['confidence'] == max(seq):

            image_gray = io.imread('crack.jpg', as_gray=True)
            image_gray = image_gray[objects['topleft']['y']:objects['bottomright']['y'] , objects['topleft']['x']:objects['bottomright']['x']]
    #        io.imshow(image_gray)
    #        plt.show()       
            image_gray = rescale(image_gray, 1, anti_aliasing=False)
            image = invert(image_gray)
            thresh_min =  threshold_minimum(image)
            binary_min = image > thresh_min
            data = binary_min
            skel, pixeldistance = medial_axis(data, return_distance=True)
            maxnum = np.max(pixeldistance)
            #print("skeleton pixel distance : ", maxnum)
            
            #change the int
            answer = distance * maxnum / (216*2.5)
            answer = round(answer, 3)
            #print ("crack Distance : ", answer , "cm")

    img = Image.open(r'crack.jpg')
    picture = np.array(img)

    #boxing function
    picture = cv2.putText(picture, 'crack size : ' + str(answer)+'cm', (10, 25), cv2.FONT_HERSHEY_SIMPLEX , 1, (255, 255, 255), 2, cv2.LINE_AA)
    picture = cv2.putText(picture, 'distance : ' + str(distance)+'cm', (10, 50), cv2.FONT_HERSHEY_SIMPLEX , 1, (255, 255, 255), 2, cv2.LINE_AA)

    plt.imshow(boxing(picture, result))
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show(block=False)
    plt.pause(8)
    plt.savefig('result.jpg')
    plt.close()
    if gpio.event_detected(16):
        break
    
gpio.cleanup()
