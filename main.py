import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from bullets import Shot
from pygame.math import Vector2
from explosion import Explosion
from particle import Particle

def main():
    pygame.init()
    background_img = pygame.image.load("Nebulous.png")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    enlarged_background = pygame.transform.scale(background_img, (1080, 600))
    font = pygame.font.Font("Orbitron-SemiBold.ttf", 36)
    life_icon = pygame.image.load("health_ship.png")
    life_icon = pygame.transform.scale(life_icon, (32, 32))
    clock = pygame.time.Clock()
    dt = clock.tick(60)/1000
    lives = 3
    score = 0
    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    Player.containers = (updateable, drawable)
    Asteroid.containers = (asteroids, updateable, drawable)
    Shot.containers = (shots, updateable, drawable)
    Explosion.containers = (explosions, updateable, drawable)
    Particle.containers = (particles, updateable, drawable)
    AsteroidField.containers = (updateable)
    player_1 = Player(x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2)
    img_x = (SCREEN_WIDTH - 1080) // 2
    img_y = (SCREEN_HEIGHT - 600) // 2
    field = AsteroidField()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        screen.blit(enlarged_background, (img_x, img_y))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (999, 10))
        for i in range(lives):
            x = 20 + i * (32 + 8)  # 8 pixels between icons
            y = 10
            screen.blit(life_icon, (x, y))
        updateable.update(dt)
        for asteroid in asteroids:
            for shot in shots:
                if shot.collision(asteroid):
                    explosion = Explosion(asteroid.position)
                    explosions.add(explosion)
                    asteroid.split()
                    shot.kill()
                    score += 10
            if not player_1.invulnerable and player_1.collision(asteroid):
                lives -= 1
                if lives <= 0:
                    sys.exit("Game over!")
                else:
                    player_1.position = Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    player_1.invulnerable = True
                    player_1.invulnerable_timer = 2.0 # seconds
                    player_1.blink_timer = 0
        explosions.update(dt)
        particles.update(dt)
        for sprite in drawable:
            sprite.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    print ("Starting Asteroids!")
    print (f"Screen width: {SCREEN_WIDTH}")
    print (f"Screen height: {SCREEN_HEIGHT}")


if __name__ == "__main__":
    main()
