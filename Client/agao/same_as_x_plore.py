# -*- coding: utf-8 -*-

import appuifw, e32, graphics, os

def cn(x):
    return x.decode("utf-8")

appuifw.app.body = canvas = appuifw.Canvas()
appuifw.app.screen="full"
font=('normal', 15, graphics.FONT_BOLD)
img=graphics.Image.new((240, 320))

img.rectangle((8, 90, 230, 110), 0xFF6347, 0x316ac5)
img.text((9, 109), cn("c:\\system\\"), 0, font)
img.rectangle((8, 110, 230, 170),0xFF6347, 0xe0e0ff)

#img.line((230,95,230,170),0,width=3)
#img.line((12,171,230,171),0,width=3)

global x, y
x = 0
y = 0
for i in os.listdir("c:\\system"):
    x=x+1

for i in os.listdir("c:\\system"):
    X = 230.0/x
    y = y+X
    img.text((9, 135), cn("")+i, 0, font)
    e32.ao_sleep(0.02)
    img.text((9, 135), cn("")+i, 0xe0e0ff, font)
    img.rectangle((8, 145, y, 170), 0, 0xFF69B4)
    e32.ao_sleep(0.02)
    canvas.blit(img)
