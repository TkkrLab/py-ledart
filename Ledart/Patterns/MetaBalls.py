from Ledart import Graphics, BLACK, BLUE, RED, WHITE
from Ledart import translate
from Ledart import Vector

from colorsys import *
import random

class Ball(object):
    def __init__(self, g=None, x=0, y=0, size=1):
        self.accel = Vector(x=0, y=0)
        self.speed = Vector(x=0, y=0)
        self.pos = Vector(x=x, y=y)
        self.drag = 0.9989
        self.size = size
        self.g = g
        self.mass = self.size ** 6 / 2
        self.max_speed = 0

    def update(self):
        self.speed += self.accel
        self.speed *= self.drag
        self.pos += self.speed
        self.accel *= 0

        self.handle_collision()

    def handle_collision(self):
        if (self.pos.x - self.size < 0 or
            self.pos.x > self.g.width - self.size):
            self.pos -= self.speed
            self.speed.x *= -1
        if (self.pos.y - self.size < 0 or 
            self.pos.y > self.g.height - self.size):
            self.pos -= self.speed
            self.speed.y *= -1

    def draw(self):
        self.g.draw_circle(self.pos.x, self.pos.y, self.size, BLACK)


class MetaBalls(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.balls = []
        for i in range(10):
            size = random.randint(4, 10)
            x = random.randint(size, self.width - size)
            y = random.randint(size, self.height - size)
            ball = Ball(g=self, x=x, y=y, size=size)
            ball.speed += (random.randint(0, 100) - 50) / 100.
            self.balls.append(ball)
        self.max = 0
        self.totalballsize = 0
        for ball in self.balls:
            self.totalballsize += ball.size
 
    def generate(self):
        self.fill(BLACK)

        for point in self.indexes:
            x, y = point
            sumc = 0
            
            for ball in self.balls:
                distance = (ball.pos.dist(Vector(x=x, y=y)) + 1)
                sumc += ball.size / distance

            # color = min(sumc * 80, 0xff) / 0xff
            # print(sumc)
            colorfunc = hsv_to_rgb
            color = min(sumc * (0x80 - self.totalballsize), 0xff) / 0xff
            self[point] = [int(c * 0xff) for c in colorfunc(1 - color, 1, 1)]


        for ball in self.balls:
            ball.update()
            # ball.draw()
            for otherball in self.balls:
                if ball != otherball: #and ball.pos.dist(otherball.pos) < self.width / 4:
                    force = ball.pos - otherball.pos
                    dist = max(force.mag, ball.size)
                    force = force.normalize()
                    G = 6.67191*(10**-11)
                    strength = (G * ball.mass * otherball.mass) / (dist ** 2)
                    force *= strength
                    ball.accel -= force
