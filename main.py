from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class Resistor:
  conductance: float
  # 2-tuple of connected nodes
  wire: tuple[int, int]

@dataclass(slots=True)
class Capacitor:
    capacitance: float
    wire: tuple[int, int]

@dataclass(slots=True)
class CurrentSource:
  value: float
  wire: tuple[int, int]

@dataclass(slots=True)
class VoltageSource:
    value: float
    wire: tuple[int,int]

resistors = [
  Resistor(1/1000, (1, 2)),
  Resistor(1/1000, (2, 0)),
]

condensators = [
  #Capacitor(1.0, (1, 0))
]

current_sources = [
  #[[CurrentSource(1.0, (2, 0))
]
voltage_sources = [
  VoltageSource(10.0, (1, 0))
]

nnodes = 0
for resistor in resistors:
  nnodes = max(nnodes, max(resistor.wire))
for condensator in condensators:
  nnodes = max(nnodes, max(condensator.wire))
for source in current_sources:
  nnodes = max(nnodes, max(source.wire))
for source in voltage_sources:
  nnodes = max(nnodes, max(source.wire))

def add_vec_entry(vec, i, v):
  if i >= 0:
    vec[i] += v

b = np.zeros(nnodes)

for current_source in current_sources:
  i = current_source.wire[0] - 1
  j = current_source.wire[1] - 1
  add_vec_entry(b, i, current_source.value)
  add_vec_entry(b, j, -current_source.value)

print(b)


def add_mat_entry(mat, i, j, v):
  if i >= 0 and j >= 0:
    mat[i, j] += v

G = np.zeros((nnodes, nnodes))
for resistor in resistors:
  i = resistor.wire[0] - 1
  j = resistor.wire[1] - 1
  c = resistor.conductance
  add_mat_entry(G, i, i, c)
  add_mat_entry(G, j, j, c)
  add_mat_entry(G, i, j, -c)
  add_mat_entry(G, j, i, -c)

print(G)


C = np.zeros((nnodes, nnodes))
for condensator in condensators:
  i = condensator.wire[0] - 1
  j = condensator.wire[1] - 1
  c = condensator.capacitance
  add_mat_entry(C, i, i, c)
  add_mat_entry(C, j, j, c)
  add_mat_entry(C, i, j, -c)
  add_mat_entry(C, j, i, -c)

B = np.zeros((nnodes, len(voltage_sources)))
e = np.zeros(len(voltage_sources))
for isource, source in enumerate(voltage_sources):
  i = source.wire[0] - 1
  j = source.wire[1] - 1
  v = source.value
  add_mat_entry(B, i, isource, +1)
  add_mat_entry(B, j, isource, -1)
  e[isource] = v
  
Z = np.zeros((len(voltage_sources), len(voltage_sources)))
A = np.block([
  [G, B],
  [B.T, Z]
])
rhs = np.concatenate([b, e])

v = np.linalg.solve(A, rhs)
print(v)


#T = 2.0
#dt = 0.05
#nsteps = int(math.ceil(T/dt))
#
#sys_mat = G+C/dt
#
##vinit = np.zeros(nnodes)
#vinit = np.array([1.0])
#vs = [vinit]
#
#for istep in range(nsteps):
#  # TODO: update b
#  rhs_vec = b + (C @ vs[istep])/dt
#  # TODO: compute factorization
#  v = np.linalg.solve(sys_mat, rhs_vec)
#  vs.append(v)
#  print(f"{istep}/{nsteps-1}")
