import pygame
import random 
from src.physics import Physics

class Player:
    """
    The Player class handles the movement, jumping, and collision logic for Mario.
    Enhanced with behavioral tracking to support advanced fitness evaluation
    and Completionist evolution.
    """
    def __init__(self, x, y):
        self.width = 32
        self.height = 32
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # --- IMAGE LOADING ---
        try:
            self.image = pygame.image.load("assets/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except:
            self.image = None  # Fallback to colored rectangle
            
        self.facing_right = True
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 3         
        self.jump_force = -18
        self.on_ground = False
        self.score = 0
        self.is_alive = True

        # --- VISIBILITY: Random Color for every AI Agent ---
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

        # --- BEHAVIORAL TRACKING FOR FITNESS FUNCTION ---
        self.coins_collected = 0
        self.max_height_reached = y          # Track highest point (lower y = higher)
        self.jumps_made = 0
        self.stuck_counter = 0
        self.death_count = 0
        self.frames_alive = 0
        self.reached_goal = False
        self.last_x_position = x             # For stuck detection

    def move(self, direction):
        """Sets horizontal velocity based on AI or Human input."""
        self.vel_x = direction * self.speed
        if direction > 0:
            self.facing_right = True
        elif direction < 0:
            self.facing_right = False

    def jump(self):
        """Triggers a jump if the player is currently on a platform."""
        if self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False
            self.jumps_made += 1

    def update(self, platforms):
        """Updates physics and handles collisions."""
        self.frames_alive += 1
        
        # Update max height (lower y = higher position)
        if self.rect.y < self.max_height_reached:
            self.max_height_reached = self.rect.y

        self.on_ground = False
        Physics.apply_gravity(self)
        
        # Horizontal Movement & Collision
        self.rect.x += self.vel_x
        self.handle_collisions(platforms, 'horizontal')
        
        # Vertical Movement & Collision
        self.rect.y += self.vel_y
        self.handle_collisions(platforms, 'vertical')

        # Stuck detection: if agent barely moved horizontally
        if abs(self.rect.x - self.last_x_position) < 2:
            self.stuck_counter += 1
        else:
            self.stuck_counter = max(0, self.stuck_counter - 5)  # Recover if moving
        
        self.last_x_position = self.rect.x

    def handle_collisions(self, platforms, direction):
        """Resolves overlaps between the player and world platforms."""
        for plat in platforms:
            if Physics.check_collision(self.rect, plat):
                if direction == 'horizontal':
                    if self.vel_x > 0:
                        self.rect.right = plat.left
                    elif self.vel_x < 0:
                        self.rect.left = plat.right
                elif direction == 'vertical':
                    if self.vel_y > 0:  # Falling
                        self.rect.bottom = plat.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:  # Hitting head
                        self.rect.top = plat.bottom
                        self.vel_y = 0

    def draw_scaled(self, surface, camera_x, camera_y, scale, is_best=False):
        """
        Enhanced Render Method for God View.
        Highlights the best agent and tints others with unique colors.
        """
        draw_x = (self.rect.x - camera_x) * scale
        draw_y = (self.rect.y - camera_y) * scale
        scaled_w = int(self.width * scale)
        scaled_h = int(self.height * scale)

        if self.image:
            img = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
            scaled_img = pygame.transform.scale(img, (scaled_w, scaled_h))
            
            if not is_best:
                color_overlay = pygame.Surface(scaled_img.get_size(), pygame.SRCALPHA)
                color_overlay.fill((*self.color, 140))
                scaled_img.blit(color_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            surface.blit(scaled_img, (draw_x, draw_y))
        else:
            color = (0, 255, 0) if is_best else self.color
            pygame.draw.rect(surface, color, (draw_x, draw_y, scaled_w, scaled_h))

    def draw(self, surface, camera_x, camera_y):
        """Standard draw for human mode."""
        self.draw_scaled(surface, camera_x, camera_y, 1.0, is_best=True)

    def reset_position(self, x, y):
        """Resets player state for new level or new generation."""
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.frames_alive = 0
        self.stuck_counter = 0
        self.last_x_position = x
        # Note: coins_collected, death_count, max_height_reached are reset by trainer when needed

    def die(self):
        """Mark agent as dead and increment death counter."""
        self.is_alive = False
        self.death_count += 1