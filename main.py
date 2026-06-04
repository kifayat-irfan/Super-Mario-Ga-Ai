import pygame
from src.game import Game
from src.trainer import Trainer
from src.menu import Menu

def show_victory_screen(screen, score, level):
    """
    Displays victory message after completing a level or the full game.
    """
    font_large = pygame.font.SysFont("Comic Sans MS", 60, bold=True)
    font_small = pygame.font.SysFont("Arial", 30)
    
    waiting = True
    while waiting:
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        
        msg1 = font_large.render("MISSION COMPLETE!", True, (255, 215, 0))
        msg2 = font_small.render(f"Level {level} Cleared!", True, (255, 255, 255))
        msg3 = font_small.render(f"Score: {score}", True, (0, 255, 0))
        msg4 = font_small.render("Press ANY KEY to continue", True, (200, 200, 200))
        
        screen.blit(msg1, (800//2 - msg1.get_width()//2, 180))
        screen.blit(msg2, (800//2 - msg2.get_width()//2, 280))
        screen.blit(msg3, (800//2 - msg3.get_width()//2, 330))
        screen.blit(msg4, (800//2 - msg4.get_width()//2, 420))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Super Mario GA AI - Neuroevolution")
    
    game_menu = Menu(screen)
    
    running = True
    while running:
        choice = game_menu.draw()
        
        if choice == "QUIT":
            running = False
            
        elif choice == "HUMAN":
            game = Game(mode='human')
            game.reset(population_size=1)
            
            game_running = True
            while game_running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_running = False
                        running = False
                
                status = game.run_single_frame()
                
                if status == "WIN":
                    show_victory_screen(screen, game.players[0].score, game.current_level_num)
                    
                    if game.current_level_num < 3:
                        game.current_level_num += 1
                        game.reset(population_size=1)
                    else:
                        print("All levels completed in Human Mode!")
                        game_running = False
                        
                elif status == "DEAD":
                    # Respawn
                    game.players[0].reset_position(50, 100)
                    game.players[0].is_alive = True
                
                game.draw()
                game.clock.tick(60)

        elif choice == "AI":
            print("Starting Neuro-Evolutionary Training...")
            trainer = Trainer()
            trainer.train(render_mode=True)
            print("Training finished. Best models saved in 'saved_models/'.")

    pygame.quit()

if __name__ == "__main__":
    main()