import pygame
import time
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # Default win target (Best of 5)
        self.win_target = 5

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # Scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        # AI paddle follows ball
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

    def check_game_over(self, screen):
        """Show winner and replay options if target score reached."""
        if self.player_score >= self.win_target or self.ai_score >= self.win_target:
            winner_is_player = self.player_score >= self.win_target
            winner_text = "Player Wins!" if winner_is_player else "AI Wins!"
            color = GREEN if winner_is_player else RED

            screen.fill(BLACK)
            winner_surface = self.font.render(winner_text, True, color)
            winner_rect = winner_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
            screen.blit(winner_surface, winner_rect)

            # Replay options
            options_font = pygame.font.SysFont("Arial", 24)
            options = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit"
            ]
            for i, text in enumerate(options):
                opt_surface = options_font.render(text, True, WHITE)
                opt_rect = opt_surface.get_rect(center=(self.width // 2, self.height // 2 + 30 + i * 40))
                screen.blit(opt_surface, opt_rect)

            pygame.display.flip()

            # Wait for replay choice
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_3:
                            self.win_target = 3
                            waiting = False
                        elif event.key == pygame.K_5:
                            self.win_target = 5
                            waiting = False
                        elif event.key == pygame.K_7:
                            self.win_target = 7
                            waiting = False
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()

                pygame.time.wait(100)

            # Reset scores and ball for new match
            self.player_score = 0
            self.ai_score = 0
            self.ball.reset()
