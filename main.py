# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join
import numpy as np
import cv2
from process import process
from process import resize

# constantes
inputPath = 'input/'
outputPath = 'output/'

# ler as imagens do diretorio inputPath
onlyfiles = [ f for f in listdir(inputPath) if isfile(join(inputPath, f)) and 'N' in f]
onlyfilesheat = [ f for f in listdir(inputPath) if isfile(join(inputPath, f)) and 'H' in f]

for n in range(0, len(onlyfiles)):
    # Carrega as imagens original e térmica
    img = cv2.imread(join(inputPath, onlyfiles[n]))
    heat = cv2.imread(join(inputPath, onlyfilesheat[n]))
    
    # imagem resultante
    final = process(img, heat, outputPath)
    
    #calcula porcentagem colorida da imagem
    img2gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
    colour = cv2.countNonZero(img2gray)
    
    #recorta a parte vermelha
    heat = resize(heat, 400)
    hsv = cv2.cvtColor(heat, cv2.COLOR_BGR2HSV)
    lower_red = np.array([170,55,55])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    res1 = cv2.bitwise_and(heat,heat, mask= mask1)
    
    #recorta a parte branca
    lower_red2 = np.array([0,55,55])
    upper_red2 = np.array([10,255,255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    res2 = cv2.bitwise_and(heat,heat, mask= mask2)
    
    #junta ambos os cortes
    res = cv2.bitwise_xor(res1,res2)
    
    #calcula porcentagem colorida(vermelha) da imagem resultante
    img2gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    rows, cols, channels = res.shape
    tam = rows*cols
    red = cv2.countNonZero(img2gray)
    percentage = (red*100)/colour
    print (percentage)

    # salva imagem final para conferencia
    cv2.imwrite(outputPath + "Final_" + onlyfiles[n], final)  
    cv2.imwrite(outputPath + 'Red_.jpeg' + onlyfiles[n], res)

key = cv2.waitKey(0)
if key == 27:  # wait for ESC key to exit
    cv2.destroyAllWindows()
