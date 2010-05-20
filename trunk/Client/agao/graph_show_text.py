# -*- coding: utf-8 -*-

"""
    test text show on graphics of pys60 
"""

import appuifw, graphics, e32

appuifw.app.screen = 'full'
canvas = appuifw.Canvas()               # create a canvas
image = graphics.Image.new(canvas.size) # create an image
appuifw.app.body = canvas
appuifw.app.exit_key_handler = quit

def quit():
  global running
  running = 0

fonts = [ # different font specifications
  None,
  'normal',
  u'LatinBold19',
  (None, 15),
  ('normal', 15),
  (u'LatinBold19', 15, graphics.FONT_BOLD | graphics.FONT_ITALIC),
]
text = "测试.".decode('utf-8')

canvas.clear(0)
image.clear(0)
y = 20
for font in fonts: # draw the same text on the canvas and the image
  canvas.text((10, y), text, fill = 0xff0000, font = font) # red text on the canvas
  image.text((10, y), text, fill = 0x0000ff, font = font) # blue text on the image
  y += 25
canvas.blit(image, target = (0, y)) # copy the image's contents to the lower part of the canvas

running = 1
while running:
  e32.ao_yield() # wait for the exit button to be pressed
