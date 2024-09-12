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
import logging  # Logging library must be imported
from falconpy import Hosts

# Step 1: Configure the logger and set the debug level.
# Standard pythonic logging functionality is fully supported.
logging.basicConfig(level=logging.DEBUG)

# Step 2: Initialize a Service or the Uber class with debugging enabled.
# Debugging must be explicitly enabled on the class for log messages to be generated.
hosts = Hosts(debug=True)  # We are using environment authentication in this example.

# Step 3: Perform any API call, debug output is controlled by the logger configuration.
response = hosts.query_devices_by_filter_scroll()
