from santas_little_helpers import day, get_data, timed
from santas_little_utils import run_vm, get_last

today = day(2019, 21)

def inject(stdin, springscript):
  for line in springscript:
    stdin.extend(map(ord, f'{line}\n'))

def create_vm(program):
  stdin = []
  vm = run_vm(program, stdin)
  return vm, stdin

def run_with_springscript(program, springscript):
  vm, stdin = create_vm(program)
  inject(stdin, springscript)
  output = get_last(vm)
  return output

def walker(program):
  springscript = [
    "OR A J",
    "AND B J",
    "AND C J",
    "NOT J J",
    "AND D J",
    "WALK"
  ]
  return run_with_springscript(program, springscript)

def runner(program):
  springscript = [
    "OR A J",
    "AND B J",
    "AND C J",
    "NOT J J",
    "AND D J",
    "OR E T",
    "OR H T",
    "AND T J",
    "RUN"
  ]
  return run_with_springscript(program, springscript)

def main() -> None:
  program = next(get_data(today, [('split', ','), ('map', int)]))
  print(f'{today} star 1 = {walker(program)}')
  print(f'{today} star 2 = {runner(program)}')

if __name__ == '__main__':
  timed(main)
