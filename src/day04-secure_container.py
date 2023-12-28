from santas_little_helpers import day, get_data, timed, base_ops
from collections import Counter

today = day(2019, 4)

def get_ranges(lower, upper):
  iupper = int(upper)
  ilower = int(lower)
  for a in range(int(lower[0]), int(upper[0])+1):
    for b in range(a, 10):
      for c in range(b, 10):
        for d in range(c, 10):
          for e in range(d, 10):
            for f in range(e, 10):
              pwd = [a, b, c, d, e, f]
              ipwd = int(''.join(map(str, pwd)))
              if ipwd <= iupper and ipwd >= ilower:
                yield pwd

def check_passwords(inp):
  star1 = star2 = 0
  for password in get_ranges(inp[0], inp[1]):
    repeating_lengths = Counter(password).values()
    if any(size >= 2 for size in repeating_lengths):
      star1 += 1
    else:
      continue
    if any(size == 2 for size in repeating_lengths):
      star2 += 1
  return star1, star2

def main() -> None:
  inp = next(get_data(today, base_ops + [('split', '-')]))
  star1, star2 = check_passwords(inp)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {star2}')

if __name__ == '__main__':
  timed(main)
