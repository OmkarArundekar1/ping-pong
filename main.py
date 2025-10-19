import pygame
from game.game_engine import GameEngine

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🏓 Ping Pong - Pygame Edition")

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Game engine
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    engine.choose_mode(SCREEN)  # Show mode selection first

    while running:
        SCREEN.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Core gameplay
        engine.handle_input()
        engine.update()
        engine.render(SCREEN)
        engine.check_game_over(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
