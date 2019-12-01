from santas_little_helpers import day, get_data, timed

today = day(2019, 1)

def fuel(mass):
  return mass // 3 - 2

def rocket_fuel(masses):
  return sum(fuel(mass) for mass in masses)

def recursive_rocket_fuel(masses):
  return sum(sum(module_fuel(mass)) for mass in masses)

def module_fuel(mass):
  while mass > 0:
    mass = fuel(mass)
    if mass > 0:
      yield mass

def main() -> None:
  masses = list(get_data(today, [('func', int)]))
  print(f'{today} star 1 = {rocket_fuel(masses)}')
  print(f'{today} star 2 = {recursive_rocket_fuel(masses)}')

if __name__ == '__main__':
  timed(main)
