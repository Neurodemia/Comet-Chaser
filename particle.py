import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.position = pygame.Vector2(pos)
        angle = random.uniform(0, 360)
        speed = random.uniform(50, 150)
        self.velocity = pygame.Vector2(speed, 0).rotate(angle)
        self.lifetime = random.uniform(0.3, 0.6)
        self.timer = 0
        self.color = (180, 170, 150)  # Dusty gray
        self.radius = random.randint(2, 4)
        if self.containers:
            for group in self.containers:
                group.add(self)

    def update(self, dt):
        self.position += self.velocity * dt
        self.timer += dt
        if self.timer > self.lifetime:
            self.kill()

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.position.x), int(self.position.y)), self.radius)
