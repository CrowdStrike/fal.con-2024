#!/usr/bin/env python3
r"""
 _______                        __ _______ __        __ __
|   _   .----.-----.--.--.--.--|  |   _   |  |_.----|__|  |--.-----.
|.  1___|   _|  _  |  |  |  |  _  |   1___|   _|   _|  |    <|  -__|
|.  |___|__| |_____|________|_____|____   |____|__| |__|__|__|_____|
|:  1   |                         |:  1   |
|::.. . |                         |::.. . |         FalconPy Lab
`-------'                         `-------'

▄▄▄          █            █     ▄ ▄           █  █   ▀
█▄█ ▀▀█ █ █  █  █▀█ ▀▀█ █▀█     █▄█ ▀▀█ █▀█ █▀█  █   █  █▀█ █▀█
█   ███ █▄█  █▄ █▄█ ███ █▄█     █ █ ███ █ █ █▄█  █▄  █  █ █ █▄█
        ▄▄█                                                 ▄▄█

This lab demonstrates how to handle different payload types within the FalconPy SDK.
"""
import socket
from argparse import ArgumentParser, RawTextHelpFormatter
import logging
import time
from secrets import choice
from falconpy import APIHarnessV2, Detects, HostGroup


def query_string_parameters(debug_mode: bool = False):
    r"""
    ╔═╗ ┬ ┬┌─┐┬─┐┬ ┬  ╔═╗┌┬┐┬─┐┬┌┐┌┌─┐  ╔═╗┌─┐┬─┐┌─┐┌┬┐┌─┐┌┬┐┌─┐┬─┐┌─┐
    ║═╬╗│ │├┤ ├┬┘└┬┘  ╚═╗ │ ├┬┘│││││ ┬  ╠═╝├─┤├┬┘├─┤│││├┤  │ ├┤ ├┬┘└─┐
    ╚═╝╚└─┘└─┘┴└─ ┴   ╚═╝ ┴ ┴└─┴┘└┘└─┘  ╩  ┴ ┴┴└─┴ ┴┴ ┴└─┘ ┴ └─┘┴└─└─┘
    Query String parameter abstraction is fully supported in all classes.
    """
    print(query_string_parameters.__doc__)
    uber = APIHarnessV2(debug=debug_mode)   # Uber Class
    # Check for rate limiting in our lab environment by forcing a login.
    # Unlike a Service Class, the Uber Class does not authenticate until
    # the first request is performed, or the login event is called.
    uber.login()
    while uber.token_status == 429:
        # We hit the rate limit, inform the user and sleep for 1 to 5 seconds.
        sleep_time = choice(range(1, 5))
        print(f"Rate limit met, sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)
        # Retry on rate limit failure
        uber.login()
    detects = Detects(auth_object=uber)     # Detects Service Class
    # When we are not using abstraction, query string parameters must
    # be provided to the parameters keywords as a dictionary.
    payload = {
        "filter": "status:'new'"
    }
    # This payload is provided to the parameters keyword argument.
    result = detects.query_detects(parameters=payload)
    print("\nService Class without using abstraction\n", result)
    # Uber Class example - the same keyword argument is used.
    result = uber.command("QueryDetects", parameters=payload)
    print("\nUber Class without using abstraction\n", result)

    # Leveraging Query String Parameter Abstraction, we can skip the payload creation step
    # and provide required query string parameters as keyword arguments directly.
    result = detects.query_detects(filter="status:'new'")
    print("\nService Class using abstraction\n", result)

    # Query String Parameter Abstraction is fully supported by the Uber class.
    result = uber.command("QueryDetects", filter="status:'new'")
    print("\nUber Class using abstraction\n", result)

    return uber


def body_parameters(uber: APIHarnessV2):
    r"""
    ╔╗ ┌─┐┌┬┐┬ ┬  ╔═╗┌─┐┬─┐┌─┐┌┬┐┌─┐┌┬┐┌─┐┬─┐  ╔═╗┌─┐┬ ┬┬  ┌─┐┌─┐┌┬┐┌─┐
    ╠╩╗│ │ ││└┬┘  ╠═╝├─┤├┬┘├─┤│││├┤  │ ├┤ ├┬┘  ╠═╝├─┤└┬┘│  │ │├─┤ ││└─┐
    ╚═╝└─┘─┴┘ ┴   ╩  ┴ ┴┴└─┴ ┴┴ ┴└─┘ ┴ └─┘┴└─  ╩  ┴ ┴ ┴ ┴─┘└─┘┴ ┴─┴┘└─┘
    Body parameter payloads is fully supported in all Service Classes.
    The Uber class currently only supports the abstraction of the "ids"
    body payload parameter.
    """
    print(body_parameters.__doc__)
    unique_id = socket.gethostname()  # Lab housekeeping for unique host group names
    host_group = HostGroup(auth_object=uber)  # Auth this class using our previous token
    # When we are not using abstraction, we will need to craft a payload dictionary
    # that exactly matches the expected payload format. This can be found at falconpy.io.
    payload = {
        "resources": [
            {
                "description": f"Test Group for {unique_id}",
                "group_type": "static",
                "name": f"TestGroup_{unique_id}"
            }
        ]
    }
    # This manually crafted payload is provided to the body keyword argument.
    result = host_group.create_host_groups(body=payload)
    print("\nService Class Host Group creation (No Abstraction)\n", result)
    host_group_id = result["body"]["resources"][0]["id"]
    # Remove the group we just created (Lab Housekeeping)
    delete_result = host_group.delete_host_groups(host_group_id)
    if delete_result["status_code"] != 200:
        raise SystemExit(f"Lab Error: Unable to remove host group ({host_group_id})")

    # Leveraging Body Payload abstraction, we can skip the payload creation step and
    # instead provide the necessary values as keyword arguments directly.
    # This functionality is NOT CURRENTLY SUPPORTED within the Uber Class in most scenarios.
    result = host_group.create_host_groups(group_type="static",
                                           name=f"TestGroup_{unique_id}",
                                           description=f"Test Group for {unique_id}"
                                           )
    print("\nService Class Host Group creation (With Abstraction)\n", result)
    host_group_id = result["body"]["resources"][0]["id"]
    # Remove the group we just created
    delete_result = host_group.delete_host_groups(host_group_id)
    if delete_result["status_code"] != 200:
        raise SystemExit(f"Lab Error: Unable to remove host group ({host_group_id})")

    # The Uber Class does support Body Payload abstraction for the "ids" parameter for all
    # API operations that use it.
    host_aid = uber.command("QueryDevicesByFilterScroll", limit=1)["body"]["resources"][0]
    payload = {
        "ids": [host_aid]
    }
    result = uber.command("PostDeviceDetailsV2", body=payload)
    print("\nUber Class without abstraction\n", result)
    result = uber.command("PostDeviceDetailsV2", ids=host_aid)
    print("\nUber Class with abstraction\n", result)


# Lab Main Routine
# This code provides the execution interface for this lab but is not part of the lab content.
if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument("-d", "--debug",
                        help="Enable API Debugging",
                        action="store_true",
                        default=False
                        )
    parsed = parser.parse_args()
    DEBUG = False
    if parsed.debug:
        logging.basicConfig(level=logging.DEBUG)
        DEBUG = True

    body_parameters(query_string_parameters(DEBUG))  # Run the lab
