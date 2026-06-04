import pygame

class Physics:
    """
    Handles global physical constants and collision detection 
    to ensure consistent and stable behavior across all agents.
    """
    GRAVITY = 0.85
    TERMINAL_VELOCITY = 12
    FRICTION = 0.18

    @staticmethod
    def apply_gravity(entity):
        """
        Applies gravity and terminal velocity limit.
        """
        entity.vel_y += Physics.GRAVITY
        
        if entity.vel_y > Physics.TERMINAL_VELOCITY:
            entity.vel_y = Physics.TERMINAL_VELOCITY

    @staticmethod
    def check_collision(rect1, rect2):
        """
        Checks if two pygame Rects are overlapping.
        """
        return rect1.colliderect(rect2)