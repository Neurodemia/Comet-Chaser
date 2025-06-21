import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, surface):
        center = (int(self.position.x), int(self.position.y))
        pygame.draw.circle(surface, "white", center, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            random_angle = random.uniform(20, 50)
            velocity_1 = self.velocity.rotate(random_angle)
            velocity_2 = self.velocity.rotate(-random_angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            split1 = Asteroid(self.position.x, self.position.y, new_radius)
            split2 = Asteroid(self.position.x, self.position.y, new_radius)
            split1.velocity = velocity_1 * 1.2
            split2.velocity = velocity_2 * 1.2
