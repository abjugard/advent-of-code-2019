from santas_little_helpers import day, get_data, timed, alphabet, submit_answer, base_ops
from santas_little_utils import run_vm, get_last

today = day(2019, 17)

offsets = [ (0,  1),
   (-1, 0), (0, -1), (1, 0) ]

m = []

def is_intersection(x, y):
  height = len(m)-1
  width = len(m[0])-1
  for x2, y2 in [(x + xdiff, y + ydiff) for (xdiff, ydiff) in offsets]:
    if y2 < 0 or y2 > height or x2 < 0 or x2 > width:
      return False
    if m[y2][x2] != '#':
      return False
  return True

def part1(inp):
  outputs = []
  vm = run_vm(inp.copy())
  try:
    while True:
      outputs.append(next(vm))
  except Exception:
    pass
  out_s = ''.join([chr(c) for c in outputs[:-1]])
  for line in out_s.split('\n'):
    split = [c for c in line]
    if len(split) > 0:
      m.append(split)
  s = 0
  for y, ys in enumerate(m):
    for x, value in enumerate(ys):
      if value == '#' and is_intersection(x, y):
        s += x * y
  return s

def part2(inp):
  inp[0] = 2
  instrs = 'A,B,A,C,B,A,C,B,A,C\nL,12,L,12,L,6,L,6\nR,8,R,4,L,12\nL,12,L,6,R,12,R,8\nn\n'
  stdin = [ord(c) for c in instrs]
  vm = run_vm(inp.copy(), stdin)
  outputs = []
  try:
    while True:
      outputs.append(next(vm))
  except Exception:
    pass
  return outputs[-2]

def main() -> None:
  inp = next(get_data(today, [('split', ','), ('map', int)]))
  print(f'{today} star 1 = {part1(inp)}')
  print(f'{today} star 2 = {part2(inp)}')

if __name__ == '__main__':
  timed(main)
