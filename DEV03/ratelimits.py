#!/usr/bin/env python3
r"""
 _______                        __ _______ __        __ __
|   _   .----.-----.--.--.--.--|  |   _   |  |_.----|__|  |--.-----.
|.  1___|   _|  _  |  |  |  |  _  |   1___|   _|   _|  |    <|  -__|
|.  |___|__| |_____|________|_____|____   |____|__| |__|__|__|_____|
|:  1   |                         |:  1   |
|::.. . |                         |::.. . |         FalconPy Lab
`-------'                         `-------'

▄▄▄      ▄          ▄    ▀       ▀   ▄
█▄▀ ▀▀█ ▀█▀ ███     █    █  ███  █  ▀█▀ █▀▀
█ █ ███  █▄ █▄▄     █▄▄  █  █ █  █   █▄ ▄▄█

This lab demonstrates a simple solution for handling rate limits received from the API.
"""
import time
from concurrent.futures import ThreadPoolExecutor
from secrets import choice
from dataclasses import dataclass
from falconpy import Hosts


@dataclass
class Demo:
    """Simple data class to store this example's configuration and status."""
    # Total number of iterations we will perform
    iterations: int = 300
    # Total number of concurrent threads we will execute
    max_threads: int = 30
    # Outstanding authentication attempts to be processed
    pending: int = 300


def run_demo(iteration: int):
    """Asynchronously perform a login using the Hosts Service Class, retring when rate limited."""
    # Create an instance of the Hosts Service Class. This will trigger an authentication attempt.
    hosts = Hosts()
    # Counter to store the number of retries performed
    retries = 0
    while hosts.token_status == 429:
        # This solution will continue to retry until a successful call is made
        # A more robust solution would exit the solution after a specified
        # number of retries had been performed.
        retries += 1
        # Psuedo-random retry time calculation.
        sleep_time = choice(range(1, 3)) + float(f"{retries}.{iteration}")
        print(f" Rate limit met, retrying {iteration} in {sleep_time}...{20*' '}", end="\r")
        # Sleep until our next attempt.
        time.sleep(sleep_time)
        # Try authenticating again.
        hosts = Hosts()

    # Decrement our pending execution count.
    DEMO.pending -= 1
    # Inform the user that this iteration is successful.
    print(f"Iteration {iteration} authenticated after {retries+1} attempts.",
          f" [{DEMO.pending} remain]{20*' '}")


# Create an instance of our demo data class.
DEMO = Demo()
# Asynchronously attempt to authenticate demo.iterations number of times.
with ThreadPoolExecutor(max_workers=DEMO.max_threads) as executor:
    futures = {executor.map(run_demo, range(1, DEMO.iterations+1))}
