#!/usr/bin/env python3
r"""
 _______                        __ _______ __        __ __
|   _   .----.-----.--.--.--.--|  |   _   |  |_.----|__|  |--.-----.
|.  1___|   _|  _  |  |  |  |  _  |   1___|   _|   _|  |    <|  -__|
|.  |___|__| |_____|________|_____|____   |____|__| |__|__|__|_____|
|:  1   |                         |:  1   |
|::.. . |                         |::.. . |         FalconPy Lab
`-------'                         `-------'

▄▄      █                ▀                        █     ▄                ▀
█ █ ███ █▀█ █ █ █▀█ █▀█  █  █▀█ █▀█     ▀▀█ █▀█ █▀█     █   █▀█ █▀█ █▀█  █  █▀█ █▀█
█▄▀ █▄▄ █▄█ █▄█ █▄█ █▄█  █  █ █ █▄█     ███ █ █ █▄█     █▄▄ █▄█ █▄█ █▄█  █  █ █ █▄█
                ▄▄█ ▄▄█         ▄▄█                             ▄▄█ ▄▄█         ▄▄█

This lab demonstrates how to activate logging within the FalconPy SDK.
"""
import time
from secrets import choice
import logging  # Logging library must be imported
from falconpy import Hosts

# Step 1: Configure the logger and set the debug level.
# Standard pythonic logging functionality is fully supported.
logging.basicConfig(level=logging.DEBUG)

# Step 2: Initialize a Service or the Uber class with debugging enabled.
# Debugging must be explicitly enabled on the class for log messages to be generated.
hosts = Hosts(debug=True)  # We are using environment authentication in this example.
while hosts.token_status == 429:
    # We hit the rate limit, inform the user and sleep for 1 to 5 seconds.
    sleep_time = choice(range(1, 5))
    print(f"Rate limit met, sleeping for {sleep_time} seconds.")
    time.sleep(sleep_time)
    # Retry on rate limit failure
    hosts = Hosts(debug=True)

# Step 3: Perform any API call, debug output is controlled by the logger configuration.
response = hosts.query_devices_by_filter_scroll()
