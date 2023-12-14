from libs.chess_lib import Chess_Lib
import torch
import torch.nn.init as init

class NNUE(nn.Module):
    def __init__(self, NUM_FEATURES = 40960, M = 256, N = 32, K = 32):
        super(NNUE, self).__init__()

        self.ft = nn.Linear(NUM_FEATURES, M)
        self.l1 = nn.Linear(2 * M, N)
        self.l2 = nn.Linear(N, K)
        # ChatGPT
        self.l3 = nn.Linear(K, 1)  # New linear layer to reduce from K to 1

        # Initialize the weights
        self.init_weights()

    def init_weights(self):
        for layer in [self.ft, self.l1, self.l2, self.l3]:
            if hasattr(layer, 'weight'):
                init.xavier_uniform_(layer.weight)

    def align_eval(self, eval):
      eval = (eval - 0.5) * 2 * Chess_Lib.MAX_EVAL
      return int(eval)

    # The inputs are a whole batch!
    # `stm` indicates the whether white is the side to move. 1 = true, 0 = false.
    def forward(self, white_features, black_features, stm):
        w = self.ft(white_features) # white's perspective
        b = self.ft(black_features) # black's perspective

        # Remember that we order the accumulators for 2 perspectives based on who is to move.
        # So we blend two possible orderings by interpolating between `stm` and `1-stm` tensors.
        accumulator = (stm * torch.cat([w, b], dim=1)) + ((1 - stm) * torch.cat([b, w], dim=1))

        # Run the linear layers and use clamp_ as ClippedReLU
        l1_x = torch.clamp(accumulator, 0.0, 1.0)
        l2_x = torch.clamp(self.l1(l1_x), 0.0, 1.0)
        # ChatGPT
        l3_x = torch.clamp(self.l2(l2_x), 0.0, 1.0)  # Output from the new layer
        eval = torch.clamp(self.l3(l3_x), 0.0, 1.0)
        return self.align_eval(eval)