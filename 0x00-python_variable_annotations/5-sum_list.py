#!/usr/bin/env python3
'''sum_list function module
'''
from typing import List


def sum_list(input_list: List[float]) -> float:
    '''Computes the sum of a list of floating-point numbers.
    '''
    return float(sum(input_list))
