import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from bullets import Shot

def main():
    pygame.init()
    background_img = pygame.image.load("Nebulous.png")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    enlarged_background = pygame.transform.scale(background_img, (1080, 600))
    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()
    dt = clock.tick(60)/1000
    lives = 3
    score = 0
    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updateable, drawable)
    Asteroid.containers = (asteroids, updateable, drawable)
    Shot.containers = (shots, updateable, drawable)
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
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH - 120, 10))
        screen.blit(lives_text, (10, 10))
        updateable.update(dt)
        for asteroid in asteroids:
            for shot in shots:
                if shot.collision(asteroid):
                    asteroid.split()
                    shot.kill()
                    score += 10
            if player_1.collision(asteroid):
                lives -= 1
                if lives <= 0:
                    sys.exit("Game over!")
                else:
                    # Invulnerable?
                    player_1.position = Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        for sprite in drawable:
            sprite.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    print ("Starting Asteroids!")
    print (f"Screen width: {SCREEN_WIDTH}")
    print (f"Screen height: {SCREEN_HEIGHT}")


if __name__ == "__main__":
    main()
