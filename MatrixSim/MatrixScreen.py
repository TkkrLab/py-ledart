import sys
import os
import time

# first things first make sure we are able to find the necesary files we need.
# wd = os.path.join(os.path.dirname(__file__), os.path.pardir)
# sys.path.append(wd)
# sys.path.append(wd + "/patterns/Graphics/")

from Pixel import Pixel
import Graphics.Graphics as Graphics
import matrix


class MatrixScreen(object):
    timing = 0
    fps = 0
    timed = False

    def __init__(self, width, height, pixelSize, fullscreen=False):
        import pygame
        self.pygame = pygame
        self.width = width
        self.height = height
        self.pixelSize = pixelSize

        self.pixels = []

        self.window_width = height*pixelSize
        self.window_height = width*pixelSize

        self.flags = self.pygame.DOUBLEBUF | self.pygame.HWSURFACE
        if fullscreen:
            self.flags |= self.pygame.FULLSCREEN

        self.window = self.pygame.display.set_mode((self.window_width,
                                                    self.window_height),
                                                   self.flags)
        self.pygame.display.set_caption("pygame artnet matrix simulator.")

        widthRange = range(0, self.window_width, pixelSize)
        # reverse order because else the display is flipped.
        heightRange = range(0, self.window_height, pixelSize)[::-1]

        #due to how the ledmatrix is displayed x, y are filled as is the
        #window_width/height thing a bit above here.
        for x in widthRange:
            for y in heightRange:
                pos = (x, y)
                color = Graphics.BLUE
                pixel = Pixel(pos, pixelSize, color)
                self.pixels.append(pixel)

    def handleInput(self):
        self.pygame.event.pump()
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                sys.exit(0)
            if event.type == self.pygame.KEYDOWN:
                lctrlPressed = (self.pygame.key.get_mods() &
                                self.pygame.KMOD_LCTRL)
                if event.key == self.pygame.K_c and lctrlPressed:
                    raise KeyboardInterrupt
                #check if mouse in window then make invisible else visible
                if self.pygame.mouse.get_focused():
                        self.pygame.mouse.set_visible(False)
                else:
                        self.pygame.mouse.set_visible(True)

    def draw(self, data):
        #extract pixels and color from data
        #get both a list index and the color data.
        for i, color in enumerate(data):
            self.pixels[i].setColor(color)

        #clear the pygame window
        self.window.fill(Graphics.BLACK)

        #display the pixels.
        for pixel in self.pixels:
            r = pixel.color[matrix.COLOR_ORDER[0]]
            g = pixel.color[matrix.COLOR_ORDER[1]]
            b = pixel.color[matrix.COLOR_ORDER[2]]
            color = (r, g, b)
            self.pygame.draw.rect(self.window, color, pixel.getRect())
            #draw a nice little square around so it looks more like a pixel.
            self.pygame.draw.rect(self.window, Graphics.BLACK,
                                  pixel.getRect(), 1)

        #update the screen so our data show.
        self.pygame.display.update()

    def process(self, data):
        self.timed = not self.timed
        if self.timed:
            self.timing = time.time()
        else:
            self.fps = 1./(time.time()-self.timing)
        self.pygame.display.set_caption("artnet matrix sim FPS:" +
                                        str(int(self.fps)))
        self.handleInput()
        self.draw(data)

    def __del__(self):
        self.pygame.quit()
