import appuifw
import e32
import graphics
import thread
import time

class Main:    
    def __init__(self):
        appuifw.app.title = u'Positioning'
        appuifw.app.body = self.canvas = appuifw.Canvas()
        appuifw.exit_key_handler = self.OnExit
        appuifw.app.menu = [(u'Calcola', self.OnCalcola)]
        self.loop = 1
        self.indice = 0
        self.img = graphics.Image.new(self.canvas.size)
        self.OnLoop()

    def OnCalcola(self):
        numero = appuifw.query(u'Inserire un Numero', 'number')
        thread.start_new_thread(self.fibonacci, (numero, ))
    
    def fibonacci(self, n):
        a, b = 0, 1
        for i in range(n):
            a, b = b, a + b
            self.indice = ((i+1)*100)/n
        
    def OnExit(self):
        self.loop = 0
    
    def OnLoop(self):
        while self.loop:
            e32.ao_sleep(0.1)
            self.img.clear(0)
            self.img.line([37, 50, 137, 50], 0xffffff, width=20)
            self.img.line([37, 50, 37 + self.indice, 50], 0xfffc0d, width=20)
            self.img.text((80, 55), str(self.indice) + u'%', 0x000000)
            self.canvas.blit(self.img)

if __name__ == '__main__':
    main = Main()
