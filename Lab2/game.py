import pygame
import random
from pygame import mixer

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Scavenger")

player_img = pygame.image.load("Lab2/assets/spaceship.png")
asteroid_img = pygame.image.load("Lab2/assets/asteroid.png")
crystal_img = pygame.image.load("Lab2/assets/energy_crystal.png")

player_img = pygame.transform.scale(player_img, (64, 64))
asteroid_img = pygame.transform.scale(asteroid_img, (48, 48))
crystal_img = pygame.transform.scale(crystal_img, (32, 32))

mixer.music.load("Lab2/assets/background_music.wav")
collision_sound = mixer.Sound("Lab2/assets/clash_sound.wav")

mixer.music.play(-1)
mixer.music.set_volume(0.5)


class Player:
    def __init__(self):
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5
        self.score = 0
        self.dragging = False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0]:
            mouse_x = mouse_pos[0]
            if abs(mouse_x - self.rect.centerx) > self.speed:
                if mouse_x < self.rect.centerx and self.rect.left > 0:
                    self.rect.x -= self.speed
                elif mouse_x > self.rect.centerx and self.rect.right < SCREEN_WIDTH:
                    self.rect.x += self.speed


class GameObject:
    def __init__(self, image, is_asteroid=True, difficulty_level=1):
        self.base_image = image
        self.is_asteroid = is_asteroid
        if is_asteroid:
            size = int(48 * (1 + 0.1 * (difficulty_level - 1)))
            self.image = pygame.transform.scale(self.base_image, (size, size))
        else:
            self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.uniform(2, 5) if is_asteroid else 3

    def move(self):
        self.rect.y += self.speed
        return self.rect.top > SCREEN_HEIGHT


class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Game:
    def __init__(self):
        self.player = Player()
        self.asteroids = []
        self.crystals = []
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.spawn_timer = 0
        self.difficulty_timer = 0
        self.difficulty_level = 1
        self.font = pygame.font.Font(None, 36)

        self.end_button = Button(
            SCREEN_WIDTH - 110, 10, 100, 40, "End", (255, 0, 0))
        self.restart_button = Button(
            SCREEN_WIDTH - 220, 10, 100, 40, "Restart", (0, 255, 0))

    def spawn_objects(self):
        self.spawn_timer += 1
        if self.spawn_timer >= 60:
            self.spawn_timer = 0
            if random.random() < 0.7:
                self.asteroids.append(GameObject(
                    asteroid_img, True, self.difficulty_level))
            else:
                self.crystals.append(GameObject(crystal_img, False))

    def increase_difficulty(self):
        self.difficulty_timer += 1
        if self.difficulty_timer >= 1000:
            self.difficulty_timer = 0
            self.difficulty_level += 1
            self.player.speed += 0.5
            for asteroid in self.asteroids:
                asteroid.speed += 0.5

    def check_collisions(self):
        for crystal in self.crystals[:]:
            if self.player.rect.colliderect(crystal.rect):
                self.crystals.remove(crystal)
                self.player.score += 10

        for asteroid in self.asteroids[:]:
            if self.player.rect.colliderect(asteroid.rect):
                collision_sound.play()
                self.game_over = True
                return

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and self.game_over:
                    if event.key == pygame.K_RETURN:
                        self.__init__()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.end_button.is_clicked(mouse_pos):
                        running = False
                    elif self.restart_button.is_clicked(mouse_pos):
                        self.__init__()

            if not self.game_over:
                self.player.move()
                self.spawn_objects()
                self.increase_difficulty()

                for asteroid in self.asteroids[:]:
                    if asteroid.move():
                        self.asteroids.remove(asteroid)

                for crystal in self.crystals[:]:
                    if crystal.move():
                        self.crystals.remove(crystal)

                self.check_collisions()

            screen.fill((0, 0, 0))

            screen.blit(self.player.image, self.player.rect)
            for asteroid in self.asteroids:
                screen.blit(asteroid.image, asteroid.rect)
            for crystal in self.crystals:
                screen.blit(crystal.image, crystal.rect)

            score_text = self.font.render(
                f"Score: {self.player.score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            self.end_button.draw(screen)
            self.restart_button.draw(screen)

            if self.game_over:
                game_over_text = self.font.render(
                    "Game Over! Press ENTER to restart", True, (255, 0, 0))
                screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2,
                                             SCREEN_HEIGHT//2 - game_over_text.get_height()//2))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
