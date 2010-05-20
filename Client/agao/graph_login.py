# -*- coding: utf-8 -*-

"""
    a graph login frame
"""

import graphics, e32, appuifw

font = ('normal', 15, graphics.FONT_BOLD)
appuifw.app.body = canvas = appuifw.Canvas()
appuifw.app.screen = "full"

def cn(x):
    return x.decode("utf-8")

img = graphics.Image.new(canvas.size)
img.clear(0)

img.rectangle((10, 90, 230, 190), 0x316ac5, 0xe0e0ff)#大
img.rectangle((10, 70, 230, 90), 0x316ac5, 0x316ac5)#标题
img.text((11, 88), cn("客户端"), 0xFF6347, font)

img.text((11, 122), cn("IP地址:"), 0x316ac5, font)
img.rectangle((70, 105, 220, 125), 0x316ac5, width=3)#IP地址框

img.text((25, 147), cn("端口:"), 0x316ac5, font)
img.rectangle((70, 130, 220, 150), 0x316ac5)#端口框

img.text((25, 180), cn("连接"), 0x316ac5, font)
img.text((187, 180), cn("取消"), 0x316ac5, font)

img.line((230, 74, 230, 190), 0x316ac5, width=2)#右阴影
img.line((14, 190, 230, 190), 0x316ac5, width=2)#下阴影

#------------按键控制-------------------↓
def down():
    img.rectangle((70, 105, 220, 125), 0xe0e0ff, width=3)#IP地址框灰
    img.rectangle((70, 105, 220, 125), 0x316ac5)#IP地址框细
    img.rectangle((70, 130, 220, 150), 0x316ac5, width=3)#端口框粗
#选中端口框
canvas.bind(63498, lambda:down())

def up():
    img.rectangle((70, 105, 220, 125), 0x316ac5, width=3)#IP地址框粗
    img.rectangle((70, 130, 220, 150), 0xe0e0ff, width=3)#端口框灰
    img.rectangle((70, 130, 220, 150), 0x316ac5)#端口框细
#选中地址框
canvas.bind(63497, lambda:up())

def left():
    img.text((25, 180), cn("连接"), 0xFF6347, font)
    img.text((187, 180), cn("取消"), 0x316ac5, font)
#选中连接
canvas.bind(63495, lambda:left())

def right():
    img.text((25, 180), cn("连接"), 0x316ac5, font)
    img.text((187, 180), cn("取消"), 0xFF6347, font)
#选中取消
canvas.bind(63496, lambda:right())
#------------按键控制-------------------↑

def exit():
    global gao
    gao = 0
appuifw.app.exit_key_handler = exit 
gao = 1
while gao:    
    canvas.blit(img)
    e32.ao_yield()
