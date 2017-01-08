from Interface import Interface

from pygame.locals import *
import pygame
import os


class PygameInterface(Interface):
    """
    a abstract drawing interface that uses pygame.
    """
    def __init__(self, width, height, blocksize, fullscreen=False):
        Interface.__init__(self, width, height, blocksize)
        self.flags = pygame.NOFRAME
        if fullscreen:
            self.flags |= pygame.FULLSCREEN

        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
        self.window = pygame.display.set_mode((self.width, self.height),
                                              self.flags)
        if blocksize < 7:
            self.pixelsurface = pygame.Surface((blocksize, blocksize))
        else:
            self.pixelsurface = pygame.Surface((blocksize - 2, blocksize - 2))

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
            # focused = pygame.mouse.get_focused()
            # pygame.mouse.set_visible(not focused)

    def setcaption(self, caption):
        pygame.display.set_caption(caption + " (pygame)")

    def clear(self, color):
        self.window.fill(color)

    def drawblock(self, rect, color):
        self.pixelsurface.fill(color)
        self.window.blit(self.pixelsurface, rect)

    def update(self):
        pygame.display.flip()

    def quit(self):
        pygame.quit()
