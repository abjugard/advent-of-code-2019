from collections import defaultdict, deque

directions_8 = [('NW', (-1, -1)), ('N', (0, -1)), ('NE', (1, -1)),
                ('W',  (-1,  0)),                 ('E',  (1,  0)),
                ('SW', (-1,  1)), ('S', (0,  1)), ('SE', (1,  1))]

directions_4 = [('N', (0, -1)), ('W', (-1, 0)), ('E', (1, 0)), ('S', (0, 1))]

def parse_instr(memory, pc, relative_base):
  yield memory[pc] % 100
  opdata = memory[pc] // 100
  for i in range(2):
    mode = opdata // pow(10, i) % 10
    arg = memory[pc + 1 + i]
    if mode == 2:
      arg += relative_base
    yield arg if mode == 1 else memory[arg]

def out_addr(memory, pc, relative_base, i):
  opdata = memory[pc] // 100
  mode = opdata // pow(10, i - 1) % 10
  arg = memory[pc + i]
  if mode == 0:
    return arg
  elif mode == 2:
    return relative_base + arg
  raise NotImplementedError(f'No implementation for parameter mode: {mode}')

def get_iterator(variable):
  try:
    it = iter(variable)
    return it
  except TypeError:
    return get_iterator([variable])

def run_vm(p, inp = None):
  memory = defaultdict(int, zip(range(len(p)), p))
  inp_is_deque = type(inp) == deque
  if not inp_is_deque:
    inp = get_iterator(inp)
  pc = relative_base = 0
  while True:
    opcode, val1, val2 = parse_instr(memory, pc, relative_base)
    if opcode == 1:
      out = out_addr(memory, pc, relative_base, 3)
      memory[out] = val1 + val2
      pc += 4
    elif opcode == 2:
      out = out_addr(memory, pc, relative_base, 3)
      memory[out] = val1 * val2
      pc += 4
    elif opcode == 3:
      out = out_addr(memory, pc, relative_base, 1)
      if inp_is_deque:
        if len(inp) == 0:
          yield None
        memory[out] = inp.popleft()
      else:
        memory[out] = next(inp)
      pc += 2
    elif opcode == 4:
      yield val1
      pc += 2
    elif opcode == 5:
      if val1 != 0:
        pc = val2
      else:
        pc += 3
    elif opcode == 6:
      if val1 == 0:
        pc = val2
      else:
        pc += 3
    elif opcode == 7:
      out = out_addr(memory, pc, relative_base, 3)
      memory[out] = 1 if val1 < val2 else 0
      pc += 4
    elif opcode == 8:
      out = out_addr(memory, pc, relative_base, 3)
      memory[out] = 1 if val1 == val2 else 0
      pc += 4
    elif opcode == 9:
      relative_base += val1
      pc += 2
    elif opcode == 99:
      yield None
      pc += 1
      break
    else:
      raise NotImplementedError(f'No implementation for opcode: {opcode}')

def get_last(generator):
  d = deque(generator, maxlen=2)
  d.pop()
  return d.pop()

def ellipse(y, x, pixel_size):
  yp = (y+2) * pixel_size
  xp = (x+2) * pixel_size
  return (xp, yp), (xp + pixel_size + 7, yp + pixel_size + 7)

def create_image(result):
  from PIL import Image, ImageDraw
  pixel_size = 8
  dimensions = ((len(result[0]) + 4) * pixel_size, (len(result) + 4) * pixel_size)
  img = Image.new('RGBA', dimensions, (255, 255, 255, 0))
  draw = ImageDraw.Draw(img)
  for y, xs in enumerate(result):
    for x, value in enumerate(xs):
      if value == 1:
        draw.ellipse(ellipse(y, x, pixel_size), fill='black')
  return img

def tesseract_parse(inp):
  try:
    import pytesseract
    image = inp
    if isinstance(inp, list):
      image = create_image(inp)
    return pytesseract.image_to_string(image, config='--psm 6')
  except ImportError:
    for line in inp:
      print(''.join('█' if c == 1 else ' ' for c in line))
    print('for cooler results, please install Pillow and pytesseract\n' \
        + '(along with a tesseract-ocr distribution)')
    return None


def build_dict_map(map_data, conv_func=None, key_func=None, criteria=None):
  the_map = dict()
  def get_value(c, p):
    return c if conv_func is None else conv_func(c, p)
  def get_key(c, p):
    return p if key_func is None else key_func(c, p)
  for y, xs in enumerate(map_data):
    for x, c in enumerate(xs):
      if criteria is None or c in criteria:
        the_map[get_key(c, (x, y))] = get_value(c, (x, y))
    else:
      w = x + 1
  else:
    h = y + 1
  return the_map, (w, h)


def map_frame(w, h):
  for x in range(w):
    yield (x, -1)
    yield (x, w)
  for y in range(h):
    yield (-1, y)
    yield (h, y)
  return


def neighbours(p, borders=None, diagonals=False, labels=False):
  def within_borders(p_n, borders):
    if borders is None:
      return True
    elif isinstance(borders, dict):
      return p_n in borders
    elif isinstance(borders, set):
      return p_n in borders
    elif isinstance(borders, (list, tuple)):
      x_n, y_n = p_n
      h = len(borders)
      return h > 0 and 0 <= y_n < h and 0 <= x_n < len(borders[0])
    raise Exception(f'unknown datastructure: {type(borders)}')
  x, y = p
  for label, (xd, yd) in directions_8 if diagonals else directions_4:
    p_n = x + xd, y + yd
    if within_borders(p_n, borders):
      yield (label, p_n) if labels else p_n


def mul(numbers):
  result = 1
  for n in numbers:
    if n == 0:
      return 0
    result *= n
  return result


def transpose(l):
  return list(map(list, zip(*l)))


def flatten(list_of_lists):
  return [item for l in list_of_lists for item in l]


def ints(num_strings, split=None):
  if split:
    num_strings = [s.strip() for s in num_strings.split(split)]
  return tuple(map(int, num_strings))
