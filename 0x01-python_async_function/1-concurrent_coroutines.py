#!/usr/bin/env python3

"""
async functions
"""
import asyncio
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
        async function
    """
    task = [wait_random(max_delay) for _ in range(n)]
    delays = []
    for i in asyncio.as_completed(task):
        delay = await i
        delays.append(delay)
    return (delays)
