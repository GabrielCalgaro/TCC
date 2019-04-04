# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join
import cv2
from process import process
from processheat import processheat

# constantes
inputPath = 'C:\\Users\\calga\\Pictures\\Formatado\\'
outputPath = "C:\\Users\\calga\\Pictures\\Resultados\\"

# ler as imagens do diretorio inputPath
onlyfiles = [ f for f in listdir(inputPath) if isfile(join(inputPath, f)) and 'N' in f]

for n in range(0, len(onlyfiles)):
    
    if 'A' in onlyfiles[n]:
        img_filename = onlyfiles[n]
        heat_filename = img_filename.replace('N', 'H')
        
        
        post_filename = img_filename.replace('A', 'D')
        post_heat_filename = heat_filename.replace('A', 'D')
    
        # Carrega as imagens original e térmica
        img = cv2.imread(join(inputPath, img_filename))
        heat = cv2.imread(join(inputPath, heat_filename))
        
        
        post_img = cv2.imread(join(inputPath, post_filename))
        post_heat = cv2.imread(join(inputPath, post_heat_filename))
        
        # Imagem resultante
        final = process(img, heat, outputPath)
        final2 = process(post_img, post_heat, outputPath)
        
        # Calcula porcentagem colorida da imagem térmica "recortada"
        img2gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
        colour = cv2.countNonZero(img2gray)
        
        img2gray2 = cv2.cvtColor(final2, cv2.COLOR_BGR2GRAY)
        colour2 = cv2.countNonZero(img2gray2)
        
        # Recorta apenas parte vermelha da imagem térmica
        res = processheat(final)
        res2 = processheat(final2)
        
        # Calcula porcentagem colorida(vermelha) da imagem resultante
        img2gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        rows, cols, channels = res.shape
        tam = rows*cols
        red = cv2.countNonZero(img2gray)
        percentage = ((red)*100)/colour
        
        img2gray2 = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)
        rows, cols, channels = res2.shape
        tam = rows*cols
        red = cv2.countNonZero(img2gray2)
        percentage2 = ((red)*100)/colour2
        print(img_filename)
        print('pre', percentage)
        print('pos', percentage2)
        
        improvement = percentage/percentage2
        print('imp', improvement)
    
        # Salva imagem final para conferencia
        cv2.imwrite(outputPath + "Pre_" + img_filename, final)
        cv2.imwrite(outputPath + "Pos_" + post_filename, final2)
        #cv2.imwrite(outputPath + 'Red_.jpeg' + onlyfiles[n], res)

key = cv2.waitKey(0)
if key == 27:  # wait for ESC key to exit
    cv2.destroyAllWindows()
