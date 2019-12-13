from santas_little_helpers import day, get_data, timed
from santas_little_utils import run_vm
from collections import Counter

today = day(2019, 13)

ball_x = paddle_x = None

def count_tiles(program):
  p = program.copy()
  outputs = list(run_vm(p))
  outputs = outputs[:-1]
  m = dict()
  for i in range(0, len(outputs), 3):
    x, y, tile = outputs[i:i+3]
    m[(x, y)] = tile
  return Counter(m.values())[2]

def stdin():
  while True:
    if ball_x < paddle_x:
      yield -1
    elif ball_x == paddle_x:
      yield 0
    else:
      yield 1

def beat_game(program):
  global ball_x, paddle_x
  p = program.copy()
  p[0] = 2
  vm = run_vm(p, stdin())
  score = 0
  while True:
    x = next(vm)
    if x is None:
      break
    y = next(vm)
    tile = next(vm)
    if tile == 4:
      ball_x = x
    if tile == 3:
      paddle_x = x
    if x == -1 and y == 0:
      score = tile
  return score

def main() -> None:
  p = next(get_data(today, [('split', ','), ('map', int)]))
  print(f'{today} star 1 = {count_tiles(p)}')
  print(f'{today} star 2 = {beat_game(p)}')

if __name__ == '__main__':
  timed(main)
