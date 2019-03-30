# -*- coding: utf-8 -*-
import numpy as np
import cv2
from process import resize

def processheat(heat):
    # recorta a parte vermelha
    heat = resize(heat, 400)
    hsv = cv2.cvtColor(heat, cv2.COLOR_BGR2HSV)
    lower_red = np.array([170,55,55], dtype="uint8")
    upper_red = np.array([180,255,255], dtype="uint8")
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    res1 = cv2.bitwise_and(heat,heat, mask= mask1)
    
    # recorta a parte branca
    lower_red2 = np.array([0,55,55])
    upper_red2 = np.array([10,255,255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    res2 = cv2.bitwise_and(heat,heat, mask= mask2)
    
    # junta ambos os cortes
    res = cv2.bitwise_xor(res1,res2)
    
    return res


