import pygame
import math
import random
from circleshape import CircleShape
from constants import *
from particle import Particle

class Asteroid(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        if self.containers:
            for group in self.containers:
                group.add(self)
        if radius < ASTEROID_LARGE_MIN_RADIUS:  # define this appropriately!
            self.points = self.generate_lumpy_shape()
            self.image = None
        else:
            self.points = None
            self.image = pygame.image.load("comet.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (2.5 * radius, 2.5 * radius))  # Ensures comet sprite fits asteroid size
            if radius >= ASTEROID_LARGE_MIN_RADIUS:
                self.rotation = random.uniform(0, 360)  # Start at a random angle for variety
                self.rotation_speed = random.uniform(-60, 60)  # Degrees per second, positive or negative

    def draw(self, surface):
        if self.radius <= ASTEROID_MIN_RADIUS:
            direction = self.velocity.normalize() if self.velocity.length() > 0 else pygame.Vector2(1, 0)
            angle = direction.angle_to(pygame.Vector2(-1, 0))
            tail_length = int(self.radius * 3)
            tail_width = int(self.radius * 1.5)
            tail_surf = pygame.Surface((tail_length, tail_width), pygame.SRCALPHA)
            tail_color = (150, 220, 255, 100)
            pygame.draw.ellipse(tail_surf, tail_color, (0, 0, tail_length, tail_width))
            rotated_tail = pygame.transform.rotate(tail_surf, angle)
            offset = -direction * self.radius
            tail_rect = rotated_tail.get_rect(center=(int(self.position.x + offset.x), int(self.position.y + offset.y)))
            surface.blit(rotated_tail, tail_rect)
        if self.image:
            rotated_image = pygame.transform.rotate(self.image, self.rotation)
            rect = rotated_image.get_rect(center=(int(self.position.x), int(self.position.y)))
            surface.blit(rotated_image, rect)
        elif self.points is not None:
            points = [
                (int(self.position.x + dx), int(self.position.y + dy))
                for (dx, dy) in self.points
            ]
            pygame.draw.polygon(surface, (120, 120, 120), points)
        else:
            center = (int(self.position.x), int(self.position.y))
            pygame.draw.circle(surface, "white", center, self.radius)

    def update(self, dt):
        self.position += self.velocity * dt
        if self.image:
            self.rotation += self.rotation_speed * dt

    def split(self):
        self.kill()
        if ASTEROID_MIN_RADIUS < self.radius < ASTEROID_LARGE_MIN_RADIUS:
            for _ in range(40):
                Particle(self.position)
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

    def generate_lumpy_shape(self, num_points=12, irregularity=0.4):
        angle_step = 2 * math.pi / num_points
        offsets = []
        for i in range(num_points):
            theta = i * angle_step
            # Jitter the radius
            offset = random.uniform(1-irregularity, 1+irregularity)
            r = self.radius * offset
            dx = r * math.cos(theta)
            dy = r * math.sin(theta)
            offsets.append((dx, dy))
        return offsets
