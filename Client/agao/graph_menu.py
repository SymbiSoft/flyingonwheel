#! -*- coding: utf-8 -*-

"""
    test graph menu
"""

import appuifw, time, audio, os
from graphics import *
import e32, topwindow

appuifw.app.screen="full"
img = Image.new((240, 320))
img.clear(0xFAEBD7)
appuifw.app.body = canvas = appuifw.Canvas()

def cn(x):
    return x.decode("utf-8")

font=('normal', 15, FONT_BOLD)

#-------------------------图片↓
screen = topwindow.TopWindow()
photo = Image.open("e:\\data\\python\\0.jpg")
screen.add_image(photo, (0, 0, 240, 320))
screen.show()
e32.ao_sleep(1.5)
screen.hide()

jpg1 = Image.open("e:\\data\\python\\1.jpg")
img.blit(jpg1, (0, 25))
canvas.blit(img)
#-------------------------图片↑

#-------------------------声音↓
sound1 = audio.Sound.open("e:\\data\\python\\ding.wav")
sound2 = audio.Sound.open("e:\\data\\python\\ding.wav")
sound3 = audio.Sound.open("e:\\data\\python\\ding.wav")
#-------------------------声音↑

#-------------------------功能↓
def menu():
    #定义通话键噶功能
    sound2.play()
    o=open("e:\\data\\python\\down.down","w")
    o.close()
    img.rectangle((0,205,85,295),0,fill=0xFAEBD7)
    img.text((205,316),cn("退出"),0xFAEBD7,font)
    img.text((207,316),cn("取消"),0xFF00FF,font)
    img.text((1,240),cn("1.开始游戏"),0xFF00FF,font)
    img.text((1,280),cn("2.退出游戏"),0,font)

    def down():
        #导向键下
        down=os.path.exists("e:\\data\\python\\down.down")
        if down>0:
            sound1.play()
            img.text((1,240),cn("1.开始游戏"),0,font)
            img.text((1,280),cn("2.退出游戏"),0xFF00FF,font)
            os.remove("e:\\data\\python\\down.down")
            o=open("e:\\data\\python\\up.up","w")
            o.close()
    
    def up():
        #导向键上
        up=os.path.exists("e:\\data\\python\\up.up")
        if up>0:
            sound1.play()
            img.text((1,240),cn("1.开始游戏"),0xFF00FF,font)
            img.text((1,280),cn("2.退出游戏"),0,font)
            os.remove("e:\\data\\python\\up.up")
            o=open("e:\\data\\python\\down.down","w")
            o.close()
    
    appuifw.app.body.bind(63498,down)
    appuifw.app.body.bind(63497,up)
    
    def exit():
        #右软键
        down=os.path.exists("e:\\data\\python\\down.down")
        up=os.path.exists("e:\\data\\python\\up.up")
        
        img.blit(jpg1,(0,25))
        canvas.blit(img)
        
        if down>0:
            os.remove("e:\\data\\python\\down.down")
        if up>0:
            os.remove("e:\\data\\python\\up.up")
        
        img.blit(jpg1,(0,25))
        canvas.blit(img)
                
        img.text((207,316),cn("取消"),0xFAEBD7,font)
        img.text((205,316),cn("退出"),0,font)
        
        if up==0 and down ==0:
            sound1.play()
            if appuifw.query(cn("退出游戏吗？"),"query"):
                appuifw.app.set_exit()
    appuifw.app.exit_key_handler=exit
appuifw.app.body.bind(63586,menu)


def out():
    #右软键
    sound1.play()
    if appuifw.query(cn("是否退出游戏？\n阿高提示"),"query"):
        appuifw.app.set_exit()
appuifw.app.exit_key_handler=out


def ok():
    #定义确定键噶功能
    down=os.path.exists("e:\\data\\python\\down.down")
    up=os.path.exists("e:\\data\\python\\up.up")
    if up>0:
        if appuifw.query(cn("退出游戏吗？"),"query"):
            os.remove("e:\\data\\python\\up.up")
            appuifw.app.set_exit()
    
    if down>0:
        img.rectangle((0,205,85,295),0xFAEBD7,fill=0xFAEBD7)
        os.remove("e:\\data\\python\\down.down")
        img.text((207,316),cn("取消"),0xFAEBD7,font)
        img.text((205,316),cn("退出"),0,font)
        sound3.play() 
        
        img.blit(jpg1,(0,25))
        canvas.blit(img)
appuifw.app.body.bind(63557,ok)
#-------------------------功能↑


#-------------------------界面↓
img.text((205,316),cn("退出"),0,font)
img.text((0,316),cn("菜单"),0,font)
img.line((0,295,320,295),0,width=2)
# img.text((197,20),cn("- 口 X"),0,font)
# img.line((0,25,320,25),0,width=2)
# img.text((0,18),cn("胃食猫"),0,font)
#-------------------------界面↑

#-------------------------无限重复动作↓    
def wwe():
    canvas.blit(img)
running=1
while running:
    wwe()
    a=time.strftime("%H:%M:%S")
    img.text((85,316),cn("")+a,0xFF0000,font)
    e32.ao_sleep(0.8)
    img.text((85,316),cn("")+a,0xFAEBD7,font)
    e32.ao_yield()
