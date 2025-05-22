import unittest
from snake_game import SnakeGame, Direction

class TestSnakeGame(unittest.TestCase):
    def setUp(self):
        self.game = SnakeGame(width=400, height=300, cell_size=20)
    
    def test_initial_state(self):
        """Test the initial game state"""
        self.assertEqual(self.game.direction, Direction.RIGHT)
        self.assertEqual(len(self.game.snake), 1)
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)
        
    def test_food_spawn(self):
        """Test that food spawns within bounds and not on snake"""
        food_x, food_y = self.game.food
        self.assertTrue(0 <= food_x < self.game.width)
        self.assertTrue(0 <= food_y < self.game.height)
        self.assertTrue(self.game.food not in self.game.snake)
        
    def test_movement_update(self):
        """Test basic movement mechanics"""
        initial_head = self.game.snake[0]
        self.game._update()
        new_head = self.game.snake[0]
        # Snake should move right by cell_size
        self.assertEqual(new_head[0], initial_head[0] + self.game.cell_size)
        self.assertEqual(new_head[1], initial_head[1])

if __name__ == '__main__':
    unittest.main()