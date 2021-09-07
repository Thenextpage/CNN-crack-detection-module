# CNN-crack-detection-module
This is a project about a module that detects cracks using machine learning image recognition technology. For the image recognition algorithm, we used a CNN algorithm, darkflow, YOLO algorithm to locate the cracks from the camera image data. We also used a ultrasonic distance sensor to measure the distance between the crack and the camera.

# What you need

this module basically runs on a raspberry pi so a basic
- raspberry pi 3b+
- raspberry pi camera
- ultrasonic distance sensor
- digital button switch
- raspberry pi display (optional)
- wires and resistor etc

![Screen Shot 2021-09-07 at 9 31 46 PM (2)](https://user-images.githubusercontent.com/30145956/132345081-c42e8d6a-d649-4009-99bb-f8d9625b9fdd.png)
 
For the case we used a 3d printer using the model found in this link https://pinshape.com/items/23208-3d-printed-raspberry-pi-7-inch-touchscreen-display-case

# How does it work

The function of the device can be explained in 2 parts.
  1. The crack detection using the camera and the CNN & Yolo algorithm
  2. The calculation of the width of the crack by measuring the distance of the crack and the pixel image counting

For the detection, we used the training data collected from the campus building of Middle East Technical University (METU) and a set of crack images provided by Utah State University (USU). Label Img was used as a tool for performing the data labeling process. 

The value of the loss function started at 100-106, which is the value in step 1, decreased significantly as the learning progressed, and then the value of the loss function stagnated at 1.9-2.7 from 21,000 steps. Due to the characteristics of Darkflow, which can only confirm the loss function, the weight obtained from 20,000 steps was stored in units of 1,000 steps and the accuracy was tested. The most accurate weight file was the weight in 24,000 steps, so the weight file in 24,000 steps was selected as the file to be used for the program.

with the database that we labeled and trained, we had about 80% of accuracy of detecting various types of cracks, such as linear cracks, and the y shaped cracks.

After we detected the location of the cracks using the image data from the camera, we then calculated the width of the cracks, which is achevied by calculating the distance of the crack and the calculating the pixel width of the cracks.

lets say that an object A is being filmed on the camera and it is occupying H amount of pixels at a W distance from the camera. When the object gets farther from the camera by 2W, the image pixel will only occupy by a half of an H, which is 1/2 H pixels. Therefore we can conclude that if we multiply the pixel count and the distance from the camera, the constant will be the same at any distance.

![Screen Shot 2021-09-07 at 9 54 32 PM (2)](https://user-images.githubusercontent.com/30145956/132348205-5bf6b3f4-63fe-4066-a55d-1fbec035bbdc.png)

Skeletonization method was used to measure the width of cracks, which has irregular patterns and shapes. Skeletonization is the process of reducing image data to skeleton form. Skeleton represents the position of the center of the circle in contact with both sides when the original image is drawn in a circle inside the figure. The distance between the skeleton extracted through Skeletonization and the side of the figure may be obtained as a pixel value. 

A library of scikit-image was used to obtain the skeleton of cracks. The original crack image was converted into gray scaling, color inversion, and binary black and white images. Figure 21 is the original image from the left, the binary black-and-white processing image, the skeleton result, the binary black-and-white image, and the result of visualizing the distance to skeleton as gradation.

![Screen Shot 2021-09-07 at 9 59 13 PM (2)](https://user-images.githubusercontent.com/30145956/132348858-80449ce7-f8f2-4b03-bf9c-d4203af00bcd.png)

as a result we could successfuly be able to measure the location, and the width of the cracks at the accuracy of ±0.2mm.

![Screen Shot 2021-09-07 at 10 01 12 PM (2)](https://user-images.githubusercontent.com/30145956/132349145-eda2dc38-d0e6-4dc6-811c-07831f68383d.png)
