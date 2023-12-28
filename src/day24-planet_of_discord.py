from santas_little_helpers import day, get_data, timed
from santas_little_utils import neighbours, directions_4, flatten

today = day(2019, 24)

N_OUTER_LAYERS, N_INNER_LAYERS = -100, 110


def evolve(last_map):
  the_map = []
  for y, xs in enumerate(last_map):
    l = []
    for x, c in enumerate(xs):
      n_count = sum(last_map[y_n][x_n] for (x_n, y_n) in neighbours((x, y), borders=last_map))
      l.append(n_count == 1 if c else 1 <= n_count <= 2)
    the_map.append(tuple(l))
  return tuple(the_map)


def biodiversity_rating(the_map):
  seen = set()
  while the_map not in seen:
    seen.add(the_map)
    the_map = evolve(the_map)
  return sum(2**n for n, c in enumerate(flatten(the_map)) if c)


def construct_initial(the_map, depth=N_OUTER_LAYERS):
  grid = [[False for _ in range(5)] for _ in range(5)]
  if depth == N_INNER_LAYERS:
    return None
  if depth == 0:
    grid = [list(line) for line in the_map]
  grid[2][2] = construct_initial(the_map, depth + 1)
  return grid


def center_neighbours(label, layer):
  if layer is None: return []
  top, *_, bottom = layer
  if label == 'N': return bottom
  if label == 'S': return top
  left, *_, right = list(zip(*layer))
  if label == 'E': return left
  if label == 'W': return right


def neighbours_rec(x, y, layer, surrounding):
  n, w, e, s = surrounding
  for label, (xd, yd) in directions_4:
    x_n, y_n = x + xd, y + yd
    if   y_n == -1: yield n
    elif x_n == -1: yield w
    elif y_n == 5:  yield s
    elif x_n == 5:  yield e
    elif y_n == 2 and x_n == 2:
      for np in center_neighbours(label, layer[2][2]):
        yield np
    else:
      yield layer[y_n][x_n]


def evolve_rec(layer, depth=N_OUTER_LAYERS, surrounding=[False,False,False,False]):
  if depth == N_INNER_LAYERS:
    return None
  new_layer = []
  for y, xs in enumerate(layer):
    l = []
    for x, c in enumerate(xs):
      ns = list(neighbours_rec(x, y, layer, surrounding))
      if y == 2 and x == 2:
        l.append(evolve_rec(layer[2][2], depth+1, ns))
      else:
        n_count = sum(ns)
        l.append(n_count == 1 if c else 1 <= n_count <= 2)
    new_layer.append(l)
  return new_layer


def count_bugs(the_map):
  if the_map == None:
    return False
  curr = sum(c for c in flatten(the_map) if isinstance(c, bool))
  return curr + count_bugs(the_map[2][2])



def extrapolate_bug_reproduction(the_map):
  the_map = construct_initial(the_map)
  for _ in range(200):
    the_map = evolve_rec(the_map)
  return count_bugs(the_map)


def parse(line):
  return tuple(c == '#' for c in line[:-1])


def main() -> None:
  grid = tuple(get_data(today, [('func', parse)]))
  print(f'{today} star 1 = {biodiversity_rating(grid)}')
  print(f'{today} star 2 = {extrapolate_bug_reproduction(grid)}')

if __name__ == '__main__':
  timed(main)
