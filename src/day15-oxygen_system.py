from santas_little_helpers import day, get_data, timed
from santas_little_utils import run_vm
from collections import defaultdict
from readchar import readkey

today = day(2019, 15)

offsets = {   1: (0,  1),
  4: (-1, 0), 2: (0, -1), 3: (1, 0) }

m = defaultdict(lambda: ' ', { (0, 0): '+' })
stdin = []
moving = 3

def next_pos(x, y, d):
  _, (xdiff, ydiff) = offsets[d]
  return x + xdiff, y + ydiff

def print_map(xp, yp):
  keys = list(m.keys())
  keys += [(xp, yp)]
  xmin = min(keys, key=lambda p: p[0])[0]
  ymin = min(keys, key=lambda p: p[1])[1]
  xmax = max(keys, key=lambda p: p[0])[0]
  ymax = max(keys, key=lambda p: p[1])[1]
  lines = []
  for y in range(ymin, ymax+1):
    line = ''
    for x in range(xmin, xmax+1):
      if x == xp and y == yp:
        line += 'D'
      else:
        line += m[(x, y)]
    lines.append(line)

  for line in lines:
    print(line)
  print()

def test(vm, d):
  opposite = d + 1 if d % 2 == 1 else d - 1
  stdin.append(d)
  reply = next(vm)
  if reply != 0:
    stdin.append(opposite)
    next(vm)
  return reply

def test_all(vm, x, y):
  for d, (xdiff, ydiff) in offsets.items():
    next_pos = (x + xdiff, y + ydiff)
    if m[next_pos] != ' ':
      continue
    reply = test(vm, d)
    if reply == 0:
      m[next_pos] = '#'
    elif reply == 1:
      if m[next_pos] == ' ':
        m[next_pos] = '.'
    elif reply == 2:
      if m[next_pos] == ' ':
        m[next_pos] = 'O'
      break

def get_traversable(x, y):
  for d, (xdiff, ydiff) in offsets.values():
    next_pos = (x + xdiff, y + ydiff)
    if m[next_pos] in '.+':
      yield d

def run_game(program):
  vm = run_vm(program, stdin)
  x = y = 0
  i = 0
  while True:
    test_all(vm, x, y)
    print(f'Iteration {i}:')
    print_map(x, y)
    i += 1
    key = readkey()
    if key == '\x03':
      break
    if key == '\x1b[A':
      travel_direction = 2
    if key == '\x1b[D':
      travel_direction = 4
    if key == '\x1b[B':
      travel_direction = 1
    if key == '\x1b[C':
      travel_direction = 3
    stdin.append(travel_direction)
    reply = next(vm)
    if reply != 0:
      xdiff, ydiff = offsets[travel_direction]
      x += xdiff; y += ydiff
    exit

def iterate_graph(lines):
  for y, ys in enumerate(lines):
    copy = ys.copy()
    for x, val in enumerate(copy):

def main() -> None:
  p = next(get_data(today, [('split', ','), ('map', int)]))
  run_game()

if __name__ == '__main__':
  timed(main)
