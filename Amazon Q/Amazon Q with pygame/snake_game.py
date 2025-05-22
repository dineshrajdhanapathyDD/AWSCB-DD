import pygame
import random
import os
from typing import List, Tuple
from enum import Enum, auto

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class SnakeGame:
    def __init__(self, width: int = 800, height: int = 600, cell_size: int = 20):
        pygame.init()
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake Game")
        
        # Initialize fonts for scoreboard
        self.font = pygame.font.SysFont('arial', 25, True)
        
        # Initialize game state
        self.direction = Direction.RIGHT
        self.snake = [(width // 2, height // 2)]
        self.food = self._spawn_food()
        self.score = 0
        self.high_score = self._load_high_score()
        self.clock = pygame.time.Clock()
        self.game_over = False
        
    def _load_high_score(self) -> int:
        """Load the high score from a file, or return 0 if the file doesn't exist."""
        try:
            if os.path.exists('snake_high_score.txt'):
                with open('snake_high_score.txt', 'r') as f:
                    return int(f.read().strip())
        except:
            pass
        return 0
        
    def _save_high_score(self) -> None:
        """Save the current high score to a file."""
        with open('snake_high_score.txt', 'w') as f:
            f.write(str(self.high_score))

    def _spawn_food(self) -> Tuple[int, int]:
        while True:
            x = random.randrange(0, self.width, self.cell_size)
            # Ensure food doesn't spawn in the scoreboard area
            y = random.randrange(40, self.height, self.cell_size)
            if (x, y) not in self.snake:
                return (x, y)

    def _handle_input(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
        return True

    def _update(self) -> None:
        head_x, head_y = self.snake[0]
        
        if self.direction == Direction.UP:
            new_head = (head_x, head_y - self.cell_size)
        elif self.direction == Direction.DOWN:
            new_head = (head_x, head_y + self.cell_size)
        elif self.direction == Direction.LEFT:
            new_head = (head_x - self.cell_size, head_y)
        else:  # Direction.RIGHT
            new_head = (head_x + self.cell_size, head_y)

        # Check for collisions
        if (new_head in self.snake or 
            new_head[0] < 0 or new_head[0] >= self.width or 
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            # Update high score if needed before game ends
            if self.score > self.high_score:
                self.high_score = self.score
                self._save_high_score()
            return

        self.snake.insert(0, new_head)
        
        # Check if food was eaten
        if new_head == self.food:
            self.score += 1
            # Update high score if needed
            if self.score > self.high_score:
                self.high_score = self.score
                self._save_high_score()
            self.food = self._spawn_food()
        else:
            self.snake.pop()

    def _draw(self) -> None:
        self.screen.fill((0, 0, 0))
        
        # Draw scoreboard background
        pygame.draw.rect(self.screen, (50, 50, 50), (0, 0, self.width, 40))
        
        # Draw current score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        # Draw high score
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, (255, 215, 0))  # Gold color
        self.screen.blit(high_score_text, (self.width - high_score_text.get_width() - 10, 10))
        
        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(self.screen, (0, 255, 0),
                           (segment[0], segment[1], self.cell_size - 1, self.cell_size - 1))
        
        # Draw food
        pygame.draw.rect(self.screen, (255, 0, 0),
                        (self.food[0], self.food[1], self.cell_size - 1, self.cell_size - 1))
        
        pygame.display.flip()

    def run(self) -> None:
        while not self.game_over:
            if not self._handle_input():
                # Save high score before quitting
                if self.score > self.high_score:
                    self.high_score = self.score
                    self._save_high_score()
                break
                
            self._update()
            self._draw()
            self.clock.tick(5)  # Control game speed (reduced for beginners)

        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()