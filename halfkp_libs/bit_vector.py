import torch

class BitVector:
    def __init__(self, size):
        self.size = size
        self.tensor_size, rest = divmod(size, 32)
        if rest > 1:
           self.tensor_size += 1
        self.bits = 0

    def set_bit(self, index):
        """Set the bit at the given index to 1."""
        if 0 <= index < self.size:
            self.bits |= 1 << index

    def clear_bit(self, index):
        """Set the bit at the given index to 0."""
        if 0 <= index < self.size:
            self.bits &= ~(1 << index)

    def get_bit(self, index):
        """Get the value of the bit at the given index."""
        if 0 <= index < self.size:
            return (self.bits >> index) & 1
        return None

    def get_range(self, start, end):
        """Return a part of the bit vector defined by start and end indices."""
        if 0 <= start <= end < self.size:
          vector = BitVector(end-start+1)
          for i in range( start, end + 1):
            if self.get_bit(i):
              vector.set_bit(i-start)
          return vector
        return None

    def to_int(self):
      if self.size > 32:
        return None
      result = 0
      for i in range(self.size):
        result = (result << 1) | self.get_bit(i)
      return result

    def to_tensor(self):
        """Convert the bit vector to a PyTorch tensor of 1280 int32 values."""
        # Create a tensor with 1280 elements, each representing a 32-bit integer
        tensor_values = [self.get_bit(i) for i in range(self.size)]
        return torch.tensor(tensor_values, dtype=torch.int8)

    def __str__(self):
        string = ""
        for i in range( self.size):
          string += str(self.get_bit(i))
        return string

    def get_non_zeros(self):
      result = []
      for i in range( self.size):
        if self.get_bit(i) == 1:
          result.append(i)
      return result
