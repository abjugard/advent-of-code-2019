from santas_little_helpers import day, get_data, timed
from collections import Counter

today = day(2019, 4)

def check_passwords(inp, extended_criteria = False):
  usable = []
  for password in [str(i) for i in range(inp[0], inp[1])]:
    if not password == ''.join(sorted(password)):
      continue
    repeating_lengths = Counter(password).values()
    if extended_criteria:
      if not any(size == 2 for size in repeating_lengths):
        continue
    else:
      if not any(size >= 2 for size in repeating_lengths):
        continue
    usable += [password]
  return len(usable)

def main() -> None:
  inp = next(get_data(today, [('split', '-'), ('map', int)]))
  print(f'{today} star 1 = {check_passwords(inp)}')
  print(f'{today} star 2 = {check_passwords(inp, extended_criteria = True)}')

if __name__ == '__main__':
  timed(main)
