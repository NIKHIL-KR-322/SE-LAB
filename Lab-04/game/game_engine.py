import pygame
import random
from game.basket import Basket
from game.fruit import Fruit


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.basket = Basket(width, height)
        self.fruits = []

        self.score = 0
        self.lives = 3

        # Task 3
        self.spawn_delay = 750
        self.last_spawn_time = pygame.time.get_ticks()

        self.game_state = "PLAYING"

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_medium = pygame.font.SysFont(None, 28)

        # Task 4: particle list
        self.particles = []

    def handle_event(self, event):
        if self.game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

    # Task 4: create splash particles
    def create_particles(self, x, y, color):
        for _ in range(12):
            particle = {
                "x": x,
                "y": y,
                "dx": random.uniform(-3, 3),
                "dy": random.uniform(-4, -1),
                "life": random.randint(20, 35),
                "color": color
            }

            self.particles.append(particle)

    # Task 4: update particles
    def update_particles(self):
        for particle in self.particles[:]:

            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]

            # Gravity
            particle["dy"] += 0.2

            particle["life"] -= 1

            if particle["life"] <= 0:
                self.particles.remove(particle)

    # Task 4: draw particles
    def render_particles(self, screen):
        for particle in self.particles:

            pygame.draw.circle(
                screen,
                particle["color"],
                (
                    int(particle["x"]),
                    int(particle["y"])
                ),
                3
            )

    def update(self):
        if self.game_state != "PLAYING":
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.basket.move_left()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.basket.move_right()

        now = pygame.time.get_ticks()

        # Task 3: dynamic difficulty
        if now - self.last_spawn_time >= self.spawn_delay:

            speed_bonus = min(
                self.score * 0.15,
                3.0
            )

            self.fruits.append(
                Fruit(
                    self.width,
                    speed_bonus
                )
            )

            self.spawn_delay = max(
                300,
                750 - self.score * 15
            )

            self.last_spawn_time = now

        basket_rect = self.basket.rect

        for fruit in self.fruits[:]:

            fruit.update()

            # Fruit caught by basket
            if basket_rect.colliderect(fruit.rect):

                if fruit.is_hazard:

                    self.lives -= 1

                    if self.lives <= 0:
                        self.game_state = "GAME_OVER"

                else:

                    self.score += 1

                    # Task 4:
                    # Create particles using fruit color
                    self.create_particles(
                        fruit.x,
                        fruit.y,
                        fruit.color
                    )

                self.fruits.remove(fruit)
                continue

            # Fruit missed
            if fruit.is_missed(self.height):

                # Task 4:
                # Create splash at floor
                self.create_particles(
                    fruit.x,
                    self.height - 25,
                    fruit.color
                )

                self.lives -= 1

                if self.lives <= 0:
                    self.game_state = "GAME_OVER"

                self.fruits.remove(fruit)

        # Task 4: update particles
        self.update_particles()

    def reset(self):
        self.basket = Basket(
            self.width,
            self.height
        )

        self.fruits.clear()

        # Task 4
        self.particles.clear()

        self.score = 0
        self.lives = 3

        self.last_spawn_time = pygame.time.get_ticks()

        self.game_state = "PLAYING"

    def render(self, screen):

        screen.fill(
            (28, 32, 40)
        )

        ground_y = self.height - 25

        pygame.draw.rect(
            screen,
            (45, 50, 60),
            (
                0,
                ground_y,
                self.width,
                25
            )
        )

        self.basket.render(screen)

        for fruit in self.fruits:
            fruit.render(screen)

        # Task 4: render particles
        self.render_particles(screen)

        # Score
        score_surf = self.font_medium.render(
            f"Score: {self.score}",
            True,
            (255, 220, 80)
        )

        screen.blit(
            score_surf,
            (25, 20)
        )

        # Lives
        lives_surf = self.font_medium.render(
            f"Lives: {self.lives}",
            True,
            (240, 80, 80)
        )

        screen.blit(
            lives_surf,
            (
                self.width - lives_surf.get_width() - 25,
                20
            )
        )

        # Game Over
        if self.game_state == "GAME_OVER":

            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 190)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            over_surf = self.font_big.render(
                "GAME OVER",
                True,
                (235, 70, 70)
            )

            screen.blit(
                over_surf,
                (
                    self.width // 2 -
                    over_surf.get_width() // 2,
                    self.height // 2 - 40
                )
            )

            final_surf = self.font_medium.render(
                f"Final Score: {self.score}",
                True,
                (255, 255, 255)
            )

            screen.blit(
                final_surf,
                (
                    self.width // 2 -
                    final_surf.get_width() // 2,
                    self.height // 2 + 10
                )
            )

            restart_surf = self.font_medium.render(
                "Press [R] to Play Again",
                True,
                (200, 200, 200)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2 -
                    restart_surf.get_width() // 2,
                    self.height // 2 + 50
                )
            )