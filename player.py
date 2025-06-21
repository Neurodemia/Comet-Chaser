import pygame
from circleshape import CircleShape
from constants import *
from bullets import Shot

class Player(CircleShape):

    def __init__(self, x, y, pew_sound=None):
        super().__init__(x, y, PLAYER_RADIUS)
        self.pew_sound = pew_sound
        self.rotation = 0
        self.timer = 0
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.blink_timer = 0
        self.image = pygame.image.load("ship.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.image = pygame.transform.scale(self.image, (60, 60))

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        if self.invulnerable and int(self.blink_timer * 10) % 2 == 0:
            # Skip drawing to create the blink effect (roughly 5 blinks per second)
            return
        rotated_image = pygame.transform.rotate(self.image, -self.rotation)
        rect = rotated_image.get_rect(center=(int(self.position.x), int(self.position.y)))
        screen.blit(rotated_image, rect)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.timer > 0:
            return
        if self.pew_sound != None:
            self.pew_sound.play()
        bullet = Shot(int(self.position.x), int(self.position.y), SHOT_RADIUS)
        vector = pygame.Vector2(0, 1)
        bullet.velocity = vector.rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.timer = SHOT_COOLDOWN


    def update(self, dt):
        self.timer -= dt
        if self.invulnerable:
            self.blink_timer += dt
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(-dt)

        if keys[pygame.K_SPACE]:
            self.shoot()

        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
