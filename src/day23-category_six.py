from santas_little_helpers import day, get_data, timed
from santas_little_utils import run_vm, flatten
from collections import defaultdict, deque

today = day(2019, 23)


def setup_network(program):
  stdins, vms, messages = {}, {}, defaultdict(list)
  for i in range(50):
    stdins[i] = deque([i])
    vms[i] = run_vm(program, stdins[i])
  return stdins, vms, messages


def simulate_network(program):
  stdins, vms, messages = setup_network(program)
  nat_value = first_found = None
  seen = set()
  while True:
    for address, vm in vms.items():
      if not stdins[address]:
        stdins[address].append(-1)
      output = next(vm)
      if output is not None:
        messages[address].append(output)
        if len(messages[address]) == 3:
          destination, x, y, *messages[address] = messages[address]
          if destination == 255:
            if not first_found:
              first_found = True
              yield y
            nat_value = (x, y)
          else:
            stdins[destination].extend([x, y])
      idle = len(flatten(stdins.values())) == 0
      if idle and nat_value:
        stdins[0].extend(nat_value)
        _, y = nat_value
        if y in seen:
          yield y
        seen.add(y)
        nat_value = None


def main() -> None:
  program = next(get_data(today, [('split', ','), ('map', int)]))
  star_gen = simulate_network(program)
  print(f'{today} star 1 = {next(star_gen)}')
  print(f'{today} star 2 = {next(star_gen)}')


if __name__ == '__main__':
  timed(main)
