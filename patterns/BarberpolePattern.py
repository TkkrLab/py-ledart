# Barberpole pattern was originally made in C by Duality
# then edited by aprogas to make it work in python.


class BarberpolePattern:
    # Rotating stripes of certain colors, default red/white
    def __init__(self, backwards=False, color1=(0, 0, 255),
                 color2=(128, 128, 128)):
        self.backwards = backwards
        self.color1 = color1
        self.color2 = color2
        self.pos = 0

        self.width = 10
        self.height = 17
        self.size = self.width * self.height

    def generate(self):
        data = []
        if self.backwards:
            leds = range(self.size, 0, 1)
        else:
            leds = range(0, self.size, 1)
        for i in leds:
            place = (i % self.width) + self.pos
            if (place >= self.width):
                place -= self.width
            if (place < self.width / 2):
                data.append(self.color1)
            else:
                data.append(self.color2)
        self.pos += 1
        if (self.pos >= self.width):
            self.pos = 0
        return data
