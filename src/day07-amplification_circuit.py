from santas_little_helpers import day, get_data, timed
from santas_little_utils import run_vm
from itertools import permutations

today = day(2019, 7)

program = None

def evaluate_sequence(phase_sequence):
  vm_stdin = [[inp] for inp in phase_sequence]
  vm_stdout = [[] for _ in range(5)]
  vm = [run_vm(program, vm_stdin[i]) for i in range(5)]
  out = 0
  while True:
    for i in range(5):
      vm_stdin[i] += [out]
      out = next(vm[i])
      if out == None:
        return vm_stdout[4][-1]
      vm_stdout[i] += [out]

def highest_thrust_signal(start, end):
  sequences = permutations(range(start, end+1))
  highest = 0
  for sequence in sequences:
    highest = max(evaluate_sequence(sequence), highest)
  return highest

def main() -> None:
  global program
  program = next(get_data(today, [('split', ','), ('map', int)]))

  print(f'{today} star 1 = {highest_thrust_signal(0, 4)}')
  print(f'{today} star 2 = {highest_thrust_signal(5, 9)}')

if __name__ == '__main__':
  timed(main)
