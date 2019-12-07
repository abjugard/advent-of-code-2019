from santas_little_helpers import day, get_data, timed
from itertools import permutations

today = day(2019, 7)

vm_state = {}

program = None

def get_params(p, pc, count = 2):
  opdata = p[pc] // 100
  for i in range(count):
    mode = opdata // pow(10, i) % 10
    data = p[(pc + 1 + i) % len(p)]
    yield p[data % len(p)] if mode is 0 else data
  return

def run_vm(vm_name, inputs):
  if vm_name in vm_state:
    p, pc, outputs, inp_count = vm_state[vm_name]
  else:
    p = program.copy()
    pc = 0
    outputs = []
    inp_count = 0
  while True:
    opcode = p[pc] % 100
    val1, val2 = get_params(p, pc)
    if opcode is 1:
      p[p[pc + 3]] = val1 + val2
      pc += 4
    elif opcode is 2:
      p[p[pc + 3]] = val1 * val2
      pc += 4
    elif opcode is 3:
      if inp_count >= len(inputs):
        vm_state[vm_name] = (p, pc, outputs, inp_count)
        return outputs, False
      p[p[pc + 1]] = inputs[inp_count]
      inp_count += 1
      pc += 2
    elif opcode is 4:
      outputs += [val1]
      pc += 2
    elif opcode is 5:
      if val1 is not 0:
        pc = val2
      else:
        pc += 3
    elif opcode is 6:
      if val1 is 0:
        pc = val2
      else:
        pc += 3
    elif opcode is 7:
      p[p[pc + 3]] = 1 if val1 < val2 else 0
      pc += 4
    elif opcode is 8:
      p[p[pc + 3]] = 1 if val1 is val2 else 0
      pc += 4
    elif opcode is 99:
      pc += 1
      if vm_name in vm_state:
        del vm_state[vm_name]
      break
    else:
      raise NotImplementedError(f'No implementation for opcode: {opcode}')
  return outputs, True

def evaluate_sequence(phase_sequence):
  exited_normally = False
  outE = []
  while not exited_normally:
    inA = [phase_sequence[0], 0] + outE
    outA, _ = run_vm('A', inA)
    inB = [phase_sequence[1]] + outA
    outB, _ = run_vm('B', inB)
    inC = [phase_sequence[2]] + outB
    outC, _ = run_vm('C', inC)
    inD = [phase_sequence[3]] + outC
    outD, _ = run_vm('D', inD)
    inE = [phase_sequence[4]] + outD
    outE, exited_normally = run_vm('E', inE)
  return outE[-1]

def highest_thrust_signal(start, end):
  sequences = permutations(range(start, end+1))
  highest = 0
  for sequence in sequences:
    highest = max(evaluate_sequence(list(sequence)), highest)
  return highest

def main() -> None:
  global program
  program = next(get_data(today, [('split', ','), ('map', int)]))

  print(f'{today} star 1 = {highest_thrust_signal(0, 4)}')
  print(f'{today} star 2 = {highest_thrust_signal(5, 9)}')

if __name__ == '__main__':
  timed(main)
