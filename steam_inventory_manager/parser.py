"""This module provides the function to parse the command line arguments."""

import argparse
import logging
import os
import sys
from steam_inventory_manager import constants
from steam_inventory_manager import steam_api_handler

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__package__)


def get_env_api_key(env: str):
    """
    Get the STEAM_API_KEY from environment variable
    """
    api_key = os.environ.get(env)
    if api_key is None:
        raise SystemExit(f"env {env} not set. {api_key}")
    return api_key


class CustomAction(argparse.Action):
    """
    Specialized action for handling --api-key arg
    TODO remove it, depacated Class
    """

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed in CustomAction")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if "api-key" in option_string:
            setattr(namespace, self.dest, get_env_api_key(values))


def check_args(args):
    """
    Check the command line arguments for validity.
    """

    args.api_key = get_env_api_key(args.api_key)

    if args.steam_ids is None:
        if args.steam_users is None:
            raise SystemExit("Please provide either --steam-ids or --steam-users.")
        elif args.steam_users:
            args.steam_ids = [
                steam_api_handler.resolve_vanity(args.api_key, steam_user)
                for steam_user in args.steam_users
            ]

    if args.steam_ids is None and args.steam_users is None:
        raise SystemExit("Please provide either --profile-id or --profile-user.")

    # Always display player summaries if inventory is requested
    if args.display_inventory:
        args.display_player = True

    if args.display_inventory_full and not args.display_inventory:
        args.display_inventory = True


def get_args():
    """Parse the command line arguments."""
    # Set up argument parser
    parser = argparse.ArgumentParser(
        prog="steam_inventory_manager", description="Fetch Steam Manager."
    )
    parser.add_argument("--steam-ids", nargs="+", type=str, help="17-digit SteamIDs.")
    parser.add_argument("--steam-users", nargs="+", type=str, help="List of users.")
    parser.add_argument(
        "--app-id", type=str, default="570", help="The app ID (Dota 2=570)."
    )
    parser.add_argument(
        "--api-key",
        default=constants.STEAM_API_KEY_env,
        type=str,
        help=f"env variable with your Steam API key. default={constants.STEAM_API_KEY_env}",
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite the inventory files."
    )
    parser.add_argument(
        "--display-player", action="store_true", help="Display player summaries."
    )
    parser.add_argument(
        "--display-inventory",
        action="store_true",
        help="Display {BUNDLE, COURIER, HERO_BUNDLE, WARD, WEATHER} items.",
    )
    parser.add_argument(
        "--display-inventory-full",
        action="store_true",
        help="Display also {HERO, MISC} items.",
    )

    group = parser.add_argument_group('filters', description="opt1 OR opt2 ...")

    group.add_argument(
        "--filter-by-hero",
        type=str,
        help="Filter items by hero",
    )

    group.add_argument(
        "--filter-by-type",
        type=str,
        help="Filter items by type",
    )

    group.add_argument(
        "--filter-by-marketable",
        action="store_true",
        help="Filter Marketable items",
    )

    group.add_argument(
        "--filter-by-tradable",
        action="store_true",
        help="Filter tradable items",
    )

    group.add_argument(
        "--filter-by-giftable",
        action="store_true",
        help="Filter Giftable items",
    )

    args = parser.parse_args()
    check_args(args)
    return args
