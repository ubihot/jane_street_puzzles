from collections import deque
from itertools import permutations



# TODO: we need to cache these results and second we need to compose these, e.g. 12 can be (1,12), (2,6), (2,3,2), (3,4)
#       so I think for the `composition` (the way how I call it) we just decompose them into 1, 2, 3, 4, 6
# also I think in the example of 12 we should be able to add 1 everywhere as that won't change the result and it can't be many times cause it cannot be orthogonal
# apply_prime_factorization -> return canonical representation in a tuple or a list, list makes sense; e.g. 12 = 2^2 * 3
# e.g. 12 -> [2, 2, 3]
# TODO
# - cache
# - use faster factorization algorithm
# - add check factors produce the input `n` before returnining
def get_prime_factors(n:int) -> tuple[int, ...]:
  # fundamental theorem of arithmetic, 1 is not prime
  # any positive integer > 1 can be represented exactly as product of prime powers
  assert n > 0, f"n needs to be positive"
  if n == 1: return n # p^0 = 1
  # first implementation, simple while loop for all the elements up to x
  factors = []
  c_factor = 2
  x = n
  # when do I exist though if I do this???
  while c_factor < x: # I though need to divide by prime factors and not just any factors, do I keep a table??
    if n % c_factor == 0:
      factors.append(c_factor)
      n = n // c_factor
    else:
      c_factor += 1
  # TODO we can put an assertion here to check that the factors actually math the `n` given as the argument
  return tuple(factors) if len(factors) > 0 else tuple([n])




# e.g. (2, 2, 3) -> [[2, 2, 3], [4, 3], [6, 2], [12], [1, 2, 2, 3], [1, 4, 3], [1, 6, 2], [12, 1], # all the 1s inserted in the intermediate?? no, this does not make sense]
def get_prime_factor_combinations(prime_factors:tuple[int, ...]) -> list[list[int]]:
  assert len(prime_factors) > 0, f"no prime factors given"

  # all_combs_found is the actual output too
  all_combs_found = {tuple(sorted(prime_factors))} # should be a list of lists, if not I can do tuples, needs to be tuple cause cannot hash a list
  #print(f"all_combs_found={all_combs_found}")

  # I need a queue and a visited set which I already have above called `all_combs_found`
  queue = deque([prime_factors])
  while len(queue) > 0:
    combination = queue.popleft()
    s = 0
    n = len(combination)
    # when do we increment the slower one, or let's say when do we get the exhaustions
    # this s and f feels like two loops but I'd like to do them in one instead
    # are they actually two loops???
    while s < n - 1:
      f = s + 1
      #print(f"combination[s]={combination[s]} combination[f]={combination[f]}")
      p = combination[s] * combination[f] # p stands for product
      # do we want [s, f] or we skip this and we do [before_start, s[ and [p] and [f:end]??? need to check this
      potential_combination = combination[:s] + tuple([p]) + combination[s+1:f] + combination[f+1:]

      potential_combination = tuple(sorted(potential_combination))
      if potential_combination not in all_combs_found:
        all_combs_found.add(potential_combination)
        queue.append(potential_combination)

        f += 1 # NOTE do I do this here??? yeah this seems correct

        # until the numbers are the same we skip as it'll produce the same result
        while f < n and combination[f-1] == combination[f]:
          f += 1
        #print(f"all_combs={all_combs_found}")
      s = s + 1
  all_combs_found = list(all_combs_found)
  # for each compaction add 3 extra compactions, I don't think we need to add a 1 in the middle
  # wow super recursive bug introduced here
  for i in range(len(all_combs_found)):
    comb = all_combs_found[i]
    all_combs_found.append(tuple([1]) + comb)
    all_combs_found.append(tuple([1]) + comb + tuple([1]))
    all_combs_found.append(comb + tuple([1]))
  return all_combs_found

# e.g. input is [2,2,3] -> output is [[2,2,3], [2, 3, 2], [3, 2, 2]] since we'll store these in a set which will remove the duplicates
def get_combination_permutations(combination:list[int]) -> list[tuple[int]]:
  # assert 
  # TODO do not cheat and remove duplicates in our own implementation
  perms = list(permutations(combination, len(combination)))
  #print(f"get_combination_permutations perms={perms}")
  #print(f"get_combination_permutations unique={set(perms)}")
  return list(set(perms))


if __name__ == "__main__":
  n = [9, 75, 16, 36, 7, 2025]
  #for x in n:
  #  o = get_prime_factors(x)
  #  print(f"prime factors of {x} are {o}")
  #  combs = get_prime_factor_combinations(o)
  #  print(f"combinations/compactions of {x} are {combs}")
  #  print(f"====================================================")

  # get the "combinations", or compactions let's call them like that
  # test for 16
  a = 16
  a_prime_factors = get_prime_factors(a)
  print(f"prime factors of {a} are {a_prime_factors} and type is {type(a_prime_factors)}")

  expected_o = [tuple(sorted(x)) for x in [(2, 2, 2, 2), (4, 2, 2), (8, 2), (4, 4), tuple([16])]]
  o = sorted(get_prime_factor_combinations(a_prime_factors))
  print(f"combinations/compactions of {a} are {o}")
  assert o == expected_o, f"o={o}, expected_o={expected_o}"

  perms = get_combination_permutations(o[1])
  print(f"permutations of combination's factorization {o[1]} is {perms}")

  # [(2, 2, 2, 2), (2, 2, 4), (2, 8), (4, 4), (16,)]
  # [[2, 2, 2, 2], [2, 2, 4], [2, 8], [4, 4], [16]]
