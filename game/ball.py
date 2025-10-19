import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        # Initialize pygame mixer once
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Load sound effects
        self.sound_paddle = pygame.mixer.Sound("assets/sounds/paddle_hit.wav")
        self.sound_wall = pygame.mixer.Sound("assets/sounds/wall_bounce.wav")
        self.sound_score = pygame.mixer.Sound("assets/sounds/score.wav")

        # Ball properties
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        """Move the ball and bounce off top/bottom walls."""
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            self.sound_wall.play()

    def check_collision(self, player, ai):
        """Check for paddle collisions and reverse direction."""
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()

        # Player paddle collision
        if ball_rect.colliderect(player_rect):
            self.x = player_rect.right
            self.velocity_x *= -1
            self.sound_paddle.play()

        # AI paddle collision
        elif ball_rect.colliderect(ai_rect):
            self.x = ai_rect.left - self.width
            self.velocity_x *= -1
            self.sound_paddle.play()

    def reset(self):
        """Reset ball to center with reversed direction."""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
        self.sound_score.play()  # play scoring sound

    def rect(self):
        """Return ball rectangle for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
