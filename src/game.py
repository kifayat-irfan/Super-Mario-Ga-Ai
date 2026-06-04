import pygame
import numpy as np
from src.player import Player
from src.level import Level

class Game:
    """
    Optimized Game Engine for fast neuroevolution training.
    Reduced collision checks and improved performance.
    """
    def __init__(self, mode='human'):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.mode = mode
        self.scale = 0.5 if mode == 'ai' else 1.0 
        
        self.levels = {
            1: ["                                      G", "                                     WW", "    C      E      C                   W", "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"],
            2: ["                                      G", "                  WWWW                W", "        C        WWWWWWWW             W", "    WWWWWW      W    W           E    W", "    W    W      W    W      C         W", "WWWW     WWWWWWWW    WWWWWWWWWWWWWWWWWWW"],
            3: ["                                      G", "      W                               W", "      W      C       E                W", "    WWWWW   WWWW  C  WWWW   C   E     W", "    W       W    W  S    W   WWWW     W", "WWWW    C   WWWWWW  WWWWWW  W         W", "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"]
        }
        
        self.current_level_num = 1
        self.setup_level(population_size=1)

    def setup_level(self, population_size=1):
        self.map_data = self.levels[self.current_level_num]
        self.level = Level(self.map_data)
        self.players = [Player(50, 100) for _ in range(population_size)]
        self.camera_x = 0
        self.camera_y = -250 if self.mode == 'ai' else 0

    def reset(self, population_size=1):
        self.setup_level(population_size)

    def get_ai_inputs(self, player):
        """Fast 16-input sensor system"""
        # Enemy sensing (optimized)
        min_enemy_dist = 1000.0
        enemy_y_diff = 0.0
        for e in self.level.enemies:
            dist = e.rect.x - player.rect.x
            if 0 < dist < min_enemy_dist:
                min_enemy_dist = dist
                enemy_y_diff = (e.rect.y - player.rect.y) / 300.0

        # Coin sensing (optimized)
        min_coin_dist = 1000.0
        coin_direction = 0.0
        coin_y_diff = 0.0
        for c in self.level.coins:
            dist = abs(c.x - player.rect.x)
            if dist < min_coin_dist and dist > 5:
                min_coin_dist = dist
                coin_direction = 1.0 if c.x > player.rect.x else -1.0
                coin_y_diff = (c.y - player.rect.y) / 300.0

        dist_to_goal = (self.level.goal.x - player.rect.x) / 2000.0 if self.level.goal else 1.0

        # Simplified & faster ray sensors
        ray_down = 1.0
        for plat in self.level.platforms[:8]:  # Limit checks
            if abs(plat.top - player.rect.bottom) < 120:
                if player.rect.right + 60 > plat.left and player.rect.left - 60 < plat.right:
                    ray_down = min(ray_down, (plat.top - player.rect.bottom) / 180.0)

        return [
            min_enemy_dist / 800.0,           # 0
            min_coin_dist / 800.0,            # 1
            coin_direction,                   # 2
            dist_to_goal,                     # 3
            player.rect.x / 2000.0,           # 4
            player.rect.y / 600.0,            # 5
            player.vel_x / 8.0,               # 6
            player.vel_y / 12.0,              # 7
            1.0 if player.on_ground else 0.0, # 8
            0.8,                              # 9  ray_front (simplified)
            ray_down,                         # 10
            0.9,                              # 11 ray_down_left
            0.9,                              # 12 ray_down_right
            enemy_y_diff,                     # 13
            coin_y_diff,                      # 14
            min(player.stuck_counter / 80.0, 1.0)  # 15
        ]

    def run_single_frame(self, ai_brain=None):
        """Human mode - unchanged logic"""
        if not self.players:
            return "DEAD"
        player = self.players[0]

        if self.mode == 'human':
            keys = pygame.key.get_pressed()
            direction = 0
            if keys[pygame.K_LEFT]: direction = -1
            elif keys[pygame.K_RIGHT]: direction = 1
            player.move(direction)
            if keys[pygame.K_SPACE]: player.jump()
        elif self.mode == 'ai' and ai_brain:
            inputs = self.get_ai_inputs(player)
            output = ai_brain.forward(inputs)
            action = np.argmax(output)
            if action == 0: player.move(-1)
            elif action == 1: player.move(1)
            elif action == 2: player.jump()

        player.update(self.level.platforms)
        
        self.camera_x = player.rect.x - 400
        self.camera_y = player.rect.y - 300

        for enemy in self.level.enemies:
            enemy.update(self.level.platforms)
            
        # Optimized coin collection
        for coin in self.level.coins[:]:
            if player.rect.colliderect(coin):
                player.coins_collected += 1
                player.score += 10
                self.level.coins.remove(coin)
                
        for enemy in self.level.enemies:
            if player.rect.colliderect(enemy.rect):
                player.die()
                return "DEAD"

        if self.level.goal and player.rect.colliderect(self.level.goal):
            player.reached_goal = True
            return "WIN"
        if player.rect.y > 1200 or not player.is_alive:
            return "DEAD"
        return "ALIVE"

    def run_parallel_frame(self, brains):
        """Fast parallel simulation for training"""
        statuses = []
        for i, player in enumerate(self.players):
            if not player.is_alive:
                statuses.append("DEAD")
                continue
                
            inputs = self.get_ai_inputs(player)
            output = brains[i].forward(inputs)
            action = np.argmax(output)
            
            if action == 0: player.move(-1)
            elif action == 1: player.move(1)
            elif action == 2: player.jump()
            
            player.update(self.level.platforms)
            
            status = "ALIVE"
            if self.level.goal and player.rect.colliderect(self.level.goal):
                player.reached_goal = True
                status = "WIN"
            if player.rect.y > 1200:
                status = "DEAD"
            
            # Optimized enemy collision
            for enemy in self.level.enemies:
                if player.rect.colliderect(enemy.rect):
                    player.die()
                    status = "DEAD"
                    break
                    
            statuses.append(status)
        
        # Global enemy update (once per frame)
        for enemy in self.level.enemies:
            enemy.update(self.level.platforms)
        
        self.camera_x = 0
        self.camera_y = -250
        return statuses

    def draw(self):
        """Rendering - only called occasionally"""
        self.screen.fill((135, 206, 235))
        self.level.draw_scaled(self.screen, self.camera_x, self.camera_y, self.scale)
        
        for i, player in enumerate(self.players):
            if player.is_alive:
                is_best = (i == 0)
                player.draw_scaled(self.screen, self.camera_x, self.camera_y, self.scale, is_best=is_best)
        
        for enemy in self.level.enemies:
            enemy.draw_scaled(self.screen, self.camera_x, self.camera_y, self.scale)
        
        font = pygame.font.SysFont("Arial", 24, bold=True)
        text = font.render(f"Level: {self.current_level_num}", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))
        pygame.display.flip()