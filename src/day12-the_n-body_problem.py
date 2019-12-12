from santas_little_helpers import day, get_data, timed
from math import gcd
import re

r = re.compile(r'<x=(?P<x>[-]*\d+), y=(?P<y>[-]*\d+), z=(?P<z>[-|]*\d+)>')

today = day(2019, 12)

def update_moon(moon, others):
  pos = moon[0]
  vel = list(moon[1])
  for (other_pos, _) in others:
    for axis in range(len(pos)):
      if other_pos[axis] > pos[axis]:
        vel[axis] += 1
      elif other_pos[axis] < pos[axis]:
        vel[axis] -= 1
  new_p = [pos[axis] + vel[axis] for axis in range(len(pos))]
  return new_p, vel

def step(moons):
  next_moons = []
  for moon in moons:
    others = [m for m in moons if m is not moon]
    next_moons += [update_moon(moon, others)]
  return next_moons

def calculate_energy(moons):
  for (pos, vel) in moons:
    yield sum(map(abs, pos)) * sum(map(abs, vel))

def total_system_energy(moons):
  for _ in range(1000):
    moons = step(moons)
  return sum(calculate_energy(moons))

def lcm(x, y):
  return (x*y) // gcd(x, y)

def find_system_interval(moons):
  seen = [set(), set(), set()]
  interval = [None, None, None]
  iteration = 0
  while True:
    if all(interval):
      i_x, i_y, i_z = interval
      return lcm(i_x, lcm(i_y, i_z))
    moons = step(moons)
    for axis in range(len(interval)):
      if interval[axis]:
        continue
      key = tuple((p[axis], v[axis]) for p, v in moons)
      if key in seen[axis]:
        interval[axis] = iteration
      seen[axis].add(key)
    iteration += 1

def parse_moon(line):
  pos = list(map(int, r.match(line).groups()))
  return (pos, (0, 0, 0))

def main() -> None:
  moons = list(get_data(today, [('func', parse_moon)]))
  print(f'{today} star 1 = {total_system_energy(moons)}')
  print(f'{today} star 2 = {find_system_interval(moons)}')

if __name__ == '__main__':
  timed(main)
