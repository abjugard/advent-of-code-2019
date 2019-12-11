from santas_little_helpers import day, get_data, timed, alphabet, submit_answer, base_ops
from santas_little_utils import run_vm, tesseract_parse
from collections import defaultdict

today = day(2019, 11)

dirs = {
  ( 0,  1): { 0: (-1,  0), 1: ( 1,  0) },
  (-1,  0): { 0: ( 0, -1), 1: ( 0,  1) },
  ( 0, -1): { 0: ( 1,  0), 1: (-1,  0) },
  ( 1,  0): { 0: ( 0,  1), 1: ( 0, -1) }
}

def paint_hull(inp, starting_colour=0):
  direction = (0, 1)
  hull = defaultdict(int)
  stdin = [starting_colour]
  vm = run_vm(inp, stdin)
  x = y = 0
  painted = 0
  while True:
    colour = next(vm)
    if colour == None:
      break
    hull[(x, y)] = colour
    direction = dirs[direction][next(vm)]
    x += direction[0]; y += direction[1]
    stdin += [hull[(x, y)]]
  return hull

def verify_result(p):
  hull = paint_hull(p, 1)
  final = []
  for y, y_actual in enumerate(reversed(range(-5, 1))):
    final += [[]]
    for x in range(1, 40):
      final[y] += [hull[(x, y_actual)]]
  result = tesseract_parse(final)
  if result != None:
    result = result.replace(' ', '')
  return result

def main() -> None:
  p = next(get_data(today, [('split', ','), ('map', int)]))
  print(f'{today} star 1 = {len(paint_hull(p).values())}')
  star2 = verify_result(p)
  if star2 == None:
    print(f'{today} star 2 printed in block letters')
  else:
    print(f'{today} star 2 = {star2}')

if __name__ == '__main__':
  timed(main)
