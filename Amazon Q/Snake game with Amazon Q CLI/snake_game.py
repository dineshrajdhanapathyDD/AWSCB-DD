#!/usr/bin/env python3
"""
Snake Game - A classic Snake game implementation using Pygame
"""
import pygame
import sys
import random
import time
from enum import Enum

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SNAKE_SPEED = 10  # Frames per second

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 100, 0)
GRAY = (100, 100, 100)

# Fonts
FONT_LARGE = pygame.font.SysFont('arial', 50, True)
FONT_MEDIUM = pygame.font.SysFont('arial', 30, True)
FONT_SMALL = pygame.font.SysFont('arial', 20)


class Direction(Enum):
    """Enum for snake direction"""
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


class Snake:
    """
    Snake class representing the player-controlled snake
    """
    def __init__(self):
        """Initialize the snake with default position and direction"""
        self.reset()
    
    def reset(self):
        """Reset snake to starting position and state"""
        # Start with a snake of length 3 in the middle of the screen
        self.length = 3
        self.positions = [
            ((GRID_WIDTH // 2), (GRID_HEIGHT // 2)),
            ((GRID_WIDTH // 2) - 1, (GRID_HEIGHT // 2)),
            ((GRID_WIDTH // 2) - 2, (GRID_HEIGHT // 2))
        ]
        self.direction = Direction.RIGHT
        self.last_direction = self.direction
        self.score = 0
    
    def get_head_position(self):
        """Return the position of the snake's head"""
        return self.positions[0]
    
    def update(self):
        """Update snake position based on current direction"""
        # Only update direction if it's not opposite to the last direction
        if self.direction != self.get_opposite_direction(self.last_direction):
            self.last_direction = self.direction
        else:
            self.direction = self.last_direction
        
        # Calculate new head position
        current_head = self.get_head_position()
        direction_vector = self.direction.value
        new_head = (
            (current_head[0] + direction_vector[0]) % GRID_WIDTH,
            (current_head[1] + direction_vector[1]) % GRID_HEIGHT
        )
        
        # Check for collision with self
        if new_head in self.positions[:-1]:
            return True  # Collision detected
        
        # Add new head to positions
        self.positions.insert(0, new_head)
        
        # Remove tail if snake hasn't grown
        if len(self.positions) > self.length:
            self.positions.pop()
            
        return False  # No collision
    
    def get_opposite_direction(self, direction):
        """Return the opposite direction"""
        if direction == Direction.RIGHT:
            return Direction.LEFT
        elif direction == Direction.LEFT:
            return Direction.RIGHT
        elif direction == Direction.UP:
            return Direction.DOWN
        elif direction == Direction.DOWN:
            return Direction.UP
    
    def grow(self):
        """Increase snake length"""
        self.length += 1
        self.score += 10
    
    def render(self, surface):
        """Draw the snake on the given surface"""
        for i, pos in enumerate(self.positions):
            # Draw snake body
            rect = pygame.Rect(
                pos[0] * GRID_SIZE,
                pos[1] * GRID_SIZE,
                GRID_SIZE, GRID_SIZE
            )
            
            # Head is a different color
            if i == 0:
                pygame.draw.rect(surface, GREEN, rect)
                pygame.draw.rect(surface, BLACK, rect, 1)  # Border
            else:
                pygame.draw.rect(surface, DARK_GREEN, rect)
                pygame.draw.rect(surface, BLACK, rect, 1)  # Border


class Food:
    """
    Food class representing the items the snake can eat
    """
    def __init__(self):
        """Initialize food with random position"""
        self.position = (0, 0)
        self.randomize_position()
    
    def randomize_position(self):
        """Place food at a random position on the grid"""
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )
    
    def render(self, surface):
        """Draw the food on the given surface"""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)  # Border


class Game:
    """
    Main game class handling the game loop, events, and rendering
    """
    def __init__(self):
        """Initialize the game"""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.state = "START"  # START, PLAYING, GAME_OVER
        self.last_update_time = 0
        self.update_interval = 1000 // SNAKE_SPEED  # milliseconds
    
    def handle_events(self):
        """Process user input and events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.state == "START":
                    if event.key == pygame.K_SPACE:
                        self.state = "PLAYING"
                
                elif self.state == "GAME_OVER":
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                
                elif self.state == "PLAYING":
                    # Arrow keys for direction
                    if event.key == pygame.K_RIGHT and self.snake.direction != Direction.LEFT:
                        self.snake.direction = Direction.RIGHT
                    elif event.key == pygame.K_LEFT and self.snake.direction != Direction.RIGHT:
                        self.snake.direction = Direction.LEFT
                    elif event.key == pygame.K_UP and self.snake.direction != Direction.DOWN:
                        self.snake.direction = Direction.UP
                    elif event.key == pygame.K_DOWN and self.snake.direction != Direction.UP:
                        self.snake.direction = Direction.DOWN
                    
                    # WASD keys for direction (alternative)
                    elif event.key == pygame.K_d and self.snake.direction != Direction.LEFT:
                        self.snake.direction = Direction.RIGHT
                    elif event.key == pygame.K_a and self.snake.direction != Direction.RIGHT:
                        self.snake.direction = Direction.LEFT
                    elif event.key == pygame.K_w and self.snake.direction != Direction.DOWN:
                        self.snake.direction = Direction.UP
                    elif event.key == pygame.K_s and self.snake.direction != Direction.UP:
                        self.snake.direction = Direction.DOWN
    
    def update(self):
        """Update game state"""
        if self.state != "PLAYING":
            return
        
        # Check if it's time to update
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time < self.update_interval:
            return
        
        self.last_update_time = current_time
        
        # Update snake position and check for collision
        collision = self.snake.update()
        if collision:
            self.state = "GAME_OVER"
            return
        
        # Check if snake ate food
        if self.snake.get_head_position() == self.food.position:
            self.snake.grow()
            
            # Place new food, ensuring it's not on the snake
            while True:
                self.food.randomize_position()
                if self.food.position not in self.snake.positions:
                    break
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.snake.reset()
        self.food.randomize_position()
        self.state = "PLAYING"
    
    def render_grid(self):
        """Draw the background grid"""
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y))
    
    def render_start_screen(self):
        """Draw the start screen"""
        self.screen.fill(BLACK)
        
        title = FONT_LARGE.render("SNAKE GAME", True, GREEN)
        instructions = FONT_MEDIUM.render("Press SPACE to Start", True, WHITE)
        controls = FONT_SMALL.render("Use Arrow Keys or WASD to move", True, WHITE)
        
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        self.screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 300))
        self.screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, 350))
    
    def render_game_over_screen(self):
        """Draw the game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over = FONT_LARGE.render("GAME OVER", True, RED)
        score = FONT_MEDIUM.render(f"Score: {self.snake.score}", True, WHITE)
        restart = FONT_MEDIUM.render("Press SPACE to Restart", True, WHITE)
        
        self.screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2, 200))
        self.screen.blit(score, (SCREEN_WIDTH // 2 - score.get_width() // 2, 280))
        self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 350))
    
    def render_score(self):
        """Draw the current score"""
        score_text = FONT_SMALL.render(f"Score: {self.snake.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
    
    def render(self):
        """Draw the game state to the screen"""
        if self.state == "START":
            self.render_start_screen()
        
        elif self.state == "PLAYING":
            self.screen.fill(BLACK)
            self.render_grid()
            self.food.render(self.screen)
            self.snake.render(self.screen)
            self.render_score()
        
        elif self.state == "GAME_OVER":
            self.render_game_over_screen()
        
        pygame.display.update()
    
    def run(self):
        """Main game loop"""
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # Cap at 60 FPS


if __name__ == "__main__":
    game = Game()
    game.run()

# Potential improvements:
# 1. Increasing difficulty: Make the snake move faster as the score increases
# 2. Add sound effects for eating food, game over, etc.
# 3. Add different types of food with different point values
# 4. Add obstacles or walls that the snake must avoid
# 5. Implement a high score system using local file storage
# 6. Add different themes or skins for the snake and background
# 7. Add power-ups that temporarily change game mechanics (e.g., slow down, invincibility)
# 8. Add a pause feature
# 9. Implement smooth animations for snake movement
# 10. Add a multiplayer mode
