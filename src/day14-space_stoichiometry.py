from santas_little_helpers import day, get_data, timed, base_ops
from collections import defaultdict
from math import ceil

today = day(2019, 14)

reaction_remainders = defaultdict(int)
reactions = {}

def calculate_ore_rec(target, needed):
  reagents, produced = reactions[target]
  needed -= reaction_remainders[target]
  multiplier = ceil(needed / produced)
  reaction_remainders[target] = multiplier * produced - needed
  for reagent, amount in reagents.items():
    r_needed = multiplier * amount
    if reagent == 'ORE':
      yield r_needed
      continue
    yield calculate_ore(reagent, r_needed)

def calculate_ore(target, needed):
  return sum(calculate_ore_rec(target, needed))

def minimum_ore():
  return calculate_ore('FUEL', 1)

def maximum_fuel():
  fuel = 0
  exponent = 7
  while exponent >= 0:
    increment = pow(10, exponent)
    reaction_remainders.clear()
    while calculate_ore('FUEL', fuel + increment) < 1e12:
      fuel += increment
    exponent -= 1
  else:
    fuel -= increment
  return fuel

def parse(line):
  def inner_parse(requirement):
    count, reagent = requirement.split(' ')
    return int(count), reagent
  left, right = line.split(' => ')
  produced, target = inner_parse(right)
  reqs = map(inner_parse, left.split(', '))
  return target, ({req: count for count, req in reqs}, produced)

def main() -> None:
  reactions.update(get_data(today, base_ops + [('func', parse)]))
  print(f'{today} star 1 = {minimum_ore()}')
  print(f'{today} star 2 = {maximum_fuel()}')

if __name__ == '__main__':
  timed(main)
