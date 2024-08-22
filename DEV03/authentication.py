#!/usr/bin/env python3
r"""
 _______                        __ _______ __        __ __
|   _   .----.-----.--.--.--.--|  |   _   |  |_.----|__|  |--.-----.
|.  1___|   _|  _  |  |  |  |  _  |   1___|   _|   _|  |    <|  -__|
|.  |___|__| |_____|________|_____|____   |____|__| |__|__|__|_____|
|:  1   |                         |:  1   |
|::.. . |                         |::.. . |         FalconPy Lab
`-------'                         `-------'

▄▄▄      ▄  █            ▄   ▀           ▄   ▀
█ █ █ █ ▀█▀ █▀█ ███ █▀█ ▀█▀  █  █▀▀ ▀▀█ ▀█▀  █  █▀█ █▀█
█▀█ █▄█  █▄ █ █ █▄▄ █ █  █▄  █  █▄▄ ███  █▄  █  █▄█ █ █

This lab demonstrates authentication mechanisms supported by the FalconPy SDK.
"""
from argparse import ArgumentParser, RawTextHelpFormatter
import logging
import os
import time
from secrets import choice
from falconpy import Hosts, HostGroup


def direct_authentication(debug_mode: bool = False, auth_only: bool = False):
    r"""
    ╔╦╗┬┬─┐┌─┐┌─┐┌┬┐
     ║║│├┬┘├┤ │   │
    ═╩╝┴┴└─└─┘└─┘ ┴  Authentication
    Provide a valid client ID and client secret as keyword arguments.
    """
    print(direct_authentication.__doc__)

    # Leverage the "client_id" and "client_secret" keywords for Direct Authentication
    hosts = Hosts(client_id=FALCON_CLIENT_ID, client_secret=FALCON_CLIENT_SECRET, debug=debug_mode)
    while hosts.token_status == 429:
        sleep_time = choice(range(1, 5))
        print(f"Rate limit met, sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)
        # Retry on rate limit failure
        hosts = Hosts(client_id=FALCON_CLIENT_ID,
                      client_secret=FALCON_CLIENT_SECRET,
                      debug=debug_mode
                      )
    if not auth_only:  # Run an API connectivity test for lab purposes
        response_direct = hosts.query_devices_by_filter_scroll()
        print(response_direct)


def credential_authentication(debug_mode: bool = False, auth_only: bool = False):
    r"""
    ╔═╗┬─┐┌─┐┌┬┐┌─┐┌┐┌┌┬┐┬┌─┐┬
    ║  ├┬┘├┤  ││├┤ │││ │ │├─┤│
    ╚═╝┴└─└─┘─┴┘└─┘┘└┘ ┴ ┴┴ ┴┴─┘ Authentication
    Client ID and client secret are provided as a dictionary.
    """
    print(credential_authentication.__doc__)

    # Craft a properly formatted credential dictionary
    creds = {
        "client_id": FALCON_CLIENT_ID,
        "client_secret": FALCON_CLIENT_SECRET
    }
    # Provide this dictionary to the "creds" keyword for Credential Authentication
    hosts = Hosts(creds=creds, debug=debug_mode)
    while hosts.token_status == 429:
        sleep_time = choice(range(1, 5))
        print(f"Rate limit met, sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)
        # Retry on rate limit failure
        hosts = Hosts(creds=creds, debug=debug_mode)
    if not auth_only:  # Run an API connectivity test for lab purposes
        response_obj = hosts.query_devices_by_filter_scroll()
        print(response_obj)


def environment_authentication(debug_mode: bool = False, auth_only: bool = False):
    r"""
    ╔═╗┌┐┌┬  ┬┬┬─┐┌─┐┌┐┌┌┬┐┌─┐┌┐┌┌┬┐
    ║╣ │││└┐┌┘│├┬┘│ │││││││├┤ │││ │
    ╚═╝┘└┘ └┘ ┴┴└─└─┘┘└┘┴ ┴└─┘┘└┘ ┴  Authentication
    Client ID and client secret are retrieve using the FALCON_CLIENT_ID
    and FALCON_CLIENT_SECRET environment variables.
    """
    print(environment_authentication.__doc__)

    # No keywords are required to use Environment Authentication
    hosts = Hosts(debug=debug_mode)
    while hosts.token_status == 429:
        sleep_time = choice(range(1, 5))
        print(f"Rate limit met, sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)
        # Retry on rate limit failure
        hosts = Hosts(debug=debug_mode)
    if not auth_only:  # Run an API connectivity test for lab purposes
        response_env = hosts.query_devices_by_filter_scroll()
        print(response_env)


def object_authentication(debug_mode: bool = False, auth_only: bool = False):
    r"""
    ╔═╗┌┐  ┬┌─┐┌─┐┌┬┐
    ║ ║├┴┐ │├┤ │   │
    ╚═╝└─┘└┘└─┘└─┘ ┴  Authentication
    An existing service class is used to authenticate
    additional FalconPy service classes.
    """
    print(object_authentication.__doc__)

    # The initial object leverages one of the other authentication styles,
    # eg. Direct, Credential, Environment.
    hosts = Hosts(debug=debug_mode)  # This example is using Environment Authentication
    while hosts.token_status == 429:
        sleep_time = choice(range(1, 5))
        print(f"Rate limit met, sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)
        # Retry on rate limit failure
        hosts = Hosts(debug=debug_mode)
    # Subsequent objects can leverage a previously authenticated object
    host_group = HostGroup(auth_object=hosts)  # Provides the pre-existing Hosts object
    if not auth_only:  # Run an API connectivity test for lab purposes
        response_hosts = hosts.query_devices_by_filter_scroll()
        print("Object one\n", response_hosts)
        response_host_group = host_group.query_combined_host_groups()
        print("Object two\n", response_host_group)


# Lab Main Routine
# This code provides the execution interface for this lab but is not part of the lab content.
if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument("-k", "--falcon_client_id", help="Falcon API client ID")
    parser.add_argument("-s", "--falcon_client_secret", help="Falcon API client secret")
    parser.add_argument("-d", "--debug",
                        help="Enable API Debugging",
                        action="store_true",
                        default=False
                        )
    parser.add_argument("-a", "--auth_only",
                        help="Do not run API connectivity tests, only authenticate.",
                        action="store_true",
                        default=False
                        )
    parsed = parser.parse_args()
    FALCON_CLIENT_ID = parsed.falcon_client_id
    FALCON_CLIENT_SECRET = parsed.falcon_client_secret
    if not FALCON_CLIENT_ID:
        retrieve = input("\nFalcon API client ID not provided on command line.\n"
                         "Would you like me to retrieve this value from the environment (y/n)? "
                         ).lower()
        if retrieve == "y":
            FALCON_CLIENT_ID = os.getenv("FALCON_CLIENT_ID")
        else:
            FALCON_CLIENT_ID = input("Please input your Falcon API client ID: ")
    if not FALCON_CLIENT_SECRET:
        retrieve = input("\nFalcon API client secret not provided on command line.\n"
                         "Would you like me to retrieve this value from the environment (y/n)? "
                         ).lower()
        if retrieve == "y":
            FALCON_CLIENT_SECRET = os.getenv("FALCON_CLIENT_SECRET")
        else:
            FALCON_CLIENT_SECRET = input("Please input your Falcon API client ID: ")
    DEBUG = parsed.debug
    AUTH_ONLY = parsed.auth_only
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    BEGIN = r"""
    ██████  ███████  ██████  ██ ███    ██     ██       █████  ██████
    ██   ██ ██      ██       ██ ████   ██     ██      ██   ██ ██   ██
    ██████  █████   ██   ███ ██ ██ ██  ██     ██      ███████ ██████
    ██   ██ ██      ██    ██ ██ ██  ██ ██     ██      ██   ██ ██   ██
    ██████  ███████  ██████  ██ ██   ████     ███████ ██   ██ ██████
    """
    print(BEGIN)
    direct_authentication(DEBUG, AUTH_ONLY)
    credential_authentication(DEBUG, AUTH_ONLY)
    environment_authentication(DEBUG, AUTH_ONLY)
    object_authentication(DEBUG, AUTH_ONLY)
