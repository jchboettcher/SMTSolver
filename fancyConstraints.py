from z3 import *
from helpers import *

def sums(gridvars,gridmap,sumdict):
  dim,_ = dimn(gridmap)
  dists = {}
  for i in range(dim):
    for j in range(dim):
      cell = gridmap[i][j]
      if cell:
        if cell not in dists:
          dists[cell] = [gridvars[i][j]]
        else:
          dists[cell].append(gridvars[i][j])
  return list(map(lambda x: Sum(x[1]) == sumdict[x[0]],dists.items()))

def distincts(gridvars,gridmap):
  dim,_ = dimn(gridmap)
  dists = {}
  for i in range(dim):
    for j in range(dim):
      cell = gridmap[i][j]
      if cell:
        if cell not in dists:
          dists[cell] = [gridvars[i][j]]
        else:
          dists[cell].append(gridvars[i][j])
  return list(map(Distinct,dists.values()))

def thermos(gridvars,thermolist,strict=True):
  dim,_ = dimn(thermolist[0])
  constrs = []
  for gridmap in thermolist:
    thermo = []
    for i in range(dim):
      for j in range(dim):
        cell = gridmap[i][j]
        if cell:
          thermo.append((cell,gridvars[i][j]))
    thermo.sort()
    for i in range(len(thermo)-1):
      constrs.append((thermo[i][1] < thermo[i+1][1]) if strict else (thermo[i][1] <= thermo[i+1][1]))
  return constrs

def diffs(gridvars,gridmap,upper=None,lower=None,diags=True):
  dim,_ = dimn(gridmap)
  dirs = [(0,1),(1,0)]
  if diags:
    dirs.extend([(1,1),(1,-1)])
  constrs = []
  for i in range(dim):
    for j in range(dim):
      for ii,jj in dirs:
        newi,newj = i+ii,j+jj
        if newi >= 0 and newi < dim and newj >= 0 and newj < dim:
          if gridmap[i][j] and gridmap[newi][newj]:
            diff = gridvars[i][j]-gridvars[newi][newj]
            if upper:
              constrs.append(And(diff <= upper,diff >= -upper))
            if lower:
              constrs.append(Or(diff >= lower,diff <= -lower))
  return constrs
