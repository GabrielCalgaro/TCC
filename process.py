# -*- coding: utf-8 -*-
import numpy as np
import cv2

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    back = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    cv2.imshow("bright", back)
    cv2.imwrite('C:\\Users\\calga\\Pictures\\Process\\' + 'bright.jpeg',back)
    return final_hsv  # back

def detectSkinArea(img, imgT):
    # define the upper and lower boundaries of the HSV pixel
    # intensities to be considered 'skin'
    lower = np.array([0, 45, 80], dtype="uint8")
    upper = np.array([30, 255, 255], dtype="uint8")
    
    # resize the frame, convert it to the HSV color space,
    # and determine the HSV pixel intensities that fall into
    # the speicifed upper and lower boundaries
    frame = resize(img, width=400)
    frameT = resize(imgT, width=400)
    added = increase_brightness(frame, 50)  # increase brightness
    
    skinMask = cv2.inRange(added, lower, upper)
    #cv2.imshow('skin',skinMask)
    cv2.imwrite('C:\\Users\\calga\\Pictures\\Process\\' + 'skin.jpeg',skinMask)
 
    # apply a series of erosions and dilations to the mask
    # using an elliptical kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    #skinMask = cv2.dilate(skinMask, kernel, iterations=1)
    #cv2.imshow('skinD', skinMask)
    #cv2.imwrite('C:\\Users\\calga\\Pictures\\Process\\' + 'skinD.jpeg',skinMask)
    #skinMask = cv2.erode(skinMask, kernel, iterations=1)
    #cv2.imshow('skinE', skinMask)
    skinMask = cv2.morphologyEx(skinMask, cv2.MORPH_OPEN, kernel)
    cv2.imshow('skinO', skinMask)
    skinMask = cv2.morphologyEx(skinMask, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('skinC', skinMask)
    cv2.imwrite('C:\\Users\\calga\\Pictures\\Process\\' + 'skinE.jpeg',skinMask)
 
    # blur the mask to help remove noise, then apply the
    # mask to the frame
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    cv2.imshow('skinB', skinMask)
    cv2.imwrite('C:\\Users\\calga\\Pictures\\Process\\' + 'skinB.jpeg',skinMask)
    skin = cv2.bitwise_and(frameT, frameT, mask=skinMask)
    
    # show the skin in the image along with the mask
    cv2.imshow("images", np.hstack([frameT, skin]))
    cv2.imwrite('C:\\Users\\calga\\Pictures\\Process\\' + 'skinF.jpeg',skin)
    
    return skin

def resize(img, width=1280.0):
    # Diminuir o tamanho das imagens
    r = width / img.shape[1]
    height = int(img.shape[0] * r)
    width = int(width)
    dim = (width, height)
    # print(dim)
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


def process(img, imgT, output, width=1280.0):
    # Diminuir o tamanho das imagens
    resize(img, width)
    resize(imgT, width)
    
    final = detectSkinArea(img, imgT)
    
    return final


