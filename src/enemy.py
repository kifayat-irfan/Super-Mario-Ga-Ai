import pygame
from src.physics import Physics

class Enemy:
    """
    The Enemy class handles patrolling enemies (Goombas).
    Enhanced for stable collisions and consistent behavior during AI training.
    """
    def __init__(self, x, y, patrol_distance=120):
        self.width = 32
        self.height = 32
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Image loading with fallback
        try:
            self.image = pygame.image.load("assets/enemy.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except:
            self.image = None
            
        self.start_x = x
        self.patrol_distance = patrol_distance
        self.speed = 2.2
        self.direction = 1
        self.vel_y = 0

    def update(self, platforms):
        """Update enemy movement with gravity and collisions."""
        # Apply gravity
        Physics.apply_gravity(self)
        
        # Horizontal movement
        self.rect.x += self.speed * self.direction
        
        # Patrol boundary check
        if self.rect.x > self.start_x + self.patrol_distance or self.rect.x < self.start_x - self.patrol_distance:
            self.direction *= -1
        
        # Collision with platforms (horizontal)
        for plat in platforms:
            if Physics.check_collision(self.rect, plat):
                # Push back and flip direction
                if self.direction > 0:
                    self.rect.right = plat.left
                else:
                    self.rect.left = plat.right
                self.direction *= -1
                break

        # Vertical movement & floor collision
        self.rect.y += self.vel_y
        for plat in platforms:
            if Physics.check_collision(self.rect, plat):
                if self.vel_y > 0:  # Falling
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                elif self.vel_y < 0:  # Hitting ceiling
                    self.rect.top = plat.bottom
                    self.vel_y = 0

    def draw_scaled(self, surface, camera_x, camera_y, scale):
        """
        Renders the enemy with proper scaling for God View.
        """
        draw_x = (self.rect.x - camera_x) * scale
        draw_y = (self.rect.y - camera_y) * scale
        scaled_w = int(self.width * scale)
        scaled_h = int(self.height * scale)

        if self.image:
            # Flip based on movement direction
            img = self.image if self.direction > 0 else pygame.transform.flip(self.image, True, False)
            scaled_img = pygame.transform.scale(img, (scaled_w, scaled_h))
            surface.blit(scaled_img, (draw_x, draw_y))
        else:
            # Fallback rectangle
            pygame.draw.rect(surface, (220, 20, 20), (draw_x, draw_y, scaled_w, scaled_h))