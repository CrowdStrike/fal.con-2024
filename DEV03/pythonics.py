#!/usr/bin/env python3
r"""
 _______                        __ _______ __        __ __
|   _   .----.-----.--.--.--.--|  |   _   |  |_.----|__|  |--.-----.
|.  1___|   _|  _  |  |  |  |  _  |   1___|   _|   _|  |    <|  -__|
|.  |___|__| |_____|________|_____|____   |____|__| |__|__|__|_____|
|:  1   |                         |:  1   |
|::.. . |                         |::.. . |         FalconPy Lab
`-------'                         `-------'

▄▄▄      ▄  █            ▀          ▄▄▄          ▄
█▄█ █ █ ▀█▀ █▀█ █▀█ █▀█  █  █▀▀     ▀▄  █ █ █▀█ ▀█▀ ▀▀█ ▀▄▀
█   █▄█  █▄ █ █ █▄█ █ █  █  █▄▄     ▄▄█ █▄█ █ █  █▄ ███ ▄▀▄
    ▄▄█                                 ▄▄█

This lab demonstrates how to leverage pythonic response syntax when using the FalconPy SDK.
"""
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from typing import List, Dict, Union
import logging
from falconpy import Hosts


# We can create our own version of a Service Class, that inherits all of the attributes,
# properties, and methods of the parent class. This allows us to create our own helper
# functions that perform compound operations quickly and easily.
class ExtendedHosts(Hosts):  # Inheriting from the Hosts Service Class
    """My custom Hosts Service Class."""

    # Enable pythonic syntax by setting the pythonic attribute to True.
    # You can also enable pythonics using any class by providing the
    # "pythonic" keyword when you create an instance of the class.
    pythonic = True

    def get_all_details(self) -> List[Dict[str, Union[str, int, Dict, List]]]:
        """Retrieve all hosts with extended details."""
        host_list = []
        offset = None
        total = 1
        while len(host_list) < total:
            result = self.query_devices_by_filter_scroll(offset=offset)
            total = result.total
            offset = result.offset
            host_list.extend(self.get_device_details(ids=result.data))
        return host_list

    def list_all_hostnames(self) -> List[str]:
        """Return a list of all hostnames within the tenant."""

        return list(h.get('hostname', h.get('device_id')) for h in self.get_all_details())


def run_lab_example(debug_mode: bool = False):
    """Execute the lab example and display the results."""

    # Create an instance of our custom Hosts Service Class as a context handler
    # using Environment Authentication. Then call our custom list_all_hostnames
    # method and loop through the results to output each hostname.
    #
    # Using the class as a context handler automatically revokes
    # the bearer token when your code exits the context.
    #
    host_list = []
    with ExtendedHosts(debug=debug_mode) as hosts:
        host_list = hosts.list_all_hostnames()
        for hostname in host_list:
            print(hostname)

    print(f"\n{len(host_list)} devices returned")


# Lab housekeeping, the following code is not part of this lab's content.
parser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)
parser.add_argument("-d", "--debug",
                    help="Enable API debugging",
                    action="store_true",
                    default=False
                    )
DEBUG = False
if parser.parse_args().debug:
    logging.basicConfig(level=logging.DEBUG)
    DEBUG = True
# Run the lab
run_lab_example(DEBUG)
