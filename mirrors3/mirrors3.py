from collections import defaultdict
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

class Coordinate:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __add__(self, other):
    assert isinstance(other, Coordinate), f"cannot add coordinates to class {type(other)}"
    return Coordinate(self.x + other.x, self.y + other.y)

  def __neg__(self): # -(x, y) = (-x, -y)
    return self * -1

  def __sub__(self, other):
    assert isinstance(other, Coordinate), f"cannot sub coordinates of class {type(other)}"
    return self + (-other)

  def __mul__(self, other):
    assert isinstance(other, int), f"can only multiply the coordinate by a scalar value"
    return Coordinate(self.x * other, self.y * other)
  
  def __rmul__(self, other): # other * self
    return self * other

  def __repr__(self):
    return f"<Coordinate x={self.x}, y={self.y}>"

class Node:
  def __init__(self, coordinate:Coordinate, mirror:Mirror, next_node, previous_node):
    self.coordinate = coordinate
    self.mirror = mirror
    self.next = next_node
    self.prev = previous_node

class Cell:
  def __init__(self, value:Union[Laser, Mirror]=None, coordinate:Coordinate=None):
    self.value = value
    self.coordinate = coordinate
    self.is_solid_path = False # this will tell us whether to quit our search early or not

    self.is_laser = lambda: self.value is not None and isinstance(self.value, Laser) == True

  def get_next_direction_from_mirror(self, previous_cell_coordinates:Coordinate):
    assert isinstance(self.value, Mirror), f"this cell value is not a Mirror {self}"
    assert isinstance(previous_cell_coordinates, Coordinate), f"the argument previous_cell_coordinates is not a Coordinate class, {type(previous_cell_coordinates)}"
    #print(f"get_next_direction_from_mirror: current_coordinates={self.coordinate} previous_cell_coordinates={previous_cell_coordinates}")
    # TODO make this more beautiful
    coord_diff = self.coordinate - previous_cell_coordinates
    if coord_diff.x == 0:
      if coord_diff.y > 0: coming_from = "left"
      else: coming_from = "right"
    elif coord_diff.x > 0: coming_from = "up"
    else: coming_from = "down"

    match self.value.direction:
      case MirrorDirection.SLASH:
        #print(f"matched case SLASH")
        if coming_from == "up": return Coordinate(0, -1) # you can go left in this condition
        if coming_from == "down": return Coordinate(0, 1) # go right
        if coming_from == "left": return Coordinate(-1, 0) # go up
        if coming_from == "right": return Coordinate(1, 0) # go down
      case MirrorDirection.BACKSLASH:
        #print(f"matched case BACKSLASH")
        if coming_from == "up": return Coordinate(0, 1) # you can go right
        if coming_from == "down": return Coordinate(0, -1) # go left
        if coming_from == "left": return Coordinate(1, 0) # go down
        if coming_from == "right": return Coordinate(-1, 0) # go up

    pass
      

  def __repr__(self):
    return f"<Cell value={self.value} coordinate={self.coordinate} is_laser={self.is_laser()}>"

# make_step will need to create the graph/tree of the possible solution
def make_step(matrix, current_node_soln_path:dict, from_cell:Cell, going_towards_direction:Coordinate, perm:tuple, stepi:int, mirror_direction:MirrorDirection) -> None: # TODO maybe change the return type to bool
  print(f"make_step: from_cell={from_cell} going_towards_direction={going_towards_direction} perm={perm} stepi={stepi} mirror_direction={mirror_direction}")
  if stepi > len(perm) - 1:
    print(f"make_step: solution not found because stuck in the middle {current_node_soln_path}")
    return False # I think this should handle the case where we've ran out of steps of the permutations and haven't found the solution yet, yeah it seems to do that

  step_magnitude = going_towards_direction * perm[stepi]
  new_pos:Coordinate = from_cell.coordinate + step_magnitude
  is_new_pos_inside = check_inside_bound(new_pos)
  if not is_new_pos_inside:
    print(f"make_step: solution not found because oob {perm} stepi={stepi}, {current_node_soln_path}")
    return False
  # this is "make the step" and you end up in the new cell position
  current_cell:Cell = matrix[new_pos.x][new_pos.y]
  current_cell.value = Mirror(MirrorDirection.SLASH) if current_cell.is_laser() == False else current_cell.value # we don't want to override the laser cells

  if current_cell.is_laser() and current_cell.value.value is not None:
    print(f"make_step: solution not found as the current_cell is a laser with predefined value")
    return False
  # TODO do not hardcode these, get them from the global defined constants instead
  # in both cases below we don't need to handle the scenario of oob as the `check_inside_bound` will handle that
  if current_cell.coordinate.y == 0 or current_cell.coordinate.y == 6 and current_cell.is_laser() and current_cell.value.value is None:
    if stepi + 1 == len(perm): print(f"make_step: solution_found {perm} {current_node_soln_path}"); return True
  if current_cell.coordinate.x == 0 or current_cell.coordinate.x == 6 and current_cell.is_laser() and current_cell.value is None:
    if stepi + 1 == len(perm): print(f"make_step: solution found {perm} {current_node_soln_path}"); return True


  if stepi < len(perm) and current_cell.is_laser() == False:
    next_step_direction = current_cell.get_next_direction_from_mirror(from_cell.coordinate) # instead of passing in the string values saying where we're coming from we should calculate the coming from based on the current cell and the previous cell coordinates
  else:
    # TODO this seems to work but the soln_graph is wrong
    # we need to create the graph better
    #current_node_soln_path[from_cell].append(current_cell)
    print(f"make_step: no solution found: we seem to be at the laser and there are still steps to make, perm={perm} stepi={stepi} {current_node_soln_path}")
    return False
  current_node_soln_path[from_cell].append(current_cell)

  # TODO find better name, this is really bad
  path_result_1 = make_step(matrix, current_node_soln_path, current_cell, next_step_direction, perm, stepi+1, current_cell.value.direction) # placed /

  # NOTE: To mark the path as a solid solution, we need to find only one path in the entire combination and then make that
  # path as solid, if not we need to make the other ones as possible solutions. We kind of need to create the tree and then find
  # all possible solutions or unique solution.

  # place an hypotethical \ and go explore that path
  current_cell.value = Mirror(MirrorDirection.BACKSLASH)
  next_step_direction = current_cell.get_next_direction_from_mirror(from_cell.coordinate)
  # TODO find better name
  path_result_2 = make_step(matrix, current_node_soln_path, current_cell, next_step_direction, perm, stepi+1, current_cell.value.direction)

  # TODO add the orthogonality check of adjacent cells to discard possible solutions immediately, we first need to mark the path as solid though 
  # before we can reliably count on this


 

