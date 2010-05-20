# -*- coding: utf-8 -*-

"""
    persion walk
"""

import appuifw, graphics, e32

def cn(x):
    return x.decode("utf-8")

font=('normal', 15, graphics.FONT_BOLD)
appuifw.app.body = canvas = appuifw.Canvas()
appuifw.app.screen = "full"
img = graphics.Image.new(canvas.size)
img.clear(0)
man = graphics.Image.open("e:\\data\\python\\person.png")

def ww(a, xy):
    if a==0:
        canvas.blit(img)
        canvas.blit(man, target=(xy, 50), source=(71, 40, 100, 100))
    else:
        canvas.blit(img)

#--------------显示人物-----------------↓
def w():
    global a
    a=0
    ww(a,xy)
#--------------显示人物-----------------↑

#--------------隐藏人物-----------------↓
def wj():
    global a
    a=3
    ww(a)
#--------------隐藏人物-----------------↑

#--------------动态人物-----------------↓
    
def l(y):
    canvas.blit(img)
    canvas.blit(man, target=(y, 50),source=(25, 40, 51, 100))

def ad():
    l(y)
    e32.ao_sleep(0.5)
    w()
    e32.ao_sleep(0.5)
    w()
    e32.ao_sleep(0.5)
global x, y, xy
x = 50
y = 50
xy = 50
for i in range(1000):
    x = x-5
    y = y-5
    xy = xy-5
    e32.ao_sleep(0.1)
    ad()     
#--------------动态人物-----------------↑ 
canvas.bind(8, lambda:ad())

#e32.ao_sleep(50)
