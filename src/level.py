import pygame
from src.enemy import Enemy

class Level:
    """
    The Level class parses text-based maps and creates game objects.
    Enhanced for reliable coin collection and multi-level training.
    """
    def __init__(self, map_data):
        self.tile_size = 32
        self.platforms = []
        self.coins = []
        self.enemies = []
        self.goal = None
        
        # --- IMAGE LOADING ---
        try:
            self.tile_img = pygame.image.load("assets/tile.png").convert_alpha()
            self.tile_img = pygame.transform.scale(self.tile_img, (32, 32))
        except:
            self.tile_img = None

        try:
            self.coin_img = pygame.image.load("assets/coin.png").convert_alpha()
            self.coin_img = pygame.transform.scale(self.coin_img, (24, 24))
        except:
            self.coin_img = None

        try:
            self.goal_img = pygame.image.load("assets/goal.png").convert_alpha()
            self.goal_img = pygame.transform.scale(self.goal_img, (32, 64))
        except:
            self.goal_img = None

        try:
            self.bg_img = pygame.image.load("assets/background.png").convert_alpha()
            self.bg_img = pygame.transform.scale(self.bg_img, (800, 600))
        except:
            self.bg_img = None

        self.parse_map(map_data)

    def parse_map(self, map_data):
        """
        Converts map characters into game objects:
        W = Platform, C = Coin, E = Enemy, G = Goal
        """
        for row_index, row in enumerate(map_data):
            for col_index, char in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size
                
                if char == 'W':
                    self.platforms.append(pygame.Rect(x, y, 32, 32))
                elif char == 'C':
                    # Store as Rect for collision + position access
                    self.coins.append(pygame.Rect(x + 4, y + 4, 24, 24))
                elif char == 'E':
                    self.enemies.append(Enemy(x, y))
                elif char == 'G':
                    self.goal = pygame.Rect(x, y, 32, 64)

    def reset_coins(self):
        """Reset coins for new training runs on the same level."""
        # Re-parse would be better, but for simplicity we can re-init if needed
        pass

    def draw_scaled(self, surface, camera_x, camera_y, scale):
        """
        Renders the entire level with proper scaling for God View.
        """
        # Background
        if self.bg_img:
            surface.blit(self.bg_img, (0, 0))
        
        # Platforms
        for plat in self.platforms:
            draw_x = (plat.x - camera_x) * scale
            draw_y = (plat.y - camera_y) * scale
            scaled_w = int(32 * scale)
            scaled_h = int(32 * scale)
            
            if self.tile_img:
                scaled_tile = pygame.transform.scale(self.tile_img, (scaled_w, scaled_h))
                surface.blit(scaled_tile, (draw_x, draw_y))
            else:
                pygame.draw.rect(surface, (100, 100, 100), (draw_x, draw_y, scaled_w, scaled_h))
        
        # Coins
        for coin in self.coins:
            draw_x = (coin.x - camera_x) * scale
            draw_y = (coin.y - camera_y) * scale
            scaled_w = int(24 * scale)
            scaled_h = int(24 * scale)
            
            if self.coin_img:
                scaled_coin = pygame.transform.scale(self.coin_img, (scaled_w, scaled_h))
                surface.blit(scaled_coin, (draw_x, draw_y))
            else:
                pygame.draw.ellipse(surface, (255, 215, 0), (draw_x, draw_y, scaled_w, scaled_h))
        
        # Goal
        if self.goal:
            draw_x = (self.goal.x - camera_x) * scale
            draw_y = (self.goal.y - camera_y) * scale
            scaled_w = int(32 * scale)
            scaled_h = int(64 * scale)
            
            if self.goal_img:
                scaled_goal = pygame.transform.scale(self.goal_img, (scaled_w, scaled_h))
                surface.blit(scaled_goal, (draw_x, draw_y))
            else:
                pygame.draw.rect(surface, (0, 255, 0), (draw_x, draw_y, scaled_w, scaled_h))