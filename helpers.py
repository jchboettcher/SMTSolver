def dimn(grid):
  dim = len(grid)
  return dim,round(dim**0.5)

def printSol(m,gridvars):
  dim,n = dimn(gridvars)
  for i in range(dim):
    print(" | ".join(
      [" ".join(
        [str(m[gridvars[i][j]]) for j in range(cj*n,(cj+1)*n)]
      ) for cj in range(n)]
    ))
    if (i+1) % n == 0:
      print((("-"*(2*n+1)+"+")*n)[1:-2] if i != dim-1 else "")

def parseGrid(gridstr,fancy=False):
  rows = gridstr.strip(" ").strip("\n").split("\n")
  if not fancy:
    return list(map(lambda s: list(map(int,list(s.strip(" ")))),rows))
  return list(map(lambda s: list(map(int,s.strip(" ").split("|"))),rows))
