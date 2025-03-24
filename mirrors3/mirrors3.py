from dataclasses import dataclass
from enum import auto, Enum
from typing import Union

from .utils import get_prime_factors, get_prime_factor_combinations, get_combination_permutations

###
### OK Let's first solve the problem and then make it beautiful
###

# a dataclass would provide for free __init__ and __repr__
# that's good enough for us in this example
# I don't think we want our dataclass to be frozen as we're gonna change the values
@dataclass
class Laser:
  value:int=None
  
class MirrorDirection(Enum):
  SLASH = auto() # /
  BACKSLASH = auto() # \
  
class Mirror:
  def __init__(self, direction:MirrorDirection):
    self.direction = direction

  def __repr__(self):
    return f"<Mirror direction={self.direction}>"

# can we also make this a dataclass?? and then override the __repr__??? we should try at least
class Cell:
  def __init__(self, value:Union[Laser, Mirror]=None, coordinate=None):
    self.value = value
    self.coordinate = coordinate
    self.is_solid_path = False # this will tell us whether to quit our search early or not

    # I really wonder whether this should be here??
    self.is_laser = lambda: self.value is not None and isinstance(self.value, Laser)

    #if isinstance(value, str) and value not in ["/" "\\"]:
      

  def __repr__(self):
    return f"<Cell value={self.value} is_laser={self.is_laser()}>"



if __name__ == "__main__":
  # what I'd like is something like Cell("/") which maps to Mirror.direction = MirrorDirection.SLASH
  m = 7
  n = 7
  max_m = m - 2
  max_n = n - 2
  # m * n, i.e. 7x7
  matrix = [
    [None, Cell(Laser()), Cell(Laser()), Cell(Laser(9)), Cell(Laser()), Cell(Laser()), None], 
    [Cell(Laser()), Cell(), Cell(), Cell(), Cell(), Cell(), Cell(Laser())], 
    [Cell(Laser()), Cell(), Cell(), Cell(), Cell(), Cell(), Cell(Laser(75))],
    [Cell(Laser()), Cell(), Cell(), Cell(), Cell(), Cell(), Cell(Laser())],
    [Cell(Laser(16)), Cell(), Cell(), Cell(), Cell(), Cell(), Cell(Laser())],
    [Cell(Laser()), Cell(), Cell(), Cell(), Cell(), Cell(), Cell(Laser())],
    [None, Cell(Laser()), Cell(Laser()), Cell(Laser(36)), Cell(Laser()), Cell(Laser()), None],
  ]
  # TODO have a nice visualization of the matrix

  # instead of starting from the highest we start from the left to right from the first row
  # first pass is to get the mirrors set up from the lasers that already have a value
  for i, row in enumerate(matrix):
    for j, column in enumerate(row):
      print(f"this is column with index {i, j} with value {matrix[i][j]}")
      cell = matrix[i][j]
      if cell is not None and cell.is_laser() and cell.value.value is not None:
        # get the prime factors e the cell value into possible combinations of products and for each check whether we can reach a laser boundary
        # from the prime factors, generate the combinations
        # for each combination, generate the permutations
        prime_factors = get_prime_factors(cell.value.value)
        print(f"prime_factors of {cell.value.value} are {prime_factors}")
        prime_factors_combinations = get_prime_factor_combinations(prime_factors)
        print(f"prime factors combs/compactions are {sorted(prime_factors_combinations)}")
        for combination in prime_factors_combinations:
          combination_permutations = get_combination_permutations(combination)
          print(f"combination/compactions={combination} has these permutations {combination_permutations}")
          # TODO all this
          # util funtion to check whether the path is a solid one or not, or more in general to check if we get to the solution or not
          #reachable_row = i + y
          #reachable_column = j + x
          ## first check is to check whether we are going outbound with this permutation (is it permutation or combination??)
          #if reachable_row > m or reachable_column > n: continue 
          #elif reachable_row and

  # second pass is to calculate the perimeter














































































































