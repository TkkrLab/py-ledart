
class PygameDummyController(object):
    def __init__(self, plugged=0):
        self.default = 1.0
    def getAxis(self, button):
        return self.default
    def getButtons(self, button):
        return int(self.default)
    def getHats(self, button):
        return int(self.default)

class PygameController(object):
    import pygame
    #axis for which axis to read (button)
    #plugged for which controller to select
    def __init__(self, plugged=0):
        self.pygame.init()
        self.joystick = self.pygame.joystick.Joystick(plugged)
        self.joystick.init()

        self.num_axis = self.joystick.get_numaxes()
        self.num_buttons = self.joystick.get_numbuttons()
        self.num_hats = self.joystick.get_numhats()
    def handleEvents(self):
        self.pygame.event.pump()
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                sys.exit(0)
    def getAxis(self, button):
        self.handleEvents()
        if self.num_axis:
            return self.joystick.get_axis(button)
        else:
            raise ControllerError("No Axis")
    def getButtons(self, button):
        self.handleEvents()
        if self.num_buttons:
            return self.joystick.get_button(button)
        else:
            raise ControllerError("No Buttons")

    def getHats(self, button):
        self.handleEvents()
        if self.num_hats:
            return self.joystick.get_hat(button)
        else:
            raise ControllerError("No Hats")
    def __del__(self):
        self.pygame.quit()