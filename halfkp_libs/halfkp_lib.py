import chess
import torch
from halfkp_libs.chess_lib import Chess_Lib
from halfkp_libs.bit_vector import BitVector

class Half_KP_Converter:

  VECTOR_SIZE = 40960

  def __init__(self):
    self.white_bv = BitVector(self.VECTOR_SIZE)
    self.black_bv = BitVector(self.VECTOR_SIZE)

  def flip_square(self, square):
    offsets = [56, 40, 24, 8, -8, -24, -40, -56]
    return square + offsets[square // 8]

  def piece_index(self, type, color):
    return (type-1)*2 + color

  def halfkp_index(self, type, color, square, k_square):
    p_idx = self.piece_index(type, color)
    index = square + (p_idx + k_square * 10) * 64
    return index

  def board2tensor(self, chess_board:chess.Board):
    # Get the positions of the kings
    white_king_square = chess_board.king(chess.WHITE)
    black_king_square = self.flip_square(chess_board.king(chess.BLACK))
    self.white_bv.new_vector()
    self.black_bv.new_vector()
    for color in Chess_Lib.color_list:
      for piece in Chess_Lib.piece_list:
        for square in chess_board.pieces(piece, color):
          halfkp_index_w = self.halfkp_index(piece, color, square, white_king_square)
          halfkp_index_b = self.halfkp_index(piece, color, self.flip_square(square), black_king_square)
          self.white_bv.set_bit(halfkp_index_w)
          self.black_bv.set_bit(halfkp_index_b)
    if chess_board.turn == chess.WHITE:
      return torch.cat((self.white_bv.to_tensor(), self.black_bv.to_tensor()), dim = 0)
    else:
      return torch.cat((self.black_bv.to_tensor(), self.white_bv.to_tensor()), dim = 0)

  def fen2tensor(self, fen:str):
    chess_board = chess.Board()
    chess_board.set_fen(fen)
    return self.board2tensor(chess_board)
