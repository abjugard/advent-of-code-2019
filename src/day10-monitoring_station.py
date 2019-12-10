from santas_little_helpers import day, get_data, timed
from math import atan2

today = day(2019, 10)

def relative_angles(x, y, asteroids):
  d = {}
  for x2, y2 in asteroids:
    if x2 == x and y2 == y:
      continue
    angle = atan2(x2-x, y2-y)
    if angle in d:
      xm, ym = d[angle]
      if abs(x2-x) + abs(y2-y) < abs(xm-x) + abs(ym-y):
        d[angle] = x2, y2
    else:
      d[angle] = x2, y2
  return d

def find_optimal_location(asteroids):
  angles = None
  for x, y in asteroids:
    curr_angles = relative_angles(x, y, asteroids)
    if angles is None or len(curr_angles) > len(angles):
      angles = curr_angles
  return angles

def calculate_winning_bet(angles):
  result = sorted(angles.items(), reverse=True)
  _, (target_x, target_y) = result[199]
  return target_x * 100 + target_y

def parse_asteroids(inp):
  for y, xs in enumerate(inp):
    for x, value in enumerate(xs):
      if value == '#':
        yield x, y

def main() -> None:
  asteroids = list(parse_asteroids(get_data(today)))
  angles = find_optimal_location(asteroids)
  print(f'{today} star 1 = {len(angles)}')
  print(f'{today} star 2 = {calculate_winning_bet(angles)}')

if __name__ == '__main__':
  timed(main)
