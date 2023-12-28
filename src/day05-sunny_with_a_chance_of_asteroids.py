from santas_little_helpers import day, get_data, timed
from santas_little_utils import run_vm, get_last

today = day(2019, 5)

def main() -> None:
  program = next(get_data(today, [('split', ','), ('map', int)]))
  print(f'{today} star 1 = {get_last(run_vm(program, 1))}')
  print(f'{today} star 2 = {get_last(run_vm(program, 5))}')

if __name__ == '__main__':
  timed(main)
