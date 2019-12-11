from santas_little_helpers import day, get_data, timed, base_ops
from collections import Counter
from santas_little_utils import tesseract_parse
import sys

today = day(2019, 8)

def checksum_image(inp):
  size = 25*6
  layers = []
  for i in range(len(inp)//size):
    layers += [inp[i*size:(i+1)*size]]
  lowest = sys.maxsize
  layer = None
  for counter in [Counter(l) for l in layers]:
    if counter[0] < lowest:
      lowest = counter[0]
      layer = counter
  return layer[1] * layer[2]

def get_pixel(layers, idx):
  current = None
  for layer in layers:
    current = layer[idx]
    if current != 2:
      return current

def decode_image(inp):
  size = 25*6
  layers = []
  for i in range(len(inp) // size):
    layers += [inp[i*size:(i+1)*size]]
  final = []
  for y in range(6):
    final += [[]]
    for x in range(25):
      final[y] += [get_pixel(layers, y*len(final[0])+x)]
  return tesseract_parse(final)

def main() -> None:
  inp = next(get_data(today, base_ops + [('map', int)]))
  print(f'{today} star 1 = {checksum_image(inp)}')
  star2 = decode_image(inp)
  if star2 == None:
    print(f'{today} star 2 printed in block letters')
  else:
    print(f'{today} star 2 = {star2}')

if __name__ == '__main__':
  timed(main)
