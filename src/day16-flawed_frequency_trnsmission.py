from santas_little_helpers import day, get_data, timed, base_ops

today = day(2019, 16)

def repeating(n, offset=0):
  n += 1
  p = [0, 1, 0, -1]
  i = offset
  while True:
    idx = (i+1) // n
    yield p[idx % 4]
    i += 1

def calc_phase(sequence):
  new = []
  l = len(sequence)
  for n in range(l):
    temp = sum(a*b for a, b in zip(sequence, repeating(n)))
    new.append(abs(temp) % 10)
  return new

def fft(sequence):
  for _ in range(100):
    sequence = calc_phase(sequence)
  return ''.join(str(c) for c in sequence[:8])

def fft_edge_case(sequence):
  offset = int(''.join(str(c) for c in sequence[:7]))
  sub_sequence = (sequence * 10000)[offset:]
  l = len(sub_sequence)
  for _ in range(100):
    temp_sum = sum(sub_sequence)
    temp_sum2 = sum(a*b for a, b in zip(sub_sequence, repeating(offset)))
    for j in range(l):
      temp = abs(temp_sum) % 10
      temp_sum -= sub_sequence[j]
      sub_sequence[j] = temp
  return ''.join(str(c) for c in sub_sequence[:8])

def main() -> None:
  inp = next(get_data(today, base_ops + [('map', int)]))
  print(f'{today} star 1 = {fft(inp)}')
  print(f'{today} star 2 = {fft_edge_case(inp)}')

if __name__ == '__main__':
  timed(main)
