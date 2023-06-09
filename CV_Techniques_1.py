#Finding the chambers of the heart through a variation of techniques. Each technique is separated out by comment. 

#(a) Take the image heart.jpg and find a threshold to pull out the two heart
#chambers. Please give me the threshold and results. See the Power Point
#medical.imaging.ppt.
"""

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


heart = cv.imread('Heart.pbm',0)

#smoothing filter
blurHeart = cv.blur(heart,(5,5))

#threshold
ret,threshHeart = cv.threshold(blurHeart,170,255,cv.THRESH_BINARY)

#comparing every pixel in the original image to 170. 
#If it's less than 170, the value is assigned to 0 which is black. 
#If it's greater than 170, the value is assigned to 255 which is white.

titles = ['Original Image','Heart Chambers']
images = [heart, threshHeart]

#range one more than the number of thresholds
for i in range(2):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

"""Threshold: 170,255 for THRESH_BINARY

I used cv2,numpy, and pyplot.
The blur and threshold functions are used to answer the question.

(b) Take the image brain.tech.jpg and find a threshold to pull out the tumor.
Please give me the threshold and results. See the Power Point
medical.imaging.ppt.
"""


brain = cv.imread('brain.tech.pgm',0)

#smoothing filter
blurBrain = cv.blur(brain,(5,5))

#threshold
ret,threshBrain1 = cv.threshold(blurBrain,155,255,cv.THRESH_BINARY)
ret,threshBrain2 = cv.threshold(blurBrain,155,255,cv.THRESH_BINARY_INV)

#comparing every pixel in the original image to 170. 
#If it's less than 170, the value is assigned to 0 which is black. 
#If it's greater than 170, the value is assigned to 255 which is white.

titles = ['Original Image','Brain Tumor','INV']
images = [brain, threshBrain1,threshBrain2]

#range one more than the number of thresholds
for i in range(3):
    plt.subplot(1,3,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

#Threshold: 155,255 for THRESH_BINARY

#Threshold: 155,255 for THRESH_BINARY_INV to see the tumor in white instead of black

#I used cv2,numpy, and pyplot.
#The blur and threshold functions are used to answer the question.

Look up the watershed method for segmentation. Write a paragraph about the
method, explaining how it works and its advantages and weaknesses. Apply it to
segmenting the tumor of brain.tech.jpg.

The act of segmenting a picture is to divide it into separate parts or sections. 
The watershed method approaches this process by looking at a grayscale image as a topographical 
landscape with ridges and valleys. It is especially useful when working with touching or 
overlapping objects within an image. Watershed segmentation helps to segment images that would 
otherwise be impossible to segment, like when using a simple thresholding algorithm. To begin, a
set of markers must be assigned throughout the image. The placement of the markers is 
important, and also poses a weakness to this method, as it needs to be correct for accurate results.
The markers allow the algorithm to treat the pixels in the image like topography. The lowest 
points or "valleys" are filled in, starting from the markers and moving outwards, until they start 
meeting each other. Over-segmentation may occur if there is noise or any other irregularity in the 
image, which is another weakness. This process essentially extracts individual objects within an 
image, solving our problem of segmenting when objects are touching or overlapping.
"""

braintech1 = cv.imread('brain.tech.pgm')
braintech = cv.imread('brain.tech.pgm')
gray = cv.cvtColor(braintech,cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)

#blur
kernel = np.ones((3,3),np.uint8)
opening = cv.morphologyEx(thresh,cv.MORPH_OPEN,kernel, iterations = 2)

#background
background = cv.dilate(opening,kernel,iterations=3)

#foreground
dist_transform = cv.distanceTransform(opening,cv.DIST_L2,5)
ret, foreground = cv.threshold(dist_transform,0.7*dist_transform.max(),255,0)

foreground = np.uint8(foreground)
unknown = cv.subtract(background,foreground)

#markers
ret, markers = cv.connectedComponents(foreground)
markers = markers+1
markers[unknown==255] = 0

markers = cv.watershed(braintech,markers)
braintech[markers == -1] = [255,0,255]

titles = ['Original','Segmented']
images = [braintech1,braintech]

