import chess

class Chess_Lib:
  piece_list = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]
  color_list = [chess.WHITE, chess.BLACK]

  MAX_EVAL = (1000 * 2 + 100 * 1000)

  def get_eval_value(centi_pawn, mate_in):
    if mate_in == 0:
      return int(centi_pawn*100)
    if mate_in < 0:
      sign = -1
      mate_in = mate_in * sign
    else:
      sign = 1
    mate_in = min(mate_in, 99)
    mate_value = sign * (Chess_Lib.MAX_EVAL - mate_in * 1000)
    return mate_value