# should it be callled coordinate or coordinates???
def check_inside_bound(coordinates:Coordinate) -> bool:
  # TODO we don't have to define these here
  # what I'd like is something like Cell("/") which maps to Mirror.direction = MirrorDirection.SLASH
  m = 7
  n = 7
  x = coordinates.x
  y = coordinates.y
  return x >= 0 and x <= n - 1 and y >= 0 and y <= m - 1

# first_direction tells us where we can go first, that's our starting point
# this shold be calling the recursive function make_step and then kind of backtrack or maybe that's not even needed
# can we actually use any of the tree algorithms???
def find_sol(perm:tuple[int, ...], cell:Cell, matrix):
  current_cell:Cell = cell
  # right, left, down, up (it's a bit counterintuitive)
  directions:list[Coordinate] = [Coordinate(0, 1), Coordinate(0, -1), Coordinate(1, 0), Coordinate(-1, 0)]
  cell_x:Coordinate = cell.coordinate.x
  cell_y:Coordinate = cell.coordinate.y
  # print(f"x={cell_x} y={cell_y}, perm={perm}")

  # can we use the new `match` keyword here instead??
  if cell_x == 0: # we can only go down from here
    going_towards_direction = directions[2]
  elif cell_x == 6: # we can only go up from here
    going_towards_direction = directions[3]
  elif cell_y == 0: # we can only go right from here
    going_towards_direction = directions[0]
  elif cell_y == 6: # we can only go left from here
    going_towards_direction = directions[1]

  """
  at this point we know the direction we're coming from and where we want to go as we need to go through the permutation
  """

  # search_solns -> make_step(current_cell, coming_from, perm_step, mirror_direction.SLASH???) and make_step(current_cell, coming_from, perm_step, mirror_direction.BACKSLASH???)
  # in the first step we don't place any mirror
  # soln_path_head = Node(current_cell.coordinate, None, None, None)
  # we're gonna make the head a hashtable instead for now
  soln_path_head = defaultdict(list)

  make_step(matrix, soln_path_head, current_cell, going_towards_direction, perm, 0, None) #MirrorDirection.SLASH) # first step place the / and explore the path





if __name__ == "__main__":
  # what I'd like is something like Cell("/") which maps to Mirror.direction = MirrorDirection.SLASH
  m = 7 # rows
  n = 7 # columns
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

  # assing the coordinates to the cells
  for i, row in enumerate(matrix):
    for j, column in enumerate(row):
      cell = matrix[i][j]
      if cell is not None:
        cell.coordinate = Coordinate(i, j)

  # instead of starting from the highest we start from the left to right from the first row
  # first pass is to get the mirrors set up from the lasers that already have a value
  for i, row in enumerate(matrix):
    for j, column in enumerate(row):
      cell = matrix[i][j]
      print(f"------------------------------ cell={cell} ------------------------------")
      #print(f"this is column with index {i, j} with value {matrix[i][j]}")
      if cell is not None and cell.is_laser() and cell.value.value is not None:
        # get the prime factors of the laser cell
        prime_factors = get_prime_factors(cell.value.value)
        print(f"prime_factors of {cell.value.value} are {prime_factors}")
        # from the prime factors, generate the "combinations/compactions"
        prime_factors_combinations = get_prime_factor_combinations(prime_factors)
        print(f"prime factors combs/compactions are {prime_factors_combinations}")
        for combination in prime_factors_combinations:
          print(f"---searching perms of the compaction {combination}")
          # for each combination, generate the permutations
          combination_permutations = get_combination_permutations(combination)
          print(f"---combination/compactions={combination} has these permutations {combination_permutations}")
          # for each perm of the combination check if it gets to the solution
          for perm in combination_permutations:
            print(f"-------searching for solutions of perm={perm}")
            # immediately discard perm which have an element that is greater than the sides
            has_any_element_greater_than_sides = any([x > max_m for x in perm])
            #print(f"analysing this perm {perm}, has_any_element_greater_than_sides={has_any_element_greater_than_sides}")
            if has_any_element_greater_than_sides: #print(f"skipping this perm {perm}")
              print(f"-------rejecting this perm={perm} as it has value of step we can never reach {[x>max_m for x in perm]}")
              continue
            # more like walk_the_path of this combination, maybe change the function name
            find_sol(perm, cell, matrix) # TODO need to find a proper way to pass in the first_direction, or we can maybe calculate from the coordinates
            # we need to go through this path and see if we can reach a laser that doesn't have a value
            # we have options at each step
            print(f"-------finished searching for solutions of perm={perm}")
          print(f"---finished searching all perms of combination={combination}")
    print(f"=================================== finished row ===================================")    

  # second pass is to calculate the perimeter and product (easiest)














































































































