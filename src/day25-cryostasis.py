from santas_little_helpers import day, get_data, timed
from santas_little_utils import run_vm
from collections import deque, defaultdict
from itertools import combinations

today = day(2019, 25)


OPPOSITE = { 'north': 'south', 'east': 'west', 'west': 'east', 'south': 'north' }
all_output, stdin = '', deque()
path, path_to_security, test_direction, carrying = [], [], None, set()
bad_items = ['infinite loop', 'molten lava', 'escape pod', 'giant electromagnet', 'photons']
paths_available = defaultdict(set)


def run_until_prompt(vm, prompt='Command?'):
  global all_output
  curr_outs = ''
  while not all_output.endswith(prompt):
    try:
      char = chr(next(vm))
      all_output += char
      curr_outs += char
    except Exception:
      return ''.join(curr_outs)
  all_output += '\n'
  return ''.join(curr_outs)


def parse_output(ascii_out, came_from=None):
  global path_to_security, test_direction
  name = ascii_out.strip().split('==')[1].strip()
  lines = [l.strip() for l in ascii_out.strip().split('\n') if len(l)]
  items = []
  end = len(lines)-1
  if 'Items here:' in lines:
    start = lines.index('Items here:')
    items = [i[2:] for i in lines[start+1:-1]]
    end = start
  if 'Doors here lead:' in lines:
    start = lines.index('Doors here lead:')
    doors = [d[2:] for d in lines[start+1:end]]
    for door in doors:
      paths_available[name].add(door)
    if name == 'Security Checkpoint':
      path_to_security.extend(path)
      if came_from:
        test_direction = list(set(doors)-{came_from})[0]
        paths_available[name].remove(test_direction)
  return name, items


def run_commands(vm, commands):
  for command in commands:
    run_command(vm, command)


def run_command(vm, command):
  global all_output
  if command in OPPOSITE:
    if len(path) and path[-1] == OPPOSITE[command]:
      path.pop()
    else:
      path.append(command)
  command += '\n'
  stdin.extend([ord(c) for c in command])
  return run_until_prompt(vm)


def take_items(vm, items):
  for item in items:
    if item in bad_items:
      continue
    carrying.add(item)
    run_command(vm, f'take {item}')


def drop_items(vm, items):
  for item in items:
    carrying.remove(item)
    run_command(vm, f'drop {item}')


def get_alternatives(all_items):
  for n in range(1, len(all_items)):
    for comb in combinations(all_items, n):
      yield set(comb)


def brute_force(vm, all_items):
  alternatives = get_alternatives(all_items)
  tested = set()
  for alternative in alternatives:
    to_remove = carrying - alternative
    to_add = alternative - carrying
    if to_remove:
      drop_items(vm, to_remove)
    if to_add:
      take_items(vm, to_add)
    ascii_out = run_command(vm, test_direction)
    if 'Alert!' not in ascii_out:
      for word in ascii_out.split():
        if all(c.isdigit() for c in word):
          return int(word)


def gather_items(vm, name, items, came_from=None):
  if items:
    take_items(vm, items)
  doors = paths_available[name]
  if came_from:
    doors -= {came_from}
  for door in sorted(doors):
    ascii_out = run_command(vm, door)
    sub_name, items = parse_output(ascii_out, OPPOSITE[door])
    gather_items(vm, sub_name, items, OPPOSITE[door])
  if came_from:
    ascii_out = run_command(vm, came_from)


def impersonate_bot(program):
  vm = run_vm(program, stdin)
  start_room, items = parse_output(run_until_prompt(vm))
  gather_items(vm, start_room, [])
  run_commands(vm, path_to_security)
  return brute_force(vm, carrying.copy())


def main() -> None:
  program = next(get_data(today, [('split', ','), ('map', int)]))
  print(f'{today} star 1 = {impersonate_bot(program)}')


if __name__ == '__main__':
  timed(main)
