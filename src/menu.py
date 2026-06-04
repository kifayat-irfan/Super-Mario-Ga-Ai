import pygame

class Menu:
    """
    Simple menu system to choose between Human play and AI Training.
    """
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 32)
        self.title_font = pygame.font.SysFont("Arial", 52, bold=True)

    def draw(self):
        """
        Displays the menu and returns user choice.
        """
        self.screen.fill((40, 40, 60))
        
        title = self.title_font.render("SUPER MARIO GA", True, (255, 215, 0))
        subtitle = self.font.render("Neuro-Evolutionary AI", True, (200, 200, 255))
        
        btn_human = self.font.render("1. Play as Human", True, (220, 220, 220))
        btn_ai = self.font.render("2. Start AI Training", True, (220, 220, 220))
        btn_exit = self.font.render("3. Exit", True, (220, 220, 220))
        
        self.screen.blit(title, (800//2 - title.get_width()//2, 140))
        self.screen.blit(subtitle, (800//2 - subtitle.get_width()//2, 210))
        
        self.screen.blit(btn_human, (800//2 - btn_human.get_width()//2, 300))
        self.screen.blit(btn_ai, (800//2 - btn_ai.get_width()//2, 350))
        self.screen.blit(btn_exit, (800//2 - btn_exit.get_width()//2, 400))
        
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return "HUMAN"
                    if event.key == pygame.K_2:
                        return "AI"
                    if event.key == pygame.K_3:
                        return "QUIT"
        return "QUIT"