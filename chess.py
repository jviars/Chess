# Basic Chess Game by jviars
# Chess piece models were sourced here: https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent

import chess
import pygame
import os
import time
from pathlib import Path


class ChessAI:
    def __init__(self, depth=3):
        self.depth = depth

        # Position weights for each piece type
        self.pawn_weights = [
            0, 0, 0, 0, 0, 0, 0, 0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5, 5, 10, 25, 25, 10, 5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, -5, -10, 0, 0, -10, -5, 5,
            5, 10, 10, -20, -20, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0
        ]

        self.knight_weights = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 0, 15, 20, 20, 15, 0, -30,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50
        ]

        self.bishop_weights = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 5, 5, 10, 10, 5, 5, -10,
            -10, 0, 10, 10, 10, 10, 0, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -20, -10, -10, -10, -10, -10, -10, -20
        ]

        self.rook_weights = [
            0, 0, 0, 0, 0, 0, 0, 0,
            5, 10, 10, 10, 10, 10, 10, 5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            0, 0, 0, 5, 5, 0, 0, 0
        ]

        self.queen_weights = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -5, 0, 5, 5, 5, 5, 0, -5,
            0, 0, 5, 5, 5, 5, 0, -5,
            -10, 5, 5, 5, 5, 5, 0, -10,
            -10, 0, 5, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20
        ]

        self.king_weights_middlegame = [
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            20, 20, 0, 0, 0, 0, 20, 20,
            20, 30, 10, 0, 0, 10, 30, 20
        ]

    def get_piece_position_score(self, piece, square, is_endgame):
        """Calculate position score for a piece"""
        if piece.piece_type == chess.PAWN:
            return self.pawn_weights[square if piece.color else 63 - square]
        elif piece.piece_type == chess.KNIGHT:
            return self.knight_weights[square if piece.color else 63 - square]
        elif piece.piece_type == chess.BISHOP:
            return self.bishop_weights[square if piece.color else 63 - square]
        elif piece.piece_type == chess.ROOK:
            return self.rook_weights[square if piece.color else 63 - square]
        elif piece.piece_type == chess.QUEEN:
            return self.queen_weights[square if piece.color else 63 - square]
        elif piece.piece_type == chess.KING:
            return self.king_weights_middlegame[square if piece.color else 63 - square]
        return 0

    def evaluate_board(self, board):
        """
        Evaluates the board position.
        Positive score favors white, negative favors black.
        """
        if board.is_checkmate():
            return -9999 if board.turn else 9999

        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        # Piece values
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }

        # Count material and position score
        score = 0
        material_count = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                material_count += piece_values[piece.piece_type]
                value = piece_values[piece.piece_type]
                # Add position score
                position_score = self.get_piece_position_score(
                    piece,
                    square,
                    material_count < 3000
                )

                if piece.color:
                    score += value + position_score * 0.1
                else:
                    score -= value + position_score * 0.1

        # Number of legal moves
        mobility = len(list(board.legal_moves))
        if board.turn:
            score += mobility * 0.1
        else:
            score -= mobility * 0.1

        # Penalties for specific positions
        if board.is_check():
            if board.turn:
                score -= 50  # White is in check
            else:
                score += 50  # Black is in check

        # Bonus for castling rights
        if board.has_castling_rights(chess.WHITE):
            score += 30
        if board.has_castling_rights(chess.BLACK):
            score -= 30

        # Bonus for developed pieces in early game
        if material_count > 5000:  # Early/middle game
            if board.piece_at(chess.E4) or board.piece_at(chess.D4):
                score += 10
            if board.piece_at(chess.E5) or board.piece_at(chess.D5):
                score -= 10

        return score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with alpha-beta pruning
        """
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in sorted(board.legal_moves, key=lambda m: self.move_value(board, m), reverse=True):
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in sorted(board.legal_moves, key=lambda m: self.move_value(board, m)):
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def move_value(self, board, move):
        """Rough estimate of move value for move ordering"""
        if board.is_capture(move):
            return 10
        elif board.gives_check(move):
            return 5
        elif move.from_square in [chess.E2, chess.D2, chess.E7, chess.D7]:  # Center pawns
            return 3
        elif move.to_square in [chess.E4, chess.D4, chess.E5, chess.D5]:  # Center control
            return 2
        return 0

    def get_best_move(self, board):
        """
        Finds the best move using minimax algorithm
        """
        best_move = None
        best_eval = float('-inf') if board.turn else float('inf')
        alpha = float('-inf')
        beta = float('inf')

        # Sort moves for better pruning
        moves = sorted(
            board.legal_moves,
            key=lambda m: self.move_value(board, m),
            reverse=board.turn
        )

        for move in moves:
            board.push(move)
            eval = self.minimax(board, self.depth - 1, alpha, beta, not board.turn)
            board.pop()

            if board.turn and eval > best_eval:
                best_eval = eval
                best_move = move
            elif not board.turn and eval < best_eval:
                best_eval = eval
                best_move = move

        return best_move or list(board.legal_moves)[0]


class ChessGUI:
    def __init__(self, width=800, height=900):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Chess Game")

        # Colors
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.YELLOW = (204, 204, 0)
        self.BLUE = (50, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Square dimensions
        self.BOARD_START_X = 50
        self.BOARD_START_Y = 50
        self.SQUARE_SIZE = 87.5

        # Load pieces
        self.pieces = {}
        self.load_pieces()

        # Game state
        self.board = chess.Board()
        self.ai = ChessAI()
        self.selected_square = None
        self.valid_moves = []
        self.move_made = False
        self.game_over = False
        self.player_color = True  # True for white, False for black

        # Animation variables
        self.animating = False
        self.animation_start = None
        self.animation_piece = None
        self.animation_start_pos = None
        self.animation_end_pos = None

        # Message display
        self.font = pygame.font.Font(None, 36)
        self.message = ""
        self.message_time = 0

    def load_pieces(self):
        """Load chess piece images"""
        pieces = ['p', 'n', 'b', 'r', 'q', 'k']
        for piece in pieces:
            # Load white pieces
            self.pieces[f'w{piece}'] = pygame.image.load(
                f'chess_pieces/w{piece}.png'
            )
            self.pieces[f'w{piece}'] = pygame.transform.scale(
                self.pieces[f'w{piece}'],
                (int(self.SQUARE_SIZE * 0.9), int(self.SQUARE_SIZE * 0.9))
            )
            # Load black pieces
            self.pieces[f'b{piece}'] = pygame.image.load(
                f'chess_pieces/b{piece}.png'
            )
            self.pieces[f'b{piece}'] = pygame.transform.scale(
                self.pieces[f'b{piece}'],
                (int(self.SQUARE_SIZE * 0.9), int(self.SQUARE_SIZE * 0.9))
            )

    def square_to_coordinates(self, pos):
        """Convert mouse position to board coordinates"""
        x, y = pos
        if (x < self.BOARD_START_X or x >= self.BOARD_START_X + 8 * self.SQUARE_SIZE or
                y < self.BOARD_START_Y or y >= self.BOARD_START_Y + 8 * self.SQUARE_SIZE):
            return None

        col = int((x - self.BOARD_START_X) // self.SQUARE_SIZE)
        row = int((y - self.BOARD_START_Y) // self.SQUARE_SIZE)
        return (7 - row) * 8 + col

    def draw_board(self):
        """Draw the chess board"""
        for row in range(8):
            for col in range(8):
                x = self.BOARD_START_X + col * self.SQUARE_SIZE
                y = self.BOARD_START_Y + row * self.SQUARE_SIZE
                color = self.WHITE if (row + col) % 2 == 0 else self.GRAY
                pygame.draw.rect(self.screen, color,
                                 (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))

                # Highlight selected square
                square = (7 - row) * 8 + col  # Convert to chess coordinates
                if self.selected_square and square == self.selected_square:
                    s = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
                    s.set_alpha(128)
                    s.fill(self.YELLOW)
                    self.screen.blit(s, (x, y))

                # Highlight valid moves
                if square in [move.to_square for move in self.valid_moves]:
                    s = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
                    s.set_alpha(128)
                    s.fill(self.BLUE)
                    self.screen.blit(s, (x, y))

    def draw_pieces(self):
        """Draw the chess pieces"""
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                x = self.BOARD_START_X + (square % 8) * self.SQUARE_SIZE
                y = self.BOARD_START_Y + (7 - square // 8) * self.SQUARE_SIZE

                # Don't draw the piece being animated
                if self.animating and square == self.animation_start_pos:
                    continue

                color = 'w' if piece.color else 'b'
                piece_type = piece.symbol().lower()
                self.screen.blit(self.pieces[f'{color}{piece_type}'],
                                 (x + self.SQUARE_SIZE * 0.05,
                                  y + self.SQUARE_SIZE * 0.05))

    def draw_status(self):
        """Draw game status and messages"""
        # Draw whose turn it is
        turn_text = "White's Turn" if self.board.turn else "Black's Turn"
        text_surface = self.font.render(turn_text, True, self.BLACK)
        self.screen.blit(text_surface, (self.width // 2 - 50, self.height - 100))

        # Draw any active message
        if time.time() - self.message_time < 3:  # Show message for 3 seconds
            text_surface = self.font.render(self.message, True, self.RED)
            self.screen.blit(text_surface, (self.width // 2 - 100, self.height - 50))

    def animate_move(self, start_pos, end_pos, piece):
        """Animate piece movement"""
        current_time = time.time()
        if self.animation_start is None:
            self.animation_start = current_time

        progress = (current_time - self.animation_start) / 0.3  # 0.3s animation

        if progress >= 1:
            self.animating = False
            return

        start_x = self.BOARD_START_X + (start_pos % 8) * self.SQUARE_SIZE
        start_y = self.BOARD_START_Y + (7 - start_pos // 8) * self.SQUARE_SIZE
        end_x = self.BOARD_START_X + (end_pos % 8) * self.SQUARE_SIZE
        end_y = self.BOARD_START_Y + (7 - end_pos // 8) * self.SQUARE_SIZE

        current_x = start_x + (end_x - start_x) * progress
        current_y = start_y + (end_y - start_y) * progress

        color = 'w' if piece.color else 'b'
        piece_type = piece.symbol().lower()
        self.screen.blit(self.pieces[f'{color}{piece_type}'],
                         (current_x + self.SQUARE_SIZE * 0.05,
                          current_y + self.SQUARE_SIZE * 0.05))

    def handle_click(self, pos):
        """Handle mouse click events"""
        square = self.square_to_coordinates(pos)
        if square is None:
            return

        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                # Get valid moves for the selected piece
                self.valid_moves = [
                    move for move in self.board.legal_moves
                    if move.from_square == square
                ]
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.valid_moves:
                # Start animation
                self.animating = True
                self.animation_start = None
                self.animation_piece = self.board.piece_at(self.selected_square)
                self.animation_start_pos = self.selected_square
                self.animation_end_pos = square

                # Make the move
                self.board.push(move)
                self.move_made = True

            self.selected_square = None
            self.valid_moves = []

    def display_message(self, msg):
        """Display a message on screen"""
        self.message = msg
        self.message_time = time.time()

    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.animating:
                    if self.board.turn == self.player_color and not self.game_over:
                        self.handle_click(event.pos)

            # Draw everything
            self.screen.fill(self.WHITE)
            self.draw_board()
            self.draw_pieces()

            # This animates
            if self.animating:
                self.animate_move(self.animation_start_pos,
                                  self.animation_end_pos,
                                  self.animation_piece)

            # AI move
            if (not self.board.turn == self.player_color and
                    not self.game_over and
                    not self.animating and
                    self.move_made):
                self.display_message("AI is thinking...")
                pygame.display.flip()

                # Get AI move
                ai_move = self.ai.get_best_move(self.board)

                # Start animation
                self.animating = True
                self.animation_start = None
                self.animation_piece = self.board.piece_at(ai_move.from_square)
                self.animation_start_pos = ai_move.from_square
                self.animation_end_pos = ai_move.to_square

                # Make the move
                self.board.push(ai_move)
                self.move_made = False

            # Check game state
            if self.board.is_checkmate():
                self.game_over = True
                winner = "White" if not self.board.turn else "Black"
                self.display_message(f"Checkmate! {winner} wins!")
            elif self.board.is_stalemate():
                self.game_over = True
                self.display_message("Stalemate!")

            self.draw_status()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


def main():
    game = ChessGUI()
    game.run()


if __name__ == "__main__":
    main()
