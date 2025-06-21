import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.position = pygame.Vector2(pos)
        self.radius = 5
        self.max_radius = 40
        self.lifetime = 0.3  # seconds
        self.timer = 0
        if self.containers:
            for group in self.containers:
                group.add(self)

    def update(self, dt):
        self.timer += dt
        self.radius = 5 + (self.max_radius - 5) * (self.timer / self.lifetime)
        if self.timer >= self.lifetime:
            self.kill()

    def draw(self, surface):
        color = (255, 200, 40)
        pygame.draw.circle(surface, color, (int(self.position.x), int(self.position.y)), int(self.radius), 2)
