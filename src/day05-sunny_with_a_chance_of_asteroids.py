from santas_little_helpers import day, get_data, timed
from itertools import product

today = day(2019, 5)

inp = None

def get_params(p, pc, count = 2):
  opdata = p[pc] // 100
  for i in range(count):
    mode = opdata // pow(10, i) % 10
    data = p[(pc + 1 + i) % len(p)]
    yield p[data % len(p)] if mode is 0 else data
  return

def execute(inp2 = 1):
  p = inp.copy()
  pc = 0
  outputs = []
  while True:
    opcode = p[pc] % 100
    val1, val2 = get_params(p, pc)
    if opcode is 1:
      p[p[pc + 3]] = val1 + val2
      pc += 4
    elif opcode is 2:
      p[p[pc + 3]] = val1 * val2
      pc += 4
    elif opcode is 3:
      p[p[pc + 1]] = inp2
      pc += 2
    elif opcode is 4:
      outputs += [val1]
      pc += 2
    elif opcode is 5:
      if val1 is not 0:
        pc = val2
      else:
        pc += 3
    elif opcode is 6:
      if val1 is 0:
        pc = val2
      else:
        pc += 3
    elif opcode is 7:
      p[p[pc + 3]] = 1 if val1 < val2 else 0
      pc += 4
    elif opcode is 8:
      p[p[pc + 3]] = 1 if val1 is val2 else 0
      pc += 4
    else:
      pc += 1
      break
  return outputs[-1]

def main() -> None:
  global inp
  inp = next(get_data(today, [('split', ','), ('map', int)]))
  print(f'{today} star 1 = {execute()}')
  print(f'{today} star 2 = {execute(5)}')

if __name__ == '__main__':
  timed(main)
