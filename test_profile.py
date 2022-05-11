from AA import sbst
import random

import logging
logging.disable(logging.INFO)


tree = sbst()
numbers = list(range(10000))
random.shuffle(numbers)
for i in numbers:
    tree.add(i)

random.shuffle(numbers)
for i in numbers:
    tree.remove(i)

if __name__ == '__main__':
    pass