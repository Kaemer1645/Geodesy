#!/usr/bin/env python
# -*- coding: utf-8 -*-
from  PIL import Image, ImageDraw, ImageFont
import os
im=Image.open('karta.png')
draw=ImageDraw.Draw(im)
fontsFolder=r'C:\Windows\Fonts'
arialFont=ImageFont.truetype(os.path.join(fontsFolder,'calibri.ttf'),30)
#draw.text((408,310),'Jak sie masz?',fill='blue',font=arialFont)

plik_tekstowy=open('tekstowy.txt','r')
lista=[]
iterator=0
for line in plik_tekstowy.readlines():
    iterator+=1
    lista.append(line)
    if iterator == 1:
        draw.text((295, 310), str(line), fill='blue', font=arialFont)
    if iterator == 2:
        draw.text((295, 482), str(line), fill='blue', font=arialFont)

#print(lista)



im.save('text.png')
