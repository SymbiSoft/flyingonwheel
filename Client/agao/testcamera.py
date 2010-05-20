import e32, camera, appuifw, key_codes
from graphics import Image

def viewfinder(img):
    canvas.blit(img)

def shoot():
    camera.stop_finder()
    photo = camera.take_photo(size = (640, 480))
    w, h = canvas.size
    canvas.blit(photo, target = (0, 0, w, h), scale = 1)
    photo.resize((320, 240))
    photo.save('e:\\photo.jpg')

def quit():
    app_lock.signal()

appuifw.app.body = canvas = appuifw.Canvas()
appuifw.app.title = u"Camera"
photo = Image.open("e:\\data\\python\\logo.jpg")
photo.resize((32, 32))
photo.save("e:\\data\\python\\logo.jpg")
canvas.blit(photo)
appuifw.app.exit_key_handler = quit

camera.start_finder(viewfinder)
canvas.bind(key_codes.EKeySelect, shoot)

app_lock = e32.Ao_lock()
app_lock.wait()
