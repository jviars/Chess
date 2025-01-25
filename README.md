# Chess AI Game

## About
This is a simple chess game with a built-in AI opponent. The game is implemented in Python using Pygame for the GUI and the python-chess library for chess logic. The AI uses a minimax algorithm with alpha-beta pruning to determine its moves. This project was created for fun by [jviars].

## Images
![image](https://github.com/user-attachments/assets/174f6939-0536-4444-9721-81e7a9cbaa7e)


## AI Model
The AI in this game uses the minimax algorithm with alpha-beta pruning to evaluate possible moves. The evaluation function considers the material value of the pieces on the board, with positive scores favoring white and negative scores favoring black. The AI searches to a fixed depth (default is 3) to balance play strength and response time.

## Packages
The game requires the following Python packages:
- `pygame`: For creating the graphical user interface.
- `python-chess`: For handling chess logic and move generation.

These dependencies are included in the text file labeled "requirements.txt".

## Installation
1. Download or clone the repository.
2. Navigate to the project directory.
3. Run the game - ensure you have the requirements installed (including Python itself).

The first time you run the game, it will automatically install the required dependencies from the `wheelhouse` folder.

## How to Play
- Use the mouse to select and move your pieces.
- The valid moves for the selected piece will be highlighted.
- The AI opponent will make its move after you.
- The game will display a message when it's checkmate or stalemate.

## Credits
This game was created for fun by [jviars]. Feel free to use, modify, and distribute it as you like.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- The chess piece images are from [Wikimedia Commons](https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces).
- The python-chess library is developed and maintained by [Niklas Fiekas](https://github.com/niklasf).
