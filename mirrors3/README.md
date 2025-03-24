DONE:
- get prime factors of laser values
- get the "combinations/compactions" of the prime factors
- get the permutations of the "combinations/compactions"



TODO:
- faster prime factorization, the current one is a naive implementation
- no cheat permutations implementation
- for all the permutations, check if you can create the mirrors, if so mark the path as a possible solution or if there's only one path, mark it as a "solid" solution. Search in all the comb's perms. Make this fast.
- write tests for the utils functions
- function to find adjacent orthogonal cells
- in the perms, we need to have perms (permutations), without the 1 or with the one after each number.
- rules: check for orthogonality of adjacent cells with mirrors
- rules: stop a possible solution if you're in a solid path
- once found the mirrors compute the `unlabeled` laser values (easy part)
- compute the product of the perimiter's side' sum (easiest part)
- have a nice visualization of the algorithm running and a nice visual the final mirrors in the grid (maybe serialize the solution and give it to a js renderer to display it beautifully or even in python maybe)
- create the grid from a input file
