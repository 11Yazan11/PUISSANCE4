import pygame
import math

class Bixel:
    def __init__(self, main, x, y, color, col, grid_position):
        """Color is a tuple or list or rgb value only."""
        self.size = (400/7,444/7+4)
        self.game = main
        self.color = color
        self.COL = col
        self.gravity = 9.81 / self.game.fps
        self.grounded = False
        self.velocity_y = 0  # Current vertical velocity
        self.air_resistance = 0.007  # Air resistance (drag)
        self.elasticity = 0.4  # Coefficient of restitution (bounciness)
        self.rect = pygame.Rect(x, y, self.size[0], self.size[1])
        self.ground_level = 500-math.floor(self.size[1])
        self.grid_position = grid_position

    def get_ground_level(self):
        """Find the nearest object below the player in the same column."""
        nearest = None
        for bixel in reversed(self.game.jetons):
            # Check if the `bixel` is in the same column
            if bixel.rect.x == self.rect.x:
                # Check if the `bixel` is directly below
                if bixel.rect.y >= self.rect.y + self.rect.h:
                    # Find the closest `bixel` below
                    if nearest is None or bixel.rect.y < nearest.rect.y:
                        nearest = bixel
    
        # Set the ground level based on the nearest `bixel`
        if nearest:
            self.ground_level = nearest.rect.y - nearest.rect.h
        else:
            self.ground_level = 500 - math.floor(self.size[1])

    def update(self):
        pygame.draw.rect(self.game.window, self.color, self.rect)
        pygame.draw.rect(self.game.window, self.darken_color(self.color), self.rect, 4)
        pygame.draw.rect(self.game.window, self.brigthen_color(self.color), self.rect, 2)
        if self.rect.y >= self.ground_level:
            self.velocity_y = -self.velocity_y * self.elasticity  # Bounce back with reduced energy
            self.rect.y = self.ground_level
            # Stop tiny oscillations when nearly at rest
            if abs(self.velocity_y) < 0.5:
                self.velocity_y = 0
                self.grounded = True
        elif not self.grounded:
            self.get_ground_level()
            self.velocity_y += self.gravity
            self.velocity_y -= self.air_resistance * self.velocity_y * abs(self.velocity_y)
            self.grounded = False

        self.rect.y += self.velocity_y

    def brigthen_color(self, color):
        """Brightens the given RGB color by increasing its values, clamped to a maximum of 255."""
        if not isinstance(color, (tuple, list)) or len(color) != 3:
            raise ValueError("Color must be a tuple or list with three elements representing RGB values.")
    
        # Increase each component by a fixed value, clamped to a maximum of 255
        brightened_color = tuple(min(c + 50, 255) for c in color)
        return brightened_color
    
    def darken_color(self, color):
        """Darkens the given RGB color by increasing its values, clamped to a minimum of 0."""
        if not isinstance(color, (tuple, list)) or len(color) != 3:
            raise ValueError("Color must be a tuple or list with three elements representing RGB values.")
    
        # Decrease each component by a fixed value, clamped to a minimum of 0
        darkened_color = tuple(max(c - 50, 0) for c in color)
        return darkened_color

    def handle_event(self, event):
        pass

    def destroy(self):
        if self in self.game.jetons:
            self.game.jetons.remove(self)