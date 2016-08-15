import random
import math

from Ledart.matrix import matrix_width, matrix_height
from Ledart.Tools import Graphics, BLUE, WHITE, BLACK


class Particle(object):
    def __init__(self, (x, y), size, mass=1):
        self.x = x
        self.y = y
        self.size = size
        self.mass = mass
        self.color = WHITE
        self.wall = 1
        self.speed = random.random()
        self.angle = random.random() * (2 * math.pi)
        self.drag = 0.999
        self.elasticity = 0.75

    def move(self, gravity):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        myvec = (self.angle, self.speed)
        myvec = self.addVectors(myvec, gravity)
        self.angle, speed = myvec
        self.speed *= self.drag

    def bounce(self, width, height):
        if self.x > (width - self.size):
            self.x = 2 * (width - self.size) - self.x
            self.angle = -self.angle
            self.speed *= self.elasticity
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = -self.angle
            self.speed *= self.elasticity
        if self.y > (height - self.size):
            self.y = 2 * (height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity
        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity

    def collide(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        
        dist = math.hypot(dx, dy)
        if dist < self.size + other.size:
            angle = math.atan2(dy, dx) + 0.5 * math.pi
            total_mass = self.mass + other.mass

            (self.angle, self.speed) = self.addVectors((self.angle, self.speed*(self.mass-other.mass)/total_mass), (angle, 2*other.speed*other.mass/total_mass))
            (other.angle, other.speed) = self.addVectors((other.angle, other.speed*(other.mass-self.mass)/total_mass), (angle+math.pi, 2*self.speed*self.mass/total_mass))
            self.speed *= self.elasticity
            other.speed *= other.elasticity

            overlap = 0.5*(self.size + other.size - dist+1)
            self.x += math.sin(angle)*overlap
            self.y -= math.cos(angle)*overlap
            other.x -= math.sin(angle)*overlap
            other.y += math.cos(angle)*overlap

    def addVectors(self, (angle1, length1), (angle2, length2)):
        x = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y = math.cos(angle1) * length1 + math.cos(angle2) * length2
        angle = 0.5 * math.pi - math.atan2(y, x)
        length = math.hypot(x, y)
        return (angle, length)

    def draw(self, g):
        g.draw_circle(self.x, self.y, self.size, self.color)

class Sim(Graphics):
    def __init__(self):
        self.width = matrix_width
        self.height = matrix_height
        Graphics.__init__(self, self.width, self.height)
        self.fill(BLACK)
        self.gravity = (math.pi, 0.06)
        self.particles = []
        for n in xrange(self.width * 7):
            size = 0
            x = random.randint(size, self.width - size)
            y = random.randint(size, self.height - size)
            density = random.randint(1, 20)
            particle = Particle((x, y), size, (density * size)**2)
            particle.color = [200 - density * 10, 200 - density * 10, 0xff]
            self.particles.append(particle)

    def generate(self):
        self.fill(BLACK)
        for i, particle in enumerate(self.particles):
            particle.move(self.gravity)
            particle.bounce(self.width, self.height)
            for other in self.particles[i+1:]:
                particle.collide(other)
            particle.draw(self)
