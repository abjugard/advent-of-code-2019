from santas_little_helpers import day, get_data, timed
from santas_little_utils import run_vm, get_last

today = day(2019, 9)

def get_star(program, star = 1):
  return get_last(run_vm(program, [star]))

def main() -> None:
  program = next(get_data(today, [('split', ','), ('map', int)]))

  print(f'{today} star 1 = {get_star(program)}')
  print(f'{today} star 2 = {get_star(program, 2)}')

if __name__ == '__main__':
  timed(main)
