# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 16:20:20 2019

@author: MM
"""
import tables
import numpy  as np
from PIL import Image
import matplotlib.pyplot as plt

def contrast(im):
    imarray = np.array(im) 
    imarray.shape 
    px = im.load()
    im.save("rzecz.tiff")
    size = im.size

    wart_max = 255
    wart_min = 0
    print(size)

    delta = 0.6*(wart_max - wart_min)

    for x in range(size[0]):
        for y in range(size[1]):
            a= px[x,y]
            if a <=  wart_min + delta :
                px[x,y] = wart_min
            if a >=  wart_min + delta :
                px[x,y] = wart_max
            
    im.show()
    im.save("rzecz_zmieniony.jpg")
    return(im)
    
def convert(im):
    width1, height1 = im.size
    pxa=im.load()
    imm=Image.new('L',(width1, height1))
    pxb=imm.load()
    for i in range(0,width1):
        for j in range(0,height1):
            pxb[i,j] = pxa[i,j][0]
    imm.show()
    return(imm)

def fft1d(vector):
    transform = np.fft.fft(vector)
    return np.fft.fftshift(np.fft.fftfreq(vector.size)), np.fft.fftshift(transform)
    

img = Image.open('image.jpg')
px=img.load()
if len(px[0,0])==3:
    img=convert(img)
img=contrast(img)
pixels = list(img.getdata())
width, height = img.size
px = img.load()
filename = 'dddd'
filename2 = 'wwww'
f = tables.open_file(filename, mode='w')
g = tables.open_file(filename2, mode='w')
atom = tables.Float64Atom()

array_c = f.create_earray(f.root, 'data', atom, (0, width))
array_d = g.create_earray(g.root, 'data', atom, (0, width))


a = np.zeros((width,height),dtype='complex')
        
vector = []
for i in range(0, width):
    vector.append(px[i,0])
#   print(px[i,0])
vector = np.asarray(vector)

e,w=fft1d(vector)
w_file = np.expand_dims(w,0)
array_c.append(np.real(w_file))
array_d.append(np.imag(w_file))
for q in range(1,height):
    vector = [] 
    for i in range(0, width):
        vector.append(px[i,q])
    
    vector = np.asarray(vector)    
    x1,y=fft1d(vector) 
    y_file = np.expand_dims(y,0)
    array_c.append(np.real(y_file))
    array_d.append(np.imag(y_file))
    


e1,u1 = fft1d(f.root.data[:,0]+1j*g.root.data[:,0])
f.root.data[:,0] = np.real(u1)
g.root.data[:,0] = np.imag(u1)


for q in range(1,width): 
    x3,y3=fft1d(f.root.data[:,q]+1j*g.root.data[:,q])
    f.root.data[:,q] = np.real(y3)
    g.root.data[:,q] = np.imag(y3)
    print(q)


img1=Image.new('L',(width, height))
px1=img1.load()

for r in range(0,width):
    for p in range(0,height):
        px1[r,p] = int(np.abs(f.root.data[p,r] + 1j*g.root.data[p,r])*256/1500000)
    print(r)


img1.save("plik1.jpg")
img1.show()
f.close()
g.close()
