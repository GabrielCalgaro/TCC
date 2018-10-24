# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 19:32:07 2018

@author: calga
"""

# -*- coding: utf-8 -*-
import numpy as np
import cv2
from process import process
from process import resize

#read images
inputPath = 'C:\\Users\\calga\\Pictures\\Img\\N01.jpeg'
inputPath2 = 'C:\\Users\\calga\\Pictures\\Img\\HN01.jpeg'
outputPath = "C:\\Users\\calga\\Pictures\\Resultados"
img = cv2.imread(inputPath)
imgT = cv2.imread(inputPath2)

#imagem resultante
final = process(img, imgT, outputPath)

#calcula porcentagem colorida da imagem
img2gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
colour = cv2.countNonZero(img2gray)
print (colour)

#recorta a parte vermelha
imgT = resize(imgT, 400)
hsv = cv2.cvtColor(imgT, cv2.COLOR_BGR2HSV)
lower_red = np.array([170,55,55])
upper_red = np.array([180,255,255])
mask1 = cv2.inRange(hsv, lower_red, upper_red)
res1 = cv2.bitwise_and(imgT,imgT, mask= mask1)

#recorta a parte branca
lower_red2 = np.array([0,55,55])
upper_red2 = np.array([10,255,255])
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
res2 = cv2.bitwise_and(imgT,imgT, mask= mask2)

#junta ambos os cortes
res = cv2.bitwise_xor(res1,res2)

#calcula porcentagem colorida(vermelha) da imagem resultante
img2gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
rows, cols, channels = res.shape
tam = rows*cols
red = cv2.countNonZero(img2gray)
percentage = (red*100)/colour
print (red)
print (percentage)

cv2.imshow('res1',res1)
cv2.imshow('res2',res2)
cv2.imshow('res',res)
cv2.imshow("final", final)

cv2.imwrite('res.jpeg',res)
cv2.imwrite('final.jpeg',final)

key = cv2.waitKey(0)
if key == 27:  # wait for ESC key to exit
    cv2.destroyAllWindows()
