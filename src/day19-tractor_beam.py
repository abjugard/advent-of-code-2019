from santas_little_helpers import day, get_data, timed
from santas_little_utils import run_vm

today = day(2019, 19)

p = []

width = 99

def in_beam(x, y):
  return next(run_vm(p, [x, y])) == 1

def points_in_beam():
  count = 0
  for y in range(50):
    for x in range(50):
      count += in_beam(x, y)
  return count

def test_square(x, y):
  corners = [(0, -width), (width, -width),
             (0,      0), (width,      0)]
  return all(in_beam(x + xd, y + yd) for (xd, yd) in corners)

def find_suitable_area():
  x = 0; y = 50
  while not test_square(x, y):
    while not in_beam(x, y):
      x += 1
    y += 1
  return x * 10000 + y - width

def main() -> None:
  global p
  p = next(get_data(today, [('split', ','), ('map', int)]))
  print(f'{today} star 1 = {points_in_beam()}')
  print(f'{today} star 2 = {find_suitable_area()}')

if __name__ == '__main__':
  timed(main)
