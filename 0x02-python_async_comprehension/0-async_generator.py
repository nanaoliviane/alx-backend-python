#!/usr/bin/env python3
'''Async generator module.
'''
import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    '''Generates a sequence of 10 numbers.
       Each number is generated after 1-second delay
    '''
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10
