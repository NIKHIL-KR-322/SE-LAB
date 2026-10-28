import random
import pygame

class Fruit:
    def __init__(self, screen_width, speed_bonus=0):
        self.screen_width = screen_width
        self.radius = 14
        self.x = random.randint(30, screen_width - 30)
        self.y = -self.radius * 2

        # Task 3: increase falling speed as score increases
        self.speed = random.uniform(4.0, 6.5) + speed_bonus

        # Task 2: 15% chance of being a hazard
        self.is_hazard = random.random() < 0.15

        if self.is_hazard:
            self.color = (30, 30, 30)
        else:
            self.color = random.choice([
                (230, 45, 45),   # Apple
                (245, 140, 30),  # Orange
                (160, 60, 200),  # Grape
            ])

    def update(self):
        self.y += self.speed

    def is_missed(self, screen_height):
        return self.y > screen_height

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def render(self, surface):
        center = (int(self.x), int(self.y))

        if self.is_hazard:
            # Draw hazard
            pygame.draw.circle(
                surface,
                self.color,
                center,
                self.radius
            )

            # Green X
            pygame.draw.line(
                surface,
                (80, 220, 80),
                (
                    int(self.x - 10),
                    int(self.y - 10)
                ),
                (
                    int(self.x + 10),
                    int(self.y + 10)
                ),
                3
            )

            pygame.draw.line(
                surface,
                (80, 220, 80),
                (
                    int(self.x + 10),
                    int(self.y - 10)
                ),
                (
                    int(self.x - 10),
                    int(self.y + 10)
                ),
                3
            )

        else:
            # Draw normal fruit
            pygame.draw.circle(
                surface,
                self.color,
                center,
                self.radius
            )

            pygame.draw.circle(
                surface,
                (255, 255, 255),
                (
                    int(self.x - 4),
                    int(self.y - 4)
                ),
                3
            )