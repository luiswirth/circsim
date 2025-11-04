import math
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
  Resistor(1, (2, 1)),
]

capacitors = [
  Capacitor(1, (1, 0))
]

current_sources = [
  #[[CurrentSource(1.0, (2, 0))
]
voltage_sources = [
  VoltageSource(5.0, (2, 0))
]

nnodes = 0
for resistor in resistors:
  nnodes = max(nnodes, max(resistor.wire))
for capacitor in capacitors:
  nnodes = max(nnodes, max(capacitor.wire))
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
for capacitor in capacitors:
  i = capacitor.wire[0] - 1
  j = capacitor.wire[1] - 1
  c = capacitor.capacitance
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


T = 2.0
dt = 0.05
nsteps = int(math.ceil(T/dt))

sys_mat = np.block([
  [G+C/dt, B],
  [B.T, Z],
])

#vinit = np.zeros(nnodes)
vinit = np.array([1.0, 5.0])

vs = [vinit]

for istep in range(nsteps):
  print(f"{istep}/{nsteps-1}")

  # TODO: update b and e
  rhs_vec = np.concatenate([
    b + (C @ vs[istep])/dt,
    e,
  ])

  # TODO: compute factorization
  x = np.linalg.solve(sys_mat, rhs_vec)
  v = x[:nnodes]
  vs.append(v)

