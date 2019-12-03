from santas_little_helpers import day, get_data, timed
from collections import defaultdict
import sys

today = day(2019, 3)

offsets = {     'U': (0,  1),
  'L': (-1, 0), 'D': (0, -1), 'R': (1, 0) }

def intersections(wires):
  visits = defaultdict(dict)
  for idx, line in enumerate(wires):
    x = y = s = 0
    for (xdiff, ydiff), distance in line:
      for _ in range(distance):
        x += xdiff; y += ydiff; s += 1
        if idx not in visits[(x, y)]:
          visits[(x, y)][idx] = s
  closest = shortest = sys.maxsize
  for (x, y), visitors in visits.items():
    if len(visitors) < 2:
      continue
    closest = min(closest, abs(x) + abs(y))
    shortest = min(shortest, sum(visitors.values()))
  return closest, shortest

def parse(inp):
  return [(offsets[d[0]], int(d[1:])) for d in inp.split(',')]

def main() -> None:
  wires = get_data(today, [('func', parse)])
  star1, star2 = intersections(wires)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {star2}')

if __name__ == '__main__':
  timed(main)
