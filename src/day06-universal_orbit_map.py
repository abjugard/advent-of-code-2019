from santas_little_helpers import day, get_data, timed, base_ops
from collections import defaultdict, Counter

today = day(2019, 6)

orbit_dict_inverted = {}

def orbit_path(target):
  curr = target
  path = []
  while curr in orbit_dict_inverted:
    curr = orbit_dict_inverted[curr]
    path += [curr]
  return path

def build_inverse_map(orbit_dict):
  for obj in orbit_dict:
    for orbiter in orbit_dict[obj]:
      orbit_dict_inverted[orbiter] = obj

def calculate_orbits(orbits):
  orbit_dict = defaultdict(list)
  for obj, orbiter in orbits:
    orbit_dict[obj] += [orbiter]
  build_inverse_map(orbit_dict)
  for obj, orbiters in orbit_dict.items():
    count = len(orbit_path(obj)) + 1
    yield count * len(orbiters)

def distance_to_santa():
  counted = Counter(orbit_path('SAN') + orbit_path('YOU'))
  return sum(1 for count in counted.values() if count < 2)

def main() -> None:
  orbits = list(get_data(today, base_ops + [('split', ')')]))
  print(f'{today} star 1 = {sum(calculate_orbits(orbits))}')
  print(f'{today} star 2 = {distance_to_santa()}')

if __name__ == '__main__':
  timed(main)
