from Interface import Interface
import pygame
from pygame.locals import *


class PygameInterface(Interface):
    """
    a abstract drawing interface that uses pygame.
    """
    def __init__(self, width, height, blocksize, fullscreen=False):
        Interface.__init__(self, width, height, blocksize)
        self.flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        if fullscreen:
            self.flags |= pygame.FULLSCREEN
        self.window = pygame.display.set_mode((self.width, self.height),
                                              self.flags)

    def handleinput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
            elif event.type == pygame.KEYDOWN:
                # quit on ctrl-c as if it were in the terminal.
                # to lazy to press x.
                mods = event.mod
                key_mod = pygame.KMOD_LCTRL
                lctrlpressed = (mods & key_mod) == key_mod
                if event.key == pygame.K_c and lctrlpressed:
                    raise KeyboardInterrupt
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    raise KeyboardInterrupt

            # check if the mouse pointer is on/in the window.
            # and if so hide it.
            focused = pygame.mouse.get_focused()
            pygame.mouse.set_visible(not focused)

    def setcaption(self, caption):
        pygame.display.set_caption(caption + " (pygame)")

    def clear(self, color):
        self.window.fill(color)

    def drawblock(self, rect, color, bordercolor, borderwidth=1):
        pygame.draw.rect(self.window, color, rect)
        # draw a nice little square around so it looks more like a pixel.
        pygame.draw.rect(self.window, bordercolor, rect, borderwidth)

    def update(self):
        pygame.display.update()

    def quit(self):
        pygame.quit()
