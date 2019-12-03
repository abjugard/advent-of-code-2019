from santas_little_helpers import day, get_data, timed
from itertools import product

today = day(2019, 2)

inp = None

def execute(noun = 12, verb = 2):
  p = inp.copy()
  pc, p[1], p[2] = 0, noun, verb
  while True:
    opcode = p[pc]
    if opcode is 1:
      res = p[p[pc + 1]] + p[p[pc + 2]]
    elif opcode is 2:
      res = p[p[pc + 1]] * p[p[pc + 2]]
    else:
      break
    p[p[pc + 3]] = res
    pc += 4
  return p[0]

def optimal_configuration(target = 19690720):
  for noun, verb in product(range(100), repeat=2):
    if execute(noun, verb) == target:
      return noun * 100 + verb

def main() -> None:
  global inp
  inp = next(get_data(today, [('split', ','), ('map', int)]))
  print(f'{today} star 1 = {execute()}')
  print(f'{today} star 2 = {optimal_configuration()}')

if __name__ == '__main__':
  timed(main)
