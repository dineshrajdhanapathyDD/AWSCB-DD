# Snake Game

A classic Snake game implementation using Pygame.

## Description

This is a modern implementation of the classic Snake game where you control a snake that grows longer as it eats food. The game ends if the snake collides with itself.

## Features

- Smooth snake movement with arrow keys or WASD controls
- Score tracking
- Start and Game Over screens
- Grid-based gameplay
- Randomly spawning food
- Collision detection

## Requirements

- Python 3.6 or higher
- Pygame






### Step-by-Step Setup to Run the Snake Game with Pygame on Linux

1.  **Check Available Files**  
    - Use `ls` to verify the presence of your game files (e.g., `snake_game.py`).
    
    `ls` 
    
2.  **Ensure `python` Points to Python 3**  
    - Install `python-is-python3` to map the `python` command to Python 3.x.
    
       
    `sudo apt install python-is-python3` 
    
3.  **Verify Python Version**  
    - Check that Python 3.12.3 (or similar) is properly installed.

    
    `python --version # Output: Python 3.12.3` 
    
4.  **Install pipx (Optional but Useful)**  
    - You can use `pipx` to manage isolated Python package installations.
    
        
    `sudo apt install pipx` 
    
5.  **Install Pygame (with system override)**  
    - Installing `pygame` directly might raise a warning about an externally managed environment. Use the `--break-system-packages` flag to proceed:

    
    `sudo pip install pygame --break-system-packages` 
        
    ```
    > ✅ Successfully installed `pygame-2.6.1`
    ```
6.  **Run the Game**  
    - Launch the Snake game using:
    
   
    `python snake_game.py` 
    
- You should see output like:

    
    ```
    pygame 2.6.1 (SDL 2.28.4, Python 3.12.3)
    Hello from the pygame community. https://www.pygame.org/contribute.html
    ```




7. Press SPACE to start the game.
8. Use the arrow keys or WASD to control the snake's direction.
9. Eat the red food to grow the snake and increase your score.
10. Avoid colliding with yourself.
11. When the game is over, press SPACE to restart.

## Controls

- Arrow Keys or WASD: Control the snake's direction
- SPACE: Start game / Restart after game over

## Future Improvements

- Increasing difficulty as the score increases
- Sound effects
- Different types of food with varying point values
- Obstacles or walls
- High score system
- Different themes or skins
- Power-ups
- Pause feature
- Smooth animations
- Multiplayer mode

## License

This project is open source and available under the MIT License.
