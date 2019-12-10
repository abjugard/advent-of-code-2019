from santas_little_helpers import day, get_data, timed, alphabet, submit_answer, base_ops
from collections import Counter
from importlib import import_module
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

def ellipse(y, x, pixel_size):
  yp = (y+2) * pixel_size
  xp = (x+2) * pixel_size
  return (xp, yp), (xp + pixel_size + 7, yp + pixel_size + 7)

def tesseract_parse(result):
  Image = import_module('PIL.Image')
  ImageDraw = import_module('PIL.ImageDraw')
  pytesseract = import_module('pytesseract')

  pixel_size = 10
  dimensions = ((len(result[0]) + 4) * pixel_size, (len(result) + 4) * pixel_size)
  img = Image.new('RGBA', dimensions, (255, 255, 255, 0))
  draw = ImageDraw.Draw(img)
  for y, xs in enumerate(result):
    for x, value in enumerate(xs):
      if value == 1:
        draw.ellipse(ellipse(y, x, pixel_size), fill='black')
  result = pytesseract.image_to_string(img, config='--psm 6')
  return result

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
  try:
    return tesseract_parse(final)
  except ImportError:
    for r in final:
      print(''.join('█' if x == 1 else ' ' for x in r))
    return None

def main() -> None:
  inp = next(get_data(today, base_ops + [('map', int)]))
  print(f'{today} star 1 = {checksum_image(inp)}')
  star2 = decode_image(inp)
  if star2 == None:
    print('for cooler results, please install Pillow and pytesseract\n' \
        + '(along with a tesseract-ocr distribution)\n')
    print(f'{today} star 2 printed in block letters')
  else:
    print(f'{today} star 2 = {star2}')

if __name__ == '__main__':
  timed(main)
