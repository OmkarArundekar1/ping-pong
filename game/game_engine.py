import pygame
import time
from .paddle import Paddle
from .ball import Ball

# ---------------------- COLORS ----------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (50, 150, 255)
GREY = (30, 30, 30)
YELLOW = (255, 215, 0)

# ----------------------------------------------------

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Game objects
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        # Game state
        self.player_score = 0
        self.ai_score = 0
        self.player_round_wins = 0
        self.ai_round_wins = 0
        self.best_of = 5
        self.win_target = 5  # points per round

        # Fonts
        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 24)

    # ----------------------------------------------------
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    # ----------------------------------------------------
    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # Scoring system
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        # Round ends at 5 points
        if self.player_score >= self.win_target or self.ai_score >= self.win_target:
            if self.player_score > self.ai_score:
                self.player_round_wins += 1
            else:
                self.ai_round_wins += 1

            # Reset for next round
            self.player_score = 0
            self.ai_score = 0
            self.ball.reset()
            pygame.time.wait(1000)

        # AI follows ball
        self.ai.auto_track(self.ball, self.height)

    # ----------------------------------------------------
    def render(self, screen):
        # Background gradient effect
        screen.fill(GREY)
        pygame.draw.rect(screen, BLUE, (0, 0, self.width, 10))  # top border
        pygame.draw.rect(screen, BLUE, (0, self.height - 10, self.width, 10))  # bottom border

        # Center line
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw paddles and ball
        pygame.draw.rect(screen, YELLOW, self.player.rect())
        pygame.draw.rect(screen, RED, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())

        # Scores
        player_text = self.font.render(str(self.player_score), True, YELLOW)
        ai_text = self.font.render(str(self.ai_score), True, RED)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

        # Round info
        round_text = self.small_font.render(
            f"Rounds: {self.player_round_wins} - {self.ai_round_wins}  (Best of {self.best_of})", True, WHITE
        )
        screen.blit(round_text, (self.width // 2 - 130, 50))

    # ----------------------------------------------------
    def check_game_over(self, screen):
        rounds_to_win = (self.best_of // 2) + 1
        if self.player_round_wins >= rounds_to_win or self.ai_round_wins >= rounds_to_win:
            winner_is_player = self.player_round_wins >= rounds_to_win
            winner_text = "PLAYER WINS THE MATCH!" if winner_is_player else "AI WINS THE MATCH!"
            color = GREEN if winner_is_player else RED

            screen.fill(BLACK)
            text_surface = self.big_font.render(winner_text, True, color)
            rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
            screen.blit(text_surface, rect)

            sub_text = self.small_font.render("Returning to menu...", True, WHITE)
            sub_rect = sub_text.get_rect(center=(self.width // 2, self.height // 2 + 40))
            screen.blit(sub_text, sub_rect)

            pygame.display.flip()
            pygame.time.wait(2000)
            self.choose_mode(screen)

    # ----------------------------------------------------
    def choose_mode(self, screen):
        screen.fill(BLACK)
        title = self.big_font.render("Ping Pong Match Setup", True, BLUE)
        title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 150))
        screen.blit(title, title_rect)

        options = [
            ("Press 3 for Best of 3", YELLOW),
            ("Press 5 for Best of 5", GREEN),
            ("Press 7 for Best of 7", RED),
            ("Press ESC to Exit", WHITE),
        ]

        for i, (text, color) in enumerate(options):
            option_surface = self.font.render(text, True, color)
            rect = option_surface.get_rect(center=(self.width // 2, self.height // 2 + i * 60))
            screen.blit(option_surface, rect)

        pygame.display.flip()

        choosing = True
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.best_of = 3
                        choosing = False
                    elif event.key == pygame.K_5:
                        self.best_of = 5
                        choosing = False
                    elif event.key == pygame.K_7:
                        self.best_of = 7
                        choosing = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
            pygame.time.wait(100)

        # Reset all stats for the new match
        self.player_score = 0
        self.ai_score = 0
        self.player_round_wins = 0
        self.ai_round_wins = 0
        self.ball.reset()
