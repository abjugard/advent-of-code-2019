from santas_little_helpers import day, get_data, timed, base_ops
from santas_little_utils import run_vm, get_last

today = day(2019, 22)

def part1(inp):
  cards = list(range(10007))
  for fun, arg in inp:
    cards = fun(arg, cards)
  return cards.index(2019)

# outright stolen from https://github.com/mcpower/adventofcode/blob/master/2019/22/a-improved.py
# this is all mumbo jumbo to me
# what the fuck /u/topaz2078!?
def part2(lines):
  cards = 119315717514047
  repeats = 101741582076661

  inc_mult = 1
  offset_diff = 0

  for func, arg in lines:
    if func is deal:
      inc_mult *= -1
      inc_mult %= cards
      offset_diff += inc_mult
      offset_diff %= cards
    elif func is cut:
      offset_diff += arg * inc_mult
      offset_diff %= cards
    elif func is deal_with_increment:
      inc_mult *= pow(arg, cards-2, cards)
      inc_mult %= cards

  increment = pow(inc_mult, repeats, cards)

  offset = offset_diff * (1 - increment) * pow((1 - inc_mult) % cards, cards-2, cards)
  offset %= cards

  return (offset + 2020 * increment) % cards

def deal(_, cards):
  return list(reversed(cards))

def cut(pos, cards):
  new_deck = cards[pos:]
  new_deck.extend(cards[:pos])
  return new_deck

def deal_with_increment(inc, cards):
  deck_size = len(cards)
  table = [None] * deck_size
  for deck_idx, table_idx in enumerate(range(0, deck_size * inc, inc)):
    table[table_idx % deck_size] = cards[deck_idx]
  return table

def parse(line):
  if line.startswith('deal into'):
    return deal, 0
  elif line.startswith('cut'):
    arg = int(line.split()[-1])
    return cut, arg
  elif line.startswith('deal with'):
    arg = int(line.split()[-1])
    return deal_with_increment, arg

def main() -> None:
  inp = list(get_data(today, base_ops + [('func', parse)]))
  print(f'{today} star 1 = {part1(inp)}')
  print(f'{today} star 2 = {part2(inp)}')

if __name__ == '__main__':
  timed(main)
