from santas_little_helpers import *
from collections import defaultdict
import networkx as nx

today = day(2019, 20)

alpha = alphabet.upper()

def neighbours(point):
  return [(point[0] + dx, point[1] + dy) for dx, dy in zip([0, 1, 0, -1], [-1, 0, 1, 0])]

def get_portal_key(pos, grid):
  x, y = pos
  key = None
  if x in [2, 82]:
    key = grid[(x-2, y)] + grid[(x-1, y)]
  elif x in [26, 106]:
    key = grid[(x+1, y)] + grid[(x+2, y)]
  elif y in [2, 78]:
    key = grid[(x, y-2)] + grid[(x, y-1)]
  elif y in [26, 102]:
    key = grid[(x, y+1)] + grid[(x, y+2)]
  if key is not None and all(c in alpha for c in key):
    return key
  return None

def construct_graph(maze, levels=0):
  grid = defaultdict(lambda: '#')
  W, H = len(maze[0]), len(maze)

  for y in range(H):
    for x in range(W):
      if maze[y][x] != ' ':
        grid[(x, y)] = maze[y][x]

  portals = defaultdict(list)
  G = nx.Graph()
  for y in range(1, H - 1):
    for x in range(1, W - 1):
      pos = x, y
      symbol = grid[pos]
      if symbol != '.':
        continue
      key = get_portal_key(pos, grid)
      if key is not None:
        portals[key].append(pos)
      if levels > 0:
        for i in range(levels):
          G.add_node((*pos, i))
      else:
        G.add_node(pos)
      for n_pos in neighbours(pos):
        if grid[n_pos] != '.':
          continue
        if levels > 0:
          for i in range(levels):
            G.add_edge((*pos, i), (*n_pos, i))
        else:
          G.add_edge(pos, n_pos)

  for pads in portals.values():
    if len(pads) == 2:
      if levels > 0:
        if pads[0][0] in [2, W - 3] or pads[0][1] in [2, H - 3]:
          outer, inner = pads
        else:
          inner, outer = pads
        for i in range(levels - 1):
          G.add_edge((*inner, i), (*outer, i + 1))
          G.add_edge((*outer, i + 1), (*inner, i))
      else:
        G.add_edge(*pads)
  return G, portals

def solve_flat_maze(maze):
  G, portals = construct_graph(maze)

  start = portals['AA'][0]
  end = portals['ZZ'][0]

  return nx.shortest_path_length(G, start, end)

def solve_recursive_maze(maze):
  G, portals = construct_graph(maze, levels=30)

  start = *portals['AA'][0], 0
  end = *portals['ZZ'][0], 0

  return nx.shortest_path_length(G, start, end)


def main() -> None:
  maze = list(get_data(today))
  print(f'{today} star 1 = {solve_flat_maze(maze)}')
  print(f'{today} star 2 = {solve_recursive_maze(maze)}')

if __name__ == '__main__':
  timed(main)
