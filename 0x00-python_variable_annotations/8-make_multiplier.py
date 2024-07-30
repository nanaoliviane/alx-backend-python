#!/usr/bin/env python3
'''
 make_multiplier function module
'''

from typing import Callable

def make_multiplier(multiplier: float) -> Callable[[float], float]:
    '''
    Returns a function that multiplies a float by a given multiplier
    
    Parameters:
    multiplier (float): The multiplier
    
    Returns:
    Callable[[float], float]: A function that takes a float and returns its product with the multiplier
    '''
    def multiplier_func(num: float) -> float:
        return num * multiplier
    
    return multiplier_func
