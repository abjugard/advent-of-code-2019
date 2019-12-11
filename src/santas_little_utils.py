from collections import defaultdict, deque

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
  if mode is 0:
    return arg
  elif mode is 2:
    return relative_base + arg

def get_iterator(variable):
  try:
    it = iter(variable)
    return it
  except TypeError:
    return get_iterator([variable])

def run_vm(p, inp):
  memory = defaultdict(int, zip(range(len(p)), p))
  inp_gen = get_iterator(inp)
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
      memory[out] = next(inp_gen)
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
      memory[out] = 1 if val1 is val2 else 0
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
