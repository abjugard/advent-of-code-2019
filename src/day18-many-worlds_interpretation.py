from santas_little_helpers import day, get_data, timed, alphabet, base_ops
from collections import deque
import networkx

today = day(2019, 18)

upper_alpha = alphabet.upper()

the_map = []
keys = {}

def get_locations():
  for y in range(len(the_map)):
    for x in range(len(the_map[y])):
      if the_map[y][x] in alphabet:
        keys[the_map[y][x]] = (x, y)

def is_wall(x, y):
  block = the_map[y][x]
  return block == '#'

def build_graph(start):
  graph = networkx.Graph()
  def possible_steps(x, y):
    steps = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    steps = [(x, y) for x, y in steps if x >= 0 and y >= 0 and not is_wall(x, y) and (x, y) not in visited]
    return steps
  visited = set()
  pos = { start }
  graph.add_node(start, start=True)
  while len(pos) > 0:
    visited.update(pos)
    n_pos = set()
    for (x, y) in pos:
      possible = set(possible_steps(x, y))
      graph.add_edges_from(((x, y), other) for other in possible)
      n_pos.update(possible)
    pos = n_pos
  return graph

def cache_obstacles(graph, start, keys=keys):
  obstacles = {}
  ps = keys.copy()
  ps['@'] = start
  for p1n, p1 in ps.items():
    for p2n, p2 in ps.items():
      if p2n == p1n:
        continue
      path = networkx.shortest_path(graph, p1, p2)
      doors = [the_map[y][x] for x, y in path if the_map[y][x] in upper_alpha]
      obstacles[(p1n, p2n)] = obstacles[(p2n, p1n)] = (doors, len(path) - 1)
  return obstacles

def accessible(key, collected, obstacles, keys=keys):
  locked = {c for c in upper_alpha if c.lower() not in collected}
  for target in keys:
    if target in collected:
      continue
    doors, s = obstacles[(key, target)]
    if any(d in locked for d in doors):
      continue
    yield s, target

def part1():
  start = (40, 40)
  graph = build_graph(start)
  obstacles = cache_obstacles(graph, start)

  to_check = deque([('@', 0, '')])
  cache = {}
  results = []

  while to_check:
    p, distance_travelled, keys = to_check.pop()
    if len(keys) == len(alphabet):
      results.append(distance_travelled)
    ck = p, keys
    if ck in cache:
      reachable, s = cache[ck]
      if s <= distance_travelled:
        continue
    else:
      reachable = sorted(accessible(p, keys, obstacles))
    cache[ck] = reachable, distance_travelled
    for s, k in reachable:
      to_check.append((k, distance_travelled + s, ''.join(sorted(keys + k))))
  return min(results)

def quadrant_search(robots):
  to_check = deque([(('@','@', '@', '@'), 0, '')])
  cache = {}

  while to_check:
    ps, distance_travelled, collected = to_check.pop()
    if len(collected) == len(alphabet):
      yield distance_travelled
    ck = ps, collected
    if ck in cache:
      reachable, s = cache[ck]
      if s <= distance_travelled:
        continue
    else:
      reachable = []
      for i, p in enumerate(ps):
        temp = sorted(accessible(p, collected, *robots[i]))
        for data in temp:
          reachable.append((i, data))

    cache[ck] = reachable, distance_travelled
    for i, (s, k) in reachable:
      temp = list(ps)
      temp[i] = k
      to_check.append((tuple(temp), distance_travelled + s, ''.join(sorted(collected + k))))

def part2():
  middle = ['@#@', '###', '@#@']
  starts = []
  for y, ys in enumerate(middle):
    for x, val in enumerate(ys):
      yp = y + 39; xp = x + 39
      the_map[yp][xp] = val
      if the_map[yp][xp] == '@':
        starts.append((xp, yp))
  robots = []
  for start in starts:
    graph = build_graph(start)
    r_keys = {k: p for k, p in keys.items() if p in graph.nodes}
    r_obs = cache_obstacles(graph, start, r_keys)
    robots.append((r_obs, r_keys))
  return min(quadrant_search(robots))

def main() -> None:
  the_map.extend(list(get_data(today, base_ops + [('func', list)])))
  get_locations()
  print(f'{today} star 1 = {part1()}')
  print(f'{today} star 2 = {part2()}')

if __name__ == '__main__':
  timed(main)
