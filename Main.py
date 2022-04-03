from ..Houses import get_houses
import numpy as np

## Minimize probability of Exceedance until its less than or equal to
## Fraction of uncovered houses

max_uncovered_rate = 0.3
minimum_covering_to_be_served = 1 # A house has to have 100% service rate
max_num_towers = 20

houses = get_houses()