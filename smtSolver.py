from z3 import *
from helpers import *
from fancyConstraints import *

def gridSolver(grid):
  dim,n = dimn(grid)
  s = Solver()

  # grid of Ints
  gridvars = [[Int('x'+str(i)+str(j)) for j in range(dim)] for i in range(dim)]

  # digit constraints
  for i in range(dim):
    for j in range(dim):
      if grid[i][j] > 0:
        s.add(gridvars[i][j] == grid[i][j])
      else:
        s.add(gridvars[i][j] > 0, gridvars[i][j] <= dim)

  # row constraints
  for i in range(dim):
    s.add(Distinct(gridvars[i]))
  
  # column constraints
  for j in range(dim):
    s.add(Distinct([gridvars[i][j] for i in range(dim)]))
  
  # box constraints
  for ci in range(n):
    for cj in range(n):
      s.add(Distinct([gridvars[i][j] for j in range(cj*n,(cj+1)*n) for i in range(ci*n,(ci+1)*n)]))
  
  return s,gridvars

def solveGrid(grid,extraConstraints=[]):
  s,gridvars = gridSolver(grid)
  s.add(extraConstraints)

  # if satisfiable, print one possible solution
  if s.check() == sat:
    m = s.model()
    printSol(m,gridvars)
    return
  print("no solution")

def solveAll(grid,printAll=False,extraConstraints=[]):
  dim,_ = dimn(grid)
  s,gridvars = gridSolver(grid)
  for f,args in extraConstraints:
    s.add(f(*([gridvars]+args)))
  count = 0

  # while still satisfiable, add to the solution count
  while s.check() == sat:
    count += 1
    m = s.model()
    if printAll:
      printSol(m,gridvars)

    # add a constraint to make sure all solutions are distinct
    constraints = []
    for i in range(dim):
      for j in range(dim):
        if grid[i][j] == 0:
          constraints.append(gridvars[i][j] != m[gridvars[i][j]])
    s.add(Or(constraints))

  print(count,"solution"+("s" if count != 1 else ""))
  return count