#range one more than the number of thresholds
for i in range(2):
    plt.subplot(1,2,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

"""I used cv2,numpy, and pyplot.
The watershed function was used from the cv2 library.

3. Apply the Laplacian of Gaussian operator to find the edges in heart.jpg and
brain.tech.jpg. Try several different values of the variance sigma. For example,
sigma=1, 10, 100, 1000.
"""

heart1 = cv.imread('Heart.pbm',0)
brain1 = cv.imread('brain.tech.pgm',0)

heartBlur1 = cv.GaussianBlur(heart1,(9,9),1)
heartLaplacian1 = cv.Laplacian(heartBlur1,cv.CV_64F)

heartBlur2 = cv.GaussianBlur(heart1,(9,9),10)
heartLaplacian2 = cv.Laplacian(heartBlur2,cv.CV_64F)

heartBlur3 = cv.GaussianBlur(heart1,(9,9),100)
heartLaplacian3 = cv.Laplacian(heartBlur3,cv.CV_64F)

heartBlur4 = cv.GaussianBlur(heart1,(9,9),1000)
heartLaplacian4 = cv.Laplacian(heartBlur4,cv.CV_64F)


brainBlur1 = cv.GaussianBlur(brain1,(9,9),1)
brainLaplacian1 = cv.Laplacian(brainBlur1,cv.CV_64F)

brainBlur2 = cv.GaussianBlur(brain1,(9,9),10)
brainLaplacian2 = cv.Laplacian(brainBlur2,cv.CV_64F)

brainBlur3 = cv.GaussianBlur(brain1,(9,9),100)
brainLaplacian3 = cv.Laplacian(brainBlur3,cv.CV_64F)

brainBlur4 = cv.GaussianBlur(brain1,(9,9),1000)
brainLaplacian4 = cv.Laplacian(brainBlur4,cv.CV_64F)



titles = ['original','sig. = 1','sig. = 10','sig. = 100','sig. = 1000','original','sig. = 1','sig. = 10','sig. = 100','sig. = 1000']
images = [heart1,heartLaplacian1,heartLaplacian2,heartLaplacian3,heartLaplacian4,brain1,brainLaplacian1,brainLaplacian2,brainLaplacian3,brainLaplacian4]

#range one more than the number of thresholds
for i in range(10):
    plt.subplot(2,5,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

"""I used cv2,numpy, and pyplot.
The GaussianBlur and Laplacian functions were used from the cv2 library.

4. Apply histogram equalization to heart.jpg and brain.tech.jpg, and show results.
"""

heartImg = cv.imread('Heart.pbm',0)
brainImg = cv.imread('brain.tech.pgm',0)

#use cv.equalizeHist to apply histogram equalization to the images
equ1 = cv.equalizeHist(heartImg)
equ2 = cv.equalizeHist(brainImg)

res1 = np.hstack((heartImg,equ1))
res2 = np.hstack((brainImg,equ2)) 

titles = ['Equalized Heart Chambers','Equalized Brain']
images = [res1, res2]

for i in range(2):
    plt.subplot(2,1,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

"""I used cv2,numpy, and pyplot.
The EqualizeHist function was used from the cv2 library.

5. What does this filter do? Take α=.5, and σ=10 (in the Gaussian), and apply to
heart.jpg. Try a few other values of α and σ, and show the results.
"""

heartPic = cv.imread('Heart.pbm',0)
  
#creating first matrix
I = np.asarray(heartPic,dtype=np.float32)

heartGauss1 = cv.GaussianBlur(heartPic,(9,9),10)
kernel1 = np.add(I,np.multiply(0.5,np.subtract(I,np.multiply(I,heartGauss1))))
filter1 = cv.filter2D(heartPic, -1, kernel1)

heartGauss2 = cv.GaussianBlur(heartPic,(9,9),100)
kernel2 = np.add(I,np.multiply(1,np.subtract(I,np.multiply(I,heartGauss2))))
filter2 = cv.filter2D(heartPic, -1, kernel2)

heartGauss3 = cv.GaussianBlur(heartPic,(9,9),1000)
kernel3 = np.add(I,np.multiply(1.5,np.subtract(I,np.multiply(I,heartGauss3))))
filter3 = cv.filter2D(heartPic, -1, kernel3)

titles = ['Original','Filtered α=.5 σ=10','Filtered α=1 σ=100','Filtered α=1.5 σ=1000']
images = [heartPic, filter1,filter2,filter3]

for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

"""I used cv2,numpy, and pyplot.
The filter2D function was used from the cv2 library to apply the formula as a filter.
"""